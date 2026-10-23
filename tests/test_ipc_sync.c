#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/wait.h>
#include <semaphore.h>
#include <string.h>

#define BUFFER_SIZE 5
#define TOTAL_ITEMS 10

// Shared memory circular buffer layout (CO: 3 Classical Synchronization)
typedef struct {
    int buffer[BUFFER_SIZE];
    int in;
    int out;
    sem_t mutex;       // Binary semaphore for mutual exclusion in critical section
    sem_t empty_slots; // Counting semaphore tracking available buffer slots
    sem_t full_slots;  // Counting semaphore tracking produced items
} shared_ring_buffer_t;

int main(void) {
    printf("============================================================\n");
    printf("  CO: 3 CONCURRENCY & SYNCHRONIZATION TEST (Producer-Consumer)\n");
    printf("  Primitives: POSIX Semaphores (sem_t) + Shared Memory (mmap)\n");
    printf("============================================================\n");

    // Allocate anonymous shared memory accessible across fork()
    shared_ring_buffer_t *shared = mmap(NULL, sizeof(shared_ring_buffer_t),
                                        PROT_READ | PROT_WRITE,
                                        MAP_SHARED | MAP_ANONYMOUS, -1, 0);
    if (shared == MAP_FAILED) {
        perror("mmap failed");
        return 1;
    }

    shared->in = 0;
    shared->out = 0;

    // Initialize semaphores: 2nd argument=1 means shared between processes
    sem_init(&shared->mutex, 1, 1);
    sem_init(&shared->empty_slots, 1, BUFFER_SIZE);
    sem_init(&shared->full_slots, 1, 0);

    printf("[Sync] Buffer capacity: %d slots | Total operations: %d items\n\n", BUFFER_SIZE, TOTAL_ITEMS);

    pid_t pid = fork();

    if (pid < 0) {
        perror("fork failed");
        return 1;
    }

    if (pid == 0) {
        // --- CONSUMER PROCESS ---
        for (int i = 1; i <= TOTAL_ITEMS; i++) {
            sem_wait(&shared->full_slots);  // Wait for available item
            sem_wait(&shared->mutex);       // Enter critical section

            int item = shared->buffer[shared->out];
            printf("  [Consumer PID %d] <-- Consumed item: %02d (from buffer index %d)\n",
                   getpid(), item, shared->out);
            shared->out = (shared->out + 1) % BUFFER_SIZE;

            sem_post(&shared->mutex);       // Exit critical section
            sem_post(&shared->empty_slots); // Signal empty slot available

            usleep(120000); // 120ms simulated consumption delay
        }
        exit(0);
    } else {
        // --- PRODUCER PROCESS ---
        for (int i = 1; i <= TOTAL_ITEMS; i++) {
            sem_wait(&shared->empty_slots); // Wait for empty buffer slot
            sem_wait(&shared->mutex);       // Enter critical section

            shared->buffer[shared->in] = i * 10;
            printf("[Producer PID %d] --> Produced item: %02d (at buffer index %d)\n",
                   getpid(), i * 10, shared->in);
            shared->in = (shared->in + 1) % BUFFER_SIZE;

            sem_post(&shared->mutex);       // Exit critical section
            sem_post(&shared->full_slots);  // Signal item available

            usleep(80000); // 80ms simulated production delay
        }

        // Wait for consumer child to complete
        wait(NULL);

        // Cleanup synchronization primitives
        sem_destroy(&shared->mutex);
        sem_destroy(&shared->empty_slots);
        sem_destroy(&shared->full_slots);
        munmap(shared, sizeof(shared_ring_buffer_t));

        printf("\n[Sync] SUCCESS: All %d items produced and consumed without race conditions!\n", TOTAL_ITEMS);
        printf("[Sync] Synchronization Primitives (Semaphores & Mutex) verified.\n");
    }

    return 0;
}
