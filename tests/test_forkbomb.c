#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <errno.h>
#include <string.h>

int main(int argc, char *argv[]) {
    int max_attempts = 50;
    if (argc > 1) {
        max_attempts = atoi(argv[1]);
    }

    printf("[test_forkbomb] Attempting to spawn %d child processes...\n", max_attempts);
    int spawned = 0;

    for (int i = 0; i < max_attempts; i++) {
        pid_t pid = fork();
        if (pid < 0) {
            printf("[test_forkbomb] Fork blocked at process #%d! Error: %s (errno=%d)\n",
                   spawned + 1, strerror(errno), errno);
            printf("[test_forkbomb] Cgroup pids.max protection successfully prevented resource exhaustion!\n");
            break;
        } else if (pid == 0) {
            // Child: Sleep briefly and exit
            sleep(2);
            exit(0);
        } else {
            spawned++;
            printf("[test_forkbomb] Successfully spawned child process %d (PID=%d)\n", spawned, pid);
        }
    }

    // Wait for all spawned children to finish
    printf("[test_forkbomb] Cleaning up %d spawned processes...\n", spawned);
    for (int i = 0; i < spawned; i++) {
        wait(NULL);
    }
    printf("[test_forkbomb] Completed.\n");
    return 0;
}
