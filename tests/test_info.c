#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/utsname.h>

int main(void) {
    printf("--- INSIDE CONTAINER INSPECTION ---\n");
    printf("Process PID : %d (Notice: In isolated PID namespace, container init is PID 1 or small)\n", getpid());
    printf("Parent PID  : %d\n", getppid());
    printf("User UID    : %d\n", getuid());

    struct utsname uts;
    if (uname(&uts) == 0) {
        printf("Hostname    : %s\n", uts.nodename);
        printf("Kernel      : %s %s\n", uts.sysname, uts.release);
    }

    printf("\nRunning 'ps -ef' or reading /proc/self:\n");
    FILE *f = fopen("/proc/self/status", "r");
    if (f) {
        char line[256];
        int count = 0;
        while (fgets(line, sizeof(line), f) && count < 8) {
            printf("  %s", line);
            count++;
        }
        fclose(f);
    } else {
        printf("  /proc not mounted or inaccessible.\n");
    }
    printf("------------------------------------\n");
    return 0;
}
