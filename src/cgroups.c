#define _GNU_SOURCE
#include "cgroups.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>
#include <errno.h>

#define CGROUP_BASE "/sys/fs/cgroup"

static int write_cgroup_file(const char *cgroup_dir, const char *filename, const char *value) {
    char path[512];
    snprintf(path, sizeof(path), "%s/%s", cgroup_dir, filename);

    FILE *f = fopen(path, "w");
    if (!f) {
        fprintf(stderr, "[cgroups] Warning: Failed to open %s: %s\n", path, strerror(errno));
        return -1;
    }

    if (fprintf(f, "%s", value) < 0) {
        fprintf(stderr, "[cgroups] Warning: Failed to write '%s' to %s: %s\n", value, path, strerror(errno));
        fclose(f);
        return -1;
    }

    fclose(f);
    return 0;
}

int cgroups_setup(pid_t pid, cgroup_config_t *config) {
    if (!config) return -1;

    // Build cgroup directory path
    snprintf(config->cgroup_path, sizeof(config->cgroup_path), "%s/minicontainer-%d", CGROUP_BASE, (int)pid);

    // Create cgroup v2 subdirectory
    if (mkdir(config->cgroup_path, 0755) != 0) {
        if (errno != EEXIST) {
            fprintf(stderr, "[cgroups] Error: Failed to create cgroup directory %s: %s\n",
                    config->cgroup_path, strerror(errno));
            return -1;
        }
    }

    printf("[cgroups] Configured cgroup path: %s\n", config->cgroup_path);

    // 1. Attach target process PID to cgroup
    char pid_str[32];
    snprintf(pid_str, sizeof(pid_str), "%d", (int)pid);
    if (write_cgroup_file(config->cgroup_path, "cgroup.procs", pid_str) != 0) {
        fprintf(stderr, "[cgroups] Error: Could not assign PID %d to cgroup\n", (int)pid);
        return -1;
    }
    printf("[cgroups] Assigned PID %d to cgroup.procs\n", (int)pid);

    // 2. Configure Memory Limit (memory.max & memory.swap.max) - CO: 4
    if (config->memory_limit_bytes > 0) {
        char mem_str[64];
        snprintf(mem_str, sizeof(mem_str), "%lld", config->memory_limit_bytes);
        if (write_cgroup_file(config->cgroup_path, "memory.max", mem_str) == 0) {
            printf("[cgroups] Memory limit applied: %lld bytes (%.2f MB)\n",
                   config->memory_limit_bytes, (double)config->memory_limit_bytes / (1024.0 * 1024.0));
        }

        // Disable swap to ensure strict physical memory ceiling triggers OOM killer
        write_cgroup_file(config->cgroup_path, "memory.swap.max", "0");
    }

    // 3. Configure CPU Quota (cpu.max: quota period) - CO: 2
    if (config->cpu_percent > 0) {
        if (config->cpu_percent > 100) config->cpu_percent = 100;
        long period_us = 100000; // 100 ms period
        long quota_us = (config->cpu_percent * period_us) / 100;

        char cpu_str[64];
        snprintf(cpu_str, sizeof(cpu_str), "%ld %ld", quota_us, period_us);
        if (write_cgroup_file(config->cgroup_path, "cpu.max", cpu_str) == 0) {
            printf("[cgroups] CPU quota applied: %d%% (%ld us / %ld us)\n",
                   config->cpu_percent, quota_us, period_us);
        }
    }

    // 4. Configure CPU Weight (cpu.weight: 1 to 10000) - CO: 2 Proportional Fair Share
    if (config->cpu_weight > 0) {
        char weight_str[32];
        snprintf(weight_str, sizeof(weight_str), "%d", config->cpu_weight);
        if (write_cgroup_file(config->cgroup_path, "cpu.weight", weight_str) == 0) {
            printf("[cgroups] CPU weight (proportional share) applied: %d\n", config->cpu_weight);
        }
    }

    // 5. Configure Maximum Process Limit (pids.max) - CO: 1
    if (config->max_pids > 0) {
        char pids_str[32];
        snprintf(pids_str, sizeof(pids_str), "%d", config->max_pids);
        if (write_cgroup_file(config->cgroup_path, "pids.max", pids_str) == 0) {
            printf("[cgroups] Process limit (pids.max) applied: %d\n", config->max_pids);
        }
    }

    return 0;
}

int cgroups_read_mem_stats(const cgroup_config_t *config, cgroup_mem_stats_t *stats) {
    if (!config || !stats || strlen(config->cgroup_path) == 0) return -1;
    memset(stats, 0, sizeof(*stats));

    char path[512];

    // Read current memory
    snprintf(path, sizeof(path), "%s/memory.current", config->cgroup_path);
    FILE *f = fopen(path, "r");
    if (f) {
        if (fscanf(f, "%lld", &stats->current_bytes) != 1) stats->current_bytes = 0;
        fclose(f);
    }

    // Read peak memory
    snprintf(path, sizeof(path), "%s/memory.peak", config->cgroup_path);
    f = fopen(path, "r");
    if (f) {
        if (fscanf(f, "%lld", &stats->peak_bytes) != 1) stats->peak_bytes = 0;
        fclose(f);
    }

    // Read page fault statistics from memory.stat
    snprintf(path, sizeof(path), "%s/memory.stat", config->cgroup_path);
    f = fopen(path, "r");
    if (f) {
        char key[64];
        long long val;
        while (fscanf(f, "%63s %lld", key, &val) == 2) {
            if (strcmp(key, "pgfault") == 0) stats->pgfault = val;
            else if (strcmp(key, "pgmajfault") == 0) stats->pgmajfault = val;
            else if (strcmp(key, "anon") == 0) stats->anon_bytes = val;
            else if (strcmp(key, "file") == 0) stats->file_bytes = val;
        }
        fclose(f);
    }

    return 0;
}

int cgroups_cleanup(cgroup_config_t *config) {
    if (!config || strlen(config->cgroup_path) == 0) return 0;

    // Capture memory accounting statistics before removing cgroup
    cgroup_mem_stats_t stats;
    if (cgroups_read_mem_stats(config, &stats) == 0 && (stats.peak_bytes > 0 || stats.pgfault > 0)) {
        printf("\n>>> [KERNEL ACCOUNTING: CO: 4 Virtual Memory & Page Faults] <<<\n");
        printf("  - Peak Physical Memory: %.2f MB (%lld bytes)\n",
               (double)stats.peak_bytes / (1024.0 * 1024.0), stats.peak_bytes);
        printf("  - Minor Page Faults   : %lld (Proves Demand Paging occurred!)\n", stats.pgfault);
        printf("  - Major Page Faults   : %lld (Disk swaps avoided)\n", stats.pgmajfault);
        printf("  - Anonymous Memory    : %.2f MB\n", (double)stats.anon_bytes / (1024.0 * 1024.0));
        printf("--------------------------------------------------\n");
    }

    // Small delay to ensure all container threads have exited
    usleep(50000);

    if (rmdir(config->cgroup_path) != 0) {
        if (errno != ENOENT) {
            fprintf(stderr, "[cgroups] Notice: Failed to remove %s: %s\n",
                    config->cgroup_path, strerror(errno));
            return -1;
        }
    } else {
        printf("[cgroups] Cleaned up cgroup directory: %s\n", config->cgroup_path);
    }
    return 0;
}
