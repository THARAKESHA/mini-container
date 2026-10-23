#define _GNU_SOURCE
#include "namespaces.h"
#include <sched.h>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/mount.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <signal.h>

#define STACK_SIZE (1024 * 1024) // 1MB child stack

static int container_child_entry(void *arg) {
    container_config_t *config = (container_config_t *)arg;

    // 1. Wait for parent to finish configuring cgroups limits
    close(config->sync_pipe[1]); // Close write end
    char sync_byte;
    if (read(config->sync_pipe[0], &sync_byte, 1) <= 0) {
        fprintf(stderr, "[container-child] Error reading sync pipe: %s\n", strerror(errno));
        return 1;
    }
    close(config->sync_pipe[0]); // Close read end

    // 2. Set UTS Hostname
    if (strlen(config->hostname) > 0) {
        if (sethostname(config->hostname, strlen(config->hostname)) != 0) {
            perror("[container-child] sethostname failed");
        }
    }

    // 3. Make all mounts private to avoid leaking mount events to host
    if (mount(NULL, "/", NULL, MS_REC | MS_PRIVATE, NULL) != 0) {
        perror("[container-child] Warning: mount(/, MS_PRIVATE) failed");
    }

    // 4. File system isolation (Rootfs & chroot)
    if (strlen(config->rootfs) > 0) {
        // Bind mount the rootfs to ensure it is a mount point
        if (mount(config->rootfs, config->rootfs, "bind", MS_BIND | MS_REC, NULL) != 0) {
            fprintf(stderr, "[container-child] Warning: bind mount on %s failed: %s\n",
                    config->rootfs, strerror(errno));
        }

        // Chroot into isolated root filesystem
        if (chroot(config->rootfs) != 0) {
            fprintf(stderr, "[container-child] Error: chroot to %s failed: %s\n",
                    config->rootfs, strerror(errno));
            return 1;
        }

        if (chdir("/") != 0) {
            perror("[container-child] chdir(/) failed");
            return 1;
        }

        // Mount pseudo filesystem /proc inside container for process isolation
        mkdir("/proc", 0755);
        if (mount("proc", "/proc", "proc", 0, NULL) != 0) {
            fprintf(stderr, "[container-child] Warning: mount(/proc) failed: %s\n", strerror(errno));
        }
    }

    // 5. Execute target payload command
    printf("[container-child] Executing: %s (PID=%d)\n", config->argv[0], getpid());
    fflush(stdout);

    execvp(config->argv[0], config->argv);

    // If execvp returns, an error occurred
    fprintf(stderr, "[container-child] execvp failed for '%s': %s\n",
            config->argv[0], strerror(errno));
    return 127;
}

int container_run(container_config_t *config) {
    if (!config || !config->argv || !config->argv[0]) {
        fprintf(stderr, "[container] Error: Invalid configuration or command\n");
        return -1;
    }

    // Initialize synchronization pipe
    if (pipe(config->sync_pipe) != 0) {
        perror("[container] pipe creation failed");
        return -1;
    }

    // Allocate stack for clone
    char *stack = malloc(STACK_SIZE);
    if (!stack) {
        perror("[container] Failed to allocate child stack");
        return -1;
    }
    char *stack_top = stack + STACK_SIZE;

    // Namespace flags:
    // CLONE_NEWUTS : Hostname isolation
    // CLONE_NEWPID : Process ID isolation (child becomes PID 1)
    // CLONE_NEWNS  : Mount filesystem isolation
    // CLONE_NEWIPC : Inter-Process Communication isolation (semaphores, message queues)
    int clone_flags = CLONE_NEWUTS | CLONE_NEWPID | CLONE_NEWNS | CLONE_NEWIPC | SIGCHLD;

    printf("[container] Spawning child with namespaces (PID, UTS, NS, IPC)...\n");
    fflush(stdout);
    fflush(stderr);
    pid_t child_pid = clone(container_child_entry, stack_top, clone_flags, config);

    if (child_pid < 0) {
        perror("[container] clone failed");
        free(stack);
        return -1;
    }

    printf("[container] Child process spawned with Host PID: %d\n", child_pid);

    // Parent setup: Configure cgroups resource limits
    close(config->sync_pipe[0]); // Parent closes read end

    cgroups_setup(child_pid, &config->cgroup_cfg);

    // Signal child to continue execution
    char signal_byte = 'G';
    if (write(config->sync_pipe[1], &signal_byte, 1) != 1) {
        perror("[container] Failed to signal child via sync pipe");
    }
    close(config->sync_pipe[1]); // Close write end

    // Wait for containerized child process to finish
    int status = 0;
    waitpid(child_pid, &status, 0);

    // Clean up cgroups
    cgroups_cleanup(&config->cgroup_cfg);
    free(stack);

    printf("--------------------------------------------------\n");
    if (WIFEXITED(status)) {
        int exit_code = WEXITSTATUS(status);
        printf("[container] Container exited cleanly with code: %d\n", exit_code);
        return exit_code;
    } else if (WIFSIGNALED(status)) {
        int term_sig = WTERMSIG(status);
        printf("[container] Container terminated by signal: %d (%s)\n",
               term_sig, strsignal(term_sig));
        if (term_sig == SIGKILL) {
            printf("[container] Notice: SIGKILL received. If memory limit was set, this indicates OS Out-Of-Memory (OOM) Killer!\n");
        }
        return 128 + term_sig;
    }

    return 0;
}
