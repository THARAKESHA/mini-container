#ifndef CGROUPS_H
#define CGROUPS_H

#include <sys/types.h>

typedef struct {
    long long memory_limit_bytes; // <= 0 means unlimited
    int cpu_percent;              // 1 to 100, 0 means unlimited
    int cpu_weight;               // 1 to 10000 (default 100, 0 means default)
    int max_pids;                 // <= 0 means unlimited
    char cgroup_path[256];
} cgroup_config_t;

// Structure to capture kernel memory statistics (CO: 4)
typedef struct {
    long long current_bytes;
    long long peak_bytes;
    long long pgfault;
    long long pgmajfault;
    long long anon_bytes;
    long long file_bytes;
} cgroup_mem_stats_t;

// Initialize and apply cgroup v2 resource limits for the target pid
int cgroups_setup(pid_t pid, cgroup_config_t *config);

// Read memory statistics from the cgroup
int cgroups_read_mem_stats(const cgroup_config_t *config, cgroup_mem_stats_t *stats);

// Clean up the created cgroup directory and print accounting summary
int cgroups_cleanup(cgroup_config_t *config);

#endif // CGROUPS_H
