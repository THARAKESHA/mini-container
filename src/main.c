#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <unistd.h>
#include "namespaces.h"
#include "cgroups.h"

static void print_banner(void) {
    printf("====================================================\n");
    printf("       MINI-CONTAINER: Linux Sandbox Runtime         \n");
    printf("  OS Isolation via Namespaces & Cgroups v2 in C      \n");
    printf("====================================================\n");
}

static void print_usage(const char *prog_name) {
    printf("Usage: %s run [OPTIONS] <command> [args...]\n\n", prog_name);
    printf("Options:\n");
    printf("  --memory <size>       Memory limit (e.g., 30M, 64M, 1G, 50000000)\n");
    printf("  --cpu <percent>       CPU quota percentage (1-100%%, CFS scheduling limit)\n");
    printf("  --cpu-weight <weight> CPU proportional share weight (1-10000, default: 100)\n");
    printf("  --pids <count>        Maximum process/thread count (fork bomb protection)\n");
    printf("  --hostname <name>     Container hostname (UTS namespace, default: container-box)\n");
    printf("  --rootfs <dir>        Path to isolated root filesystem (Alpine userland)\n");
    printf("  --help                Display this help message\n\n");
    printf("Examples:\n");
    printf("  sudo %s run --hostname test-box /bin/sh\n", prog_name);
    printf("  sudo %s run --memory 30M ./tests/test_memory 60\n", prog_name);
    printf("  sudo %s run --cpu-weight 800 ./tests/test_cpu 5\n", prog_name);
    printf("  sudo %s run --pids 10 ./tests/test_forkbomb\n\n", prog_name);
}

static long long parse_memory_size(const char *str) {
    char *endptr;
    double val = strtod(str, &endptr);
    if (val <= 0) return -1;

    while (isspace((unsigned char)*endptr)) endptr++;

    if (*endptr == '\0') {
        return (long long)val; // Raw bytes
    } else if (toupper((unsigned char)*endptr) == 'K') {
        return (long long)(val * 1024);
    } else if (toupper((unsigned char)*endptr) == 'M') {
        return (long long)(val * 1024 * 1024);
    } else if (toupper((unsigned char)*endptr) == 'G') {
        return (long long)(val * 1024 * 1024 * 1024);
    }

    return -1;
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        print_banner();
        print_usage(argv[0]);
        return 1;
    }

    if (strcmp(argv[1], "--help") == 0 || strcmp(argv[1], "-h") == 0) {
        print_usage(argv[0]);
        return 0;
    }

    if (strcmp(argv[1], "run") != 0) {
        fprintf(stderr, "Unknown command '%s'. Only 'run' is supported.\n", argv[1]);
        print_usage(argv[0]);
        return 1;
    }

    // Check root privileges
    if (geteuid() != 0) {
        fprintf(stderr, "[Error] mini-container requires root privileges for namespace creation and cgroups setup.\n");
        fprintf(stderr, "Please re-run using: sudo %s ...\n", argv[0]);
        return 1;
    }

    container_config_t config;
    memset(&config, 0, sizeof(config));
    strncpy(config.hostname, "container-box", sizeof(config.hostname) - 1);

    int cmd_idx = -1;
    for (int i = 2; i < argc; i++) {
        if (strcmp(argv[i], "--memory") == 0 && i + 1 < argc) {
            config.cgroup_cfg.memory_limit_bytes = parse_memory_size(argv[++i]);
            if (config.cgroup_cfg.memory_limit_bytes <= 0) {
                fprintf(stderr, "Invalid memory format: %s\n", argv[i]);
                return 1;
            }
        } else if (strcmp(argv[i], "--cpu") == 0 && i + 1 < argc) {
            config.cgroup_cfg.cpu_percent = atoi(argv[++i]);
            if (config.cgroup_cfg.cpu_percent <= 0 || config.cgroup_cfg.cpu_percent > 100) {
                fprintf(stderr, "Invalid CPU percentage (must be 1-100): %s\n", argv[i]);
                return 1;
            }
        } else if (strcmp(argv[i], "--cpu-weight") == 0 && i + 1 < argc) {
            config.cgroup_cfg.cpu_weight = atoi(argv[++i]);
            if (config.cgroup_cfg.cpu_weight < 1 || config.cgroup_cfg.cpu_weight > 10000) {
                fprintf(stderr, "Invalid CPU weight (must be 1-10000): %s\n", argv[i]);
                return 1;
            }
        } else if (strcmp(argv[i], "--pids") == 0 && i + 1 < argc) {
            config.cgroup_cfg.max_pids = atoi(argv[++i]);
            if (config.cgroup_cfg.max_pids <= 0) {
                fprintf(stderr, "Invalid pids limit: %s\n", argv[i]);
                return 1;
            }
        } else if (strcmp(argv[i], "--hostname") == 0 && i + 1 < argc) {
            strncpy(config.hostname, argv[++i], sizeof(config.hostname) - 1);
        } else if (strcmp(argv[i], "--rootfs") == 0 && i + 1 < argc) {
            strncpy(config.rootfs, argv[++i], sizeof(config.rootfs) - 1);
        } else {
            // First non-flag argument is the command
            cmd_idx = i;
            break;
        }
    }

    if (cmd_idx == -1) {
        fprintf(stderr, "Error: No command specified to run inside container.\n");
        print_usage(argv[0]);
        return 1;
    }

    config.argv = &argv[cmd_idx];

    print_banner();
    printf("Container Configuration:\n");
    printf("  Hostname   : %s\n", config.hostname);
    if (strlen(config.rootfs) > 0) {
        printf("  Rootfs     : %s\n", config.rootfs);
    } else {
        printf("  Rootfs     : (Host filesystem)\n");
    }
    if (config.cgroup_cfg.memory_limit_bytes > 0) {
        printf("  Memory     : %.2f MB\n", (double)config.cgroup_cfg.memory_limit_bytes / (1024.0 * 1024.0));
    } else {
        printf("  Memory     : Unlimited\n");
    }
    if (config.cgroup_cfg.cpu_percent > 0) {
        printf("  CPU Quota  : %d%%\n", config.cgroup_cfg.cpu_percent);
    } else {
        printf("  CPU Quota  : Unlimited\n");
    }
    if (config.cgroup_cfg.cpu_weight > 0) {
        printf("  CPU Weight : %d (Proportional Share)\n", config.cgroup_cfg.cpu_weight);
    }
    if (config.cgroup_cfg.max_pids > 0) {
        printf("  Max PIDs   : %d\n", config.cgroup_cfg.max_pids);
    } else {
        printf("  Max PIDs   : Unlimited\n");
    }
    printf("  Command    : %s\n", config.argv[0]);
    printf("--------------------------------------------------\n");

    return container_run(&config);
}
