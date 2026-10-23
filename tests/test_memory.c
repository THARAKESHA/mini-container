#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
    int target_mb = 100;
    if (argc > 1) {
        target_mb = atoi(argv[1]);
    }

    printf("[test_memory] Target allocation: %d MB\n", target_mb);
    printf("[test_memory] Allocating in chunks of 5 MB...\n");

    int chunk_size = 5 * 1024 * 1024; // 5 MB
    int total_allocated = 0;

    for (int i = 1; i <= target_mb / 5; i++) {
        char *ptr = (char *)malloc(chunk_size);
        if (!ptr) {
            printf("[test_memory] malloc failed at %d MB!\n", total_allocated);
            return 1;
        }

        // Write to every page to force physical memory page fault & commit
        memset(ptr, 0xAA, chunk_size);
        total_allocated += 5;
        printf("[test_memory] Successfully committed %d MB to physical RAM\n", total_allocated);
        usleep(100000); // 100ms pause to observe gradual consumption
    }

    printf("[test_memory] SUCCESS: Finished allocating %d MB without OOM kill.\n", total_allocated);
    return 0;
}
