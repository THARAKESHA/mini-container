# MINI-CONTAINER: COMPREHENSIVE USER GUIDE & DEMONSTRATION MANUAL
**A Feature-by-Feature Technical Walkthrough with Exact Example Outputs, Syllabus Mapping, and Viva Scripts**

---

## TABLE OF CONTENTS
1. [Overview & Quick Reference](#1-overview--quick-reference)
2. [Feature 1: Process ID & Hostname Virtualization (CO: 1 & CO: 5)](#feature-1-process-id--hostname-virtualization-co-1--co-5)
3. [Feature 2: Virtual Memory Ceiling, Demand Paging & OOM Killer (CO: 4)](#feature-2-virtual-memory-ceiling-demand-paging--oom-killer-co-4)
4. [Feature 3: CPU Scheduling Bandwidth Quota Throttling (CO: 2)](#feature-3-cpu-scheduling-bandwidth-quota-throttling-co-2)
5. [Feature 4: Proportional Fair-Share CPU Scheduling Contest (CO: 2)](#feature-4-proportional-fair-share-cpu-scheduling-contest-co-2)
6. [Feature 5: Classical Concurrency, POSIX Semaphores & Shared Memory IPC (CO: 3)](#feature-5-classical-concurrency-posix-semaphores--shared-memory-ipc-co-3)
7. [Feature 6: Process Table Exhaustion & Fork Bomb Defense (CO: 1 & CO: 3)](#feature-6-process-table-exhaustion--fork-bomb-defense-co-1--co-3)
8. [Feature 7: Filesystem Sandboxing & Isolated Alpine Rootfs (CO: 5)](#feature-7-filesystem-sandboxing--isolated-alpine-rootfs-co-5)
9. [Feature 8: Real-Time Kernel Resource Dashboard (CO: 2 & CO: 4)](#feature-8-real-time-kernel-resource-dashboard-co-2--co-4)
10. [Feature 9: Master Interactive Menu (`interactive_menu.sh`)](#feature-9-master-interactive-menu-interactive_menush)

---

## 1. OVERVIEW & QUICK REFERENCE

| # | Feature Name | Core Mechanism | Syllabus Outcome | Demo Command |
|---|---|---|---|---|
| **1** | Process Isolation | `CLONE_NEWPID`, `CLONE_NEWUTS` | **CO: 1 & CO: 5** | `sudo ./minicontainer run --hostname isolated-box ./tests/test_info` |
| **2** | Memory & OOM Killer | `memory.max`, `memory.stat` | **CO: 4** | `sudo ./minicontainer run --memory 30M ./tests/test_memory 60` |
| **3** | CPU CFS Throttling | `cpu.max` (quota/period) | **CO: 2** | `sudo ./minicontainer run --cpu 40 ./tests/test_cpu 3` |
| **4** | Proportional CPU Shares | `cpu.weight` (800 vs 200) | **CO: 2** | `sudo bash scripts/test_cpu_shares.sh` |
| **5** | Concurrency & Semaphores | POSIX `sem_t`, `mmap` | **CO: 3** | `sudo ./minicontainer run ./tests/test_ipc_sync` |
| **6** | Fork Bomb Protection | `pids.max` | **CO: 1 & CO: 3** | `sudo ./minicontainer run --pids 10 ./tests/test_forkbomb 50` |
| **7** | Filesystem Sandboxing | `chroot()`, private `/proc` | **CO: 5** | `sudo ./minicontainer run --rootfs ./rootfs /bin/sh` |
| **8** | Live Kernel Dashboard | Cgroups v2 polling | **CO: 2 & CO: 4** | `sudo bash scripts/monitor.sh` |
| **9** | Interactive Menu | Multi-feature CLI UI | **All COs** | `sudo bash interactive_menu.sh` |

---

## FEATURE 1: Process ID & Hostname Virtualization (CO: 1 & CO: 5)

### Purpose
Demonstrates how the Linux kernel isolates the process hierarchy and system identity so that a containerized process cannot observe or interact with host processes.

### Command
```bash
sudo ./minicontainer run --hostname isolated-box ./tests/test_info
```

### Exact Output
```text
====================================================
       MINI-CONTAINER: Linux Sandbox Runtime         
  OS Isolation via Namespaces & Cgroups v2 in C      
====================================================
Container Configuration:
  Hostname   : isolated-box
  Rootfs     : (Host filesystem)
  Memory     : Unlimited
  CPU Quota  : Unlimited
  Max PIDs   : Unlimited
  Command    : ./tests/test_info
--------------------------------------------------
[container] Spawning child with namespaces (PID, UTS, NS, IPC)...
[container-child] Executing: ./tests/test_info (PID=1)
--- INSIDE CONTAINER INSPECTION ---
Process PID : 1 (Notice: In isolated PID namespace, container init is PID 1 or small)
Parent PID  : 0
User UID    : 0
Hostname    : isolated-box
Kernel      : Linux 6.18.33.1-microsoft-standard-WSL2

Running 'ps -ef' or reading /proc/self:
  Name:	test_info
  Umask:	0022
  State:	R (running)
  Tgid:	7826
  Ngid:	0
  Pid:	7826
  PPid:	7825
  TracerPid:	0
------------------------------------
[container] Child process spawned with Host PID: 7826
[cgroups] Configured cgroup path: /sys/fs/cgroup/minicontainer-7826
[cgroups] Assigned PID 7826 to cgroup.procs
[cgroups] Cleaned up cgroup directory: /sys/fs/cgroup/minicontainer-7826
--------------------------------------------------
[container] Container exited cleanly with code: 0
```

### What to Point Out to Evaluator:
1. **`PID = 1` vs Host PID `7826`:** Point out that inside the container, the process sees itself as `PID 1` (the init process of that namespace), while the host OS kernel tracks it as PID `7826`.
2. **`Hostname: isolated-box`:** Show that the hostname changed inside the container without affecting your host machine (`Tharakesha`).
3. **Syllabus Justification:** This satisfies **CO: 1 (Process creation & PCB)** and **CO: 5 (Container Virtualization & Namespaces)**.

---

## FEATURE 2: Virtual Memory Ceiling, Demand Paging & OOM Killer (CO: 4)

### Purpose
Proves how the operating system handles virtual memory boundaries, records demand page faults, and protects system stability via the kernel Out-Of-Memory (OOM) Killer.

### Command
```bash
sudo ./minicontainer run --memory 30M ./tests/test_memory 60
```

### Exact Output
```text
====================================================
       MINI-CONTAINER: Linux Sandbox Runtime         
  OS Isolation via Namespaces & Cgroups v2 in C      
====================================================
Container Configuration:
  Hostname   : container-box
  Rootfs     : (Host filesystem)
  Memory     : 30.00 MB
  CPU Quota  : Unlimited
  Max PIDs   : Unlimited
  Command    : ./tests/test_memory
--------------------------------------------------
[container] Spawning child with namespaces (PID, UTS, NS, IPC)...
[container-child] Executing: ./tests/test_memory (PID=1)
[test_memory] Target allocation: 60 MB
[test_memory] Allocating in chunks of 5 MB...
[test_memory] Successfully committed 5 MB to physical RAM
[test_memory] Successfully committed 10 MB to physical RAM
[test_memory] Successfully committed 15 MB to physical RAM
[test_memory] Successfully committed 20 MB to physical RAM
[test_memory] Successfully committed 25 MB to physical RAM
[container] Child process spawned with Host PID: 7828
[cgroups] Configured cgroup path: /sys/fs/cgroup/minicontainer-7828
[cgroups] Assigned PID 7828 to cgroup.procs
[cgroups] Memory limit applied: 31457280 bytes (30.00 MB)

>>> [KERNEL ACCOUNTING: CO: 4 Virtual Memory & Page Faults] <<<
  - Peak Physical Memory: 30.00 MB (31457280 bytes)
  - Minor Page Faults   : 7705 (Proves Demand Paging occurred!)
  - Major Page Faults   : 1 (Disk swaps avoided)
  - Anonymous Memory    : 0.00 MB
--------------------------------------------------
[cgroups] Cleaned up cgroup directory: /sys/fs/cgroup/minicontainer-7828
--------------------------------------------------
[container] Container terminated by signal: 9 (Killed)
[container] Notice: SIGKILL received. If memory limit was set, this indicates OS Out-Of-Memory (OOM) Killer!
```

### What to Point Out to Evaluator:
1. **Gradual Allocation Stopping at 25MB:** The program requests 60MB, but the container enforces a strict 30MB limit (`memory.max = 31457280`).
2. **`Minor Page Faults: 7705`:** Explain that when `malloc()` is called, Linux doesn't allocate physical RAM immediately (optimistic overcommit). When `memset()` writes bytes, 7,705 page faults occur to bring physical pages into memory.
3. **`Signal: 9 (Killed)`:** When memory crossed 30MB with swap disabled (`memory.swap.max = 0`), the Linux kernel OOM Killer dispatched an uncatchable `SIGKILL`.
4. **Syllabus Justification:** Directly proves **CO: 4 (Main Memory, Virtual Memory, Demand Paging, Page Faults, and Thrashing Protection)**.

---

## FEATURE 3: CPU Scheduling Bandwidth Quota Throttling (CO: 2)

### Purpose
Demonstrates how the Linux Completely Fair Scheduler (CFS) enforces deterministic CPU bandwidth caps over time windows.

### Command
```bash
sudo ./minicontainer run --cpu 40 ./tests/test_cpu 3
```

### Exact Output
```text
====================================================
       MINI-CONTAINER: Linux Sandbox Runtime         
  OS Isolation via Namespaces & Cgroups v2 in C      
====================================================
Container Configuration:
  Hostname   : container-box
  Rootfs     : (Host filesystem)
  Memory     : Unlimited
  CPU Quota  : 40%
  Max PIDs   : Unlimited
  Command    : ./tests/test_cpu
--------------------------------------------------
[container] Spawning child with namespaces (PID, UTS, NS, IPC)...
[container-child] Executing: ./tests/test_cpu (PID=1)
[test_cpu] Running intensive CPU calculation for 3 seconds...
[test_cpu] Wall-clock time : 3 seconds
[test_cpu] CPU time used   : 1.12 seconds
[test_cpu] Effective CPU % : 37.4%
[container] Child process spawned with Host PID: 3694
[cgroups] Configured cgroup path: /sys/fs/cgroup/minicontainer-3694
[cgroups] Assigned PID 3694 to cgroup.procs
[cgroups] CPU quota applied: 40% (40000 us / 100000 us)
[cgroups] Cleaned up cgroup directory: /sys/fs/cgroup/minicontainer-3694
--------------------------------------------------
[container] Container exited cleanly with code: 0
```

### What to Point Out to Evaluator:
1. **The Numbers:** Over 3 seconds of wall-clock time, the CPU-intensive infinite loop only received **1.12 seconds** of CPU compute time.
2. **`Effective CPU % : 37.4%`:** The cgroup CFS quota (`40000 us / 100000 us`) clamped execution right at the 40% ceiling.
3. **Syllabus Justification:** Demonstrates **CO: 2 (Preemptive CPU Scheduling & Bandwidth Quotas)**.

---

## FEATURE 4: Proportional Fair-Share CPU Scheduling Contest (CO: 2)

### Purpose
Demonstrates weighted fair queuing and proportional CPU time partitioning between competing workloads on the same CPU core.

### Command
```bash
sudo bash scripts/test_cpu_shares.sh
```

### Exact Output
```text
=================================================================
  CO: 2 CPU SCHEDULING: PROPORTIONAL FAIR-SHARE CONTEST          
  Comparing 2 Concurrent Containers with CFS Weights 800 vs 200  
=================================================================
Experiment Design:
  - Container A : CPU Weight 800 (High Share ~ 80%)
  - Container B : CPU Weight 200 (Low Share  ~ 20%)
  - Both run 100% compute loops simultaneously pinned to CPU 0
-----------------------------------------------------------------
Containers running concurrently on Core 0 (PIDs: 7898, 7899)...

>>> RESULTS & OBSERVATIONS <<<
Container A (Weight 800) CPU Time : 2.78 seconds
Container B (Weight 200) CPU Time : 0.69 seconds

Summary:
  Container A received significantly more scheduling slices than Container B,
  validating Linux CFS Proportional Share CPU Scheduling (CO: 2)!
```

### What to Point Out to Evaluator:
1. **The Exact 4:1 Ratio:**
   $$\frac{\text{Container A CPU Time}}{\text{Container B CPU Time}} = \frac{2.78}{0.69} = \mathbf{4.02 : 1}$$
   This matches the theoretical $\frac{800}{200} = \mathbf{4 : 1}$ weight ratio with 99.5% accuracy!
2. **CPU Pinning (`taskset -c 0`):** Both containers were forced to compete on the exact same core (Core 0), proving that the OS scheduler dynamically partitioned scheduling slices according to their priority weights.
3. **Syllabus Justification:** Concretely proves **CO: 2 (Priority Scheduling & Multiprocessor Fair Sharing)**.

---

## FEATURE 5: Classical Concurrency, POSIX Semaphores & Shared Memory IPC (CO: 3)

### Purpose
Demonstrates process synchronization, mutual exclusion, and Inter-Process Communication (IPC) by solving the classic Producer-Consumer problem inside an isolated container sandbox.

### Command
```bash
sudo ./minicontainer run --hostname ipc-box ./tests/test_ipc_sync
```

### Exact Output
```text
====================================================
       MINI-CONTAINER: Linux Sandbox Runtime         
  OS Isolation via Namespaces & Cgroups v2 in C      
====================================================
Container Configuration:
  Hostname   : ipc-box
  Rootfs     : (Host filesystem)
  Memory     : Unlimited
  CPU Quota  : Unlimited
  Max PIDs   : Unlimited
  Command    : ./tests/test_ipc_sync
--------------------------------------------------
[container] Spawning child with namespaces (PID, UTS, NS, IPC)...
[container-child] Executing: ./tests/test_ipc_sync (PID=1)
============================================================
  CO: 3 CONCURRENCY & SYNCHRONIZATION TEST (Producer-Consumer)
  Primitives: POSIX Semaphores (sem_t) + Shared Memory (mmap)
============================================================
[Sync] Buffer capacity: 5 slots | Total operations: 10 items

[Producer PID 1] --> Produced item: 10 (at buffer index 0)
  [Consumer PID 2] <-- Consumed item: 10 (from buffer index 0)
[Producer PID 1] --> Produced item: 20 (at buffer index 1)
  [Consumer PID 2] <-- Consumed item: 20 (from buffer index 1)
[Producer PID 1] --> Produced item: 30 (at buffer index 2)
  [Consumer PID 2] <-- Consumed item: 30 (from buffer index 2)
[Producer PID 1] --> Produced item: 40 (at buffer index 3)
  [Consumer PID 2] <-- Consumed item: 40 (from buffer index 3)
[Producer PID 1] --> Produced item: 50 (at buffer index 4)
  [Consumer PID 2] <-- Consumed item: 50 (from buffer index 4)
[Producer PID 1] --> Produced item: 60 (at buffer index 0)
  [Consumer PID 2] <-- Consumed item: 60 (from buffer index 0)
[Producer PID 1] --> Produced item: 70 (at buffer index 1)
  [Consumer PID 2] <-- Consumed item: 70 (from buffer index 1)
[Producer PID 1] --> Produced item: 80 (at buffer index 2)
  [Consumer PID 2] <-- Consumed item: 80 (from buffer index 2)
[Producer PID 1] --> Produced item: 90 (at buffer index 3)
  [Consumer PID 2] <-- Consumed item: 90 (from buffer index 3)
[Producer PID 1] --> Produced item: 100 (at buffer index 4)
  [Consumer PID 2] <-- Consumed item: 100 (from buffer index 4)

[Sync] SUCCESS: All 10 items produced and consumed without race conditions!
[Sync] Synchronization Primitives (Semaphores & Mutex) verified.
[container] Child process spawned with Host PID: 7832
[cgroups] Configured cgroup path: /sys/fs/cgroup/minicontainer-7832
[cgroups] Assigned PID 7832 to cgroup.procs
[cgroups] Cleaned up cgroup directory: /sys/fs/cgroup/minicontainer-7832
--------------------------------------------------
[container] Container exited cleanly with code: 0
```

### What to Point Out to Evaluator:
1. **Three Semaphores Used:**
   - `sem_t mutex`: Binary semaphore for critical section protection.
   - `sem_t empty_slots`: Counting semaphore initialized to 5.
   - `sem_t full_slots`: Counting semaphore initialized to 0.
2. **IPC Memory Mapping:** Allocated using `mmap(..., MAP_SHARED | MAP_ANONYMOUS, ...)`.
3. **Circular Ring Buffer:** Shows indices wrapping around from index 4 back to index 0 smoothly.
4. **Syllabus Justification:** Validates **CO: 3 (Concurrency, Synchronization Primitives, Semaphores, IPC in UNIX)**.

---

## FEATURE 6: Process Table Exhaustion & Fork Bomb Defense (CO: 1 & CO: 3)

### Purpose
Demonstrates how the runtime protects the operating system against Denial of Service (DoS) attacks and process table exhaustion.

### Command
```bash
sudo ./minicontainer run --pids 10 ./tests/test_forkbomb 50
```

### Exact Output
```text
====================================================
       MINI-CONTAINER: Linux Sandbox Runtime         
  OS Isolation via Namespaces & Cgroups v2 in C      
====================================================
Container Configuration:
  Hostname   : container-box
  Rootfs     : (Host filesystem)
  Memory     : Unlimited
  CPU Quota  : Unlimited
  Max PIDs   : 10
  Command  : ./tests/test_forkbomb
--------------------------------------------------
[container] Spawning child with namespaces (PID, UTS, NS, IPC)...
[container-child] Executing: ./tests/test_forkbomb (PID=1)
[test_forkbomb] Attempting to spawn 50 child processes...
[test_forkbomb] Successfully spawned child process 1 (PID=2)
[test_forkbomb] Successfully spawned child process 2 (PID=3)
[test_forkbomb] Successfully spawned child process 3 (PID=4)
[test_forkbomb] Successfully spawned child process 4 (PID=5)
[test_forkbomb] Successfully spawned child process 5 (PID=6)
[test_forkbomb] Successfully spawned child process 6 (PID=7)
[test_forkbomb] Successfully spawned child process 7 (PID=8)
[test_forkbomb] Successfully spawned child process 8 (PID=9)
[test_forkbomb] Successfully spawned child process 9 (PID=10)
[test_forkbomb] Fork blocked at process #10! Error: Resource temporarily unavailable (errno=11)
[test_forkbomb] Cgroup pids.max protection successfully prevented resource exhaustion!
[test_forkbomb] Cleaning up 9 spawned processes...
[test_forkbomb] Completed.
[container] Child process spawned with Host PID: 7835
[cgroups] Configured cgroup path: /sys/fs/cgroup/minicontainer-7835
[cgroups] Assigned PID 7835 to cgroup.procs
[cgroups] Process limit (pids.max) applied: 10
[cgroups] Cleaned up cgroup directory: /sys/fs/cgroup/minicontainer-7835
--------------------------------------------------
[container] Container exited cleanly with code: 0
```

### What to Point Out to Evaluator:
1. **The Block at Process #10:** The container limit was set to `--pids 10`. Children 1 through 9 spawned (reaching 10 total active tasks including the parent).
2. **`errno = 11 (EAGAIN)`:** When the 10th child attempted `fork()`, the kernel intercepted the call and returned `Resource temporarily unavailable`.
3. **Host Safety:** While a fork bomb would freeze an unconfined machine, the host system remained 100% responsive.
4. **Syllabus Justification:** Validates **CO: 1 (Process creation & limits)** and **CO: 3 (Deadlocks & Resource Exhaustion)**.

---

## FEATURE 7: Filesystem Sandboxing & Isolated Alpine Rootfs (CO: 5)

### Purpose
Demonstrates how the container isolates storage and directory structures so that containerized software cannot inspect or mutate host operating system files.

### Command
```bash
sudo ./minicontainer run --hostname alpine-node --rootfs ./rootfs /bin/sh
```

### Exact Interactive Session
```text
====================================================
       MINI-CONTAINER: Linux Sandbox Runtime         
  OS Isolation via Namespaces & Cgroups v2 in C      
====================================================
Container Configuration:
  Hostname   : alpine-node
  Rootfs     : ./rootfs
  Memory     : Unlimited
  CPU Quota  : Unlimited
  Max PIDs   : Unlimited
  Command    : /bin/sh
--------------------------------------------------
[container] Spawning child with namespaces (PID, UTS, NS, IPC)...
[container-child] Executing: /bin/sh (PID=1)
/ # hostname
alpine-node
/ # ps aux
PID   USER     TIME  COMMAND
    1 0         0:00 /bin/sh
    2 0         0:00 ps aux
/ # ls -l /
total 48
drwxr-xr-x    2 0        0             4096 Jun  5 01:12 bin
drwxr-xr-x    2 0        0             4096 Jun  5 01:12 dev
drwxr-xr-x   15 0        0             4096 Jun  5 01:12 etc
drwxr-xr-x    2 0        0             4096 Jun  5 01:12 home
drwxr-xr-x    5 0        0             4096 Jun  5 01:12 lib
dr-xr-xr-x   13 0        0                0 Oct 23 15:10 proc
drwx------    2 0        0             4096 Jun  5 01:12 root
drwxr-xr-x    2 0        0             4096 Jun  5 01:12 sys
drwxrwxrwt    2 0        0             4096 Jun  5 01:12 tmp
drwxr-xr-x    7 0        0             4096 Jun  5 01:12 usr
drwxr-xr-x   11 0        0             4096 Jun  5 01:12 var
/ # exit
[cgroups] Cleaned up cgroup directory: /sys/fs/cgroup/minicontainer-491
--------------------------------------------------
[container] Container exited cleanly with code: 0
```

### What to Point Out to Evaluator:
1. **Interactive Shell:** You are running an actual Busybox shell inside an isolated root filesystem.
2. **`ps aux` Isolation:** Running `ps aux` only shows `PID 1 (/bin/sh)` and `PID 2 (ps aux)`. The host machine's background services and processes are completely invisible because `/proc` is private.
3. **File Sandboxing:** Files created here exist solely inside `./rootfs` and cannot tamper with the host Windows or WSL filesystems.
4. **Syllabus Justification:** Validates **CO: 5 (Virtualization, Filesystem Interfaces, and VFS Mounts)**.

---

## FEATURE 8: Real-Time Kernel Resource Dashboard (CO: 2 & CO: 4)

### Purpose
Provides a live visual monitor of active container cgroup parameters, memory utilization bars, and page fault counters directly from kernel memory.

### Command
```bash
sudo bash scripts/monitor.sh
```

### Exact Output
```text
==================================================================
          MINI-CONTAINER REAL-TIME KERNEL DASHBOARD               
  Live Monitoring of Linux Cgroups v2 Resource Accounting         
==================================================================

┌─────────────────────────────────────────────────────────────┐
│ Container ID: minicontainer-8120  (Host PID: 8120)          │
├─────────────────────────────────────────────────────────────┤
│ Memory Usage   : [████████████░░░] 25 MB / 30 MB ( 83%)     │
│ Minor PgFaults : 6400 (Proves Demand Paging)                │
│ Major PgFaults : 0 (Page Faults requiring disk I/O)         │
│ Anonymous RAM  : 25 MB                                      │
│ CPU CFS Quota  : 50000 100000 us (period)                   │
│ Active Tasks   : 1 / 10 max                                 │
└─────────────────────────────────────────────────────────────┘
```

### What to Point Out to Evaluator:
1. **Real-Time ASCII Progress Bar:** Visually depicts memory consumption nearing the 30MB limit.
2. **Dynamic Polling:** Directly reads `/sys/fs/cgroup/minicontainer-[PID]/memory.current` and `memory.stat`.
3. **Demand Paging Counter:** Minor page faults show how many MMU traps were resolved without disk I/O.

---

## FEATURE 9: Master Interactive Menu (`interactive_menu.sh`)

### Purpose
Gives you a clean, bulletproof interface to trigger any test on demand during your project review without memorizing long terminal commands.

### Command
```bash
sudo bash interactive_menu.sh
```

### Screen Interface
```text
========================================================================
        MINI-CONTAINER: OPERATING SYSTEMS PROJECT DEMONSTRATION         
        Covering Course Outcomes: CO: 1, CO: 2, CO: 3, CO: 4, CO: 5     
========================================================================

  [1] Process & Hostname Isolation (CO: 1 & CO: 5 Namespaces)
  [2] Virtual Memory Boundary, Page Faults & OOM Killer (CO: 4)
  [3] CPU Quota & CFS Scheduling Throttling (CO: 2)
  [4] Proportional Fair-Share CPU Contest - 2 Containers (CO: 2)
  [5] Concurrency, Semaphores & Shared Memory IPC (CO: 3)
  [6] Process Table Exhaustion & Fork Bomb Defense (CO: 1 & CO: 3)
  [7] Launch Interactive Alpine Linux Container Shell (CO: 5 Rootfs)
  [8] Live Real-Time Kernel Resource Dashboard (CO: 2 & CO: 4)
  [9] Run Full Automated 5-in-1 Evaluation Demo Suite
  [0] Exit
------------------------------------------------------------------------
Select an option [0-9]:
```

### How to Use During Review:
* When the teacher says: *"Show me CPU scheduling"* $\rightarrow$ Press **`3`** or **`4`**.
* When the teacher says: *"Show me memory management"* $\rightarrow$ Press **`2`**.
* When the teacher says: *"Show me concurrency or semaphores"* $\rightarrow$ Press **`5`**.
* When the teacher says: *"Show me container shell"* $\rightarrow$ Press **`7`**.
* When the teacher says: *"Show me everything"* $\rightarrow$ Press **`9`**.
