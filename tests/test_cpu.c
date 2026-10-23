#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
    int duration_sec = 5;
    if (argc > 1) {
        duration_sec = atoi(argv[1]);
    }

    printf("[test_cpu] Running intensive CPU calculation for %d seconds...\n", duration_sec);
    time_t start = time(NULL);
    clock_t start_clock = clock();

    volatile unsigned long long count = 0;
    while (time(NULL) - start < duration_sec) {
        count++;
    }

    clock_t end_clock = clock();
    double cpu_time_used = ((double)(end_clock - start_clock)) / CLOCKS_PER_SEC;

    printf("[test_cpu] Wall-clock time : %d seconds\n", duration_sec);
    printf("[test_cpu] CPU time used   : %.2f seconds\n", cpu_time_used);
    printf("[test_cpu] Effective CPU %% : %.1f%%\n", (cpu_time_used / duration_sec) * 100.0);
    return 0;
}
