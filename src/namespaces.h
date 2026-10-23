#ifndef NAMESPACES_H
#define NAMESPACES_H

#include "cgroups.h"
#include <sys/types.h>

typedef struct {
    char hostname[64];
    char rootfs[512];
    char **argv;
    int sync_pipe[2];
    cgroup_config_t cgroup_cfg;
} container_config_t;

// Launch the containerized process with isolated namespaces and cgroup boundaries
int container_run(container_config_t *config);

#endif // NAMESPACES_H
