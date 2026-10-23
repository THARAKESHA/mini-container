# Mini-Container: A Lightweight Linux Container Runtime from Scratch in C

A minimalist, high-performance container virtualization engine implemented from scratch in **C99** using native Linux kernel subsystems: **Namespaces**, **Cgroups v2**, **chroot**, and **virtual filesystems (VFS)**.

This project was built to explore operating system kernel mechanisms, process isolation, CPU scheduling, concurrency synchronization, virtual memory demand paging, and container virtualization without relying on third-party runtime dependencies like Docker, containerd, or runc.

---

## 🎯 Syllabus & Course Outcomes (CO: 1 to CO: 5) Alignment

| Course Outcome (CO) | Topic Covered | Implementation Mechanism in Code |
| :--- | :--- | :--- |
| **CO 1: OS Principles & Processes** | System calls, Protection modes, PCB, Process creation & lifecycles | `clone()`, `execvp()`, `waitpid()`, custom child stack allocation |
| **CO 2: CPU Scheduling** | Preemption, Scheduling quotas, Proportional Fair Share | Linux Cgroups v2 `cpu.max` (CFS quotas) & `cpu.weight` (800 vs 200 contest) |
| **CO 3: Concurrency & IPC** | Synchronization primitives, Semaphores, Inter-Process Communication | POSIX `pipe()` barrier, Producer-Consumer with `sem_t` and shared memory (`mmap`) |
| **CO 4: Memory Management** | Main memory allocation, Virtual memory ceilings, Page faults, Demand paging | Linux Cgroups v2 `memory.max`, `pgfault` accounting (7,705 page faults logged), OOM Killer |
| **CO 5: Virtualization & File Systems** | Container virtualization, Namespaces, Mount propagation, Private `/proc` | `CLONE_NEWPID`, `CLONE_NEWUTS`, `CLONE_NEWNS`, `CLONE_NEWIPC`, `chroot()`, private `/proc` VFS |

---

## 🏛️ System Architecture

```
User Command:
sudo ./minicontainer run --memory 30M --cpu 40 --pids 10 ./tests/test_memory 60
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ Parent Process (Host Context)                               │
│ 1. Allocates 1MB isolated stack for child                   │
│ 2. Creates UNIX synchronization pipe (sync_pipe)            │
│ 3. Invokes clone() system call with namespace flags:        │
│    - CLONE_NEWPID (Process ID isolation)                    │
│    - CLONE_NEWUTS (Hostname isolation)                      │
│    - CLONE_NEWNS  (Mount table isolation)                   │
│    - CLONE_NEWIPC (Inter-process comm isolation)            │
│ 4. Sets up /sys/fs/cgroup/minicontainer-[PID]:              │
│    - memory.max = 31457280 bytes (30MB)                     │
│    - cpu.max    = 40000 100000 (40% CFS Quota)              │
│    - pids.max   = 10                                        │
│    - cgroup.procs <- child PID                              │
│ 5. Signals child via pipe and waits via waitpid()           │
│ 6. Reads memory.stat (Page Faults, Peak RAM) on exit        │
└──────────────────────────────┬──────────────────────────────┘
                               │ (Sync Pipe Barrier)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ Child Process (Container Sandbox Context)                   │
│ 1. Blocks on sync pipe until parent applies cgroup rules    │
│ 2. Sets UTS hostname (sethostname)                          │
│ 3. Enforces MS_PRIVATE mount propagation                    │
│ 4. If rootfs is provided: chroot() & mounts private /proc   │
│ 5. Executes payload via execvp() (Becomes PID 1)            │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start & Demonstration Options

### Option 1: Master Interactive Demonstration Menu (Recommended for Faculty)
Launch the colored, menu-driven interface:
```bash
sudo bash interactive_menu.sh
```
This presents a menu to trigger each test individually with single-key selection:
```text
  [1] Process & Hostname Isolation (CO: 1 & CO: 5)
  [2] Virtual Memory Boundary, Page Faults & OOM Killer (CO: 4)
  [3] CPU Quota & CFS Scheduling Throttling (CO: 2)
  [4] Proportional Fair-Share CPU Contest - 2 Containers (CO: 2)
  [5] Concurrency, Semaphores & Shared Memory IPC (CO: 3)
  [6] Process Table Exhaustion & Fork Bomb Defense (CO: 1 & CO: 3)
  [7] Launch Interactive Alpine Linux Container Shell (CO: 5)
  [8] Live Real-Time Kernel Resource Dashboard (CO: 2 & CO: 4)
  [9] Run Full Automated 5-in-1 Evaluation Demo Suite
  [0] Exit
```

### Option 2: Automated 5-in-1 Evaluation Suite
```bash
sudo bash scripts/run_demo.sh
```

### Option 3: Proportional CPU Fair-Share Contest (CO: 2)
```bash
sudo bash scripts/test_cpu_shares.sh
```

### Option 4: Real-Time Kernel Resource Dashboard
```bash
sudo bash scripts/monitor.sh
```

---

## 🧪 Detailed Test Scenarios & Empirical Results

### 1. PID & Hostname Isolation (CO: 1 & CO: 5)
```bash
sudo ./minicontainer run --hostname isolated-node ./tests/test_info
```
* **Observed:** The process reports `PID = 1` inside its namespace. Host processes are completely invisible. Host hostname remains unchanged.

### 2. Memory Boundary, Demand Paging & Kernel OOM Killer (CO: 4)
```bash
sudo ./minicontainer run --memory 30M ./tests/test_memory 60
```
* **Observed:** The test allocates memory in 5MB chunks and touches each page with `memset()`. Once allocations cross 30MB, the Linux kernel Out-Of-Memory (OOM) Killer dispatches `SIGKILL (signal 9)`.
* **Kernel Accounting Output:**
  ```text
  >>> [KERNEL ACCOUNTING: CO: 4 Virtual Memory & Page Faults] <<<
    - Peak Physical Memory: 30.00 MB (31457280 bytes)
    - Minor Page Faults   : 7705 (Proves Demand Paging occurred!)
    - Major Page Faults   : 1 (Disk swaps avoided)
  ```

### 3. CPU Scheduling Throttling (CO: 2)
```bash
sudo ./minicontainer run --cpu 40 ./tests/test_cpu 3
```
* **Observed:** An infinite compute loop executes for 3 seconds. The CFS scheduler clamps the CPU usage precisely at ~37-39%.

### 4. Proportional Fair-Share CPU Contest (CO: 2)
```bash
sudo bash scripts/test_cpu_shares.sh
```
* **Observed:** Two concurrent containers on CPU Core 0 with weights 800 vs 200 achieved **2.78s vs 0.69s** of CPU time (an exact **4.02 : 1** execution ratio).

### 5. Classical Concurrency & Semaphores (CO: 3)
```bash
sudo ./minicontainer run ./tests/test_ipc_sync
```
* **Observed:** Producer-Consumer synchronization executed using POSIX Semaphores (`sem_t`) and shared memory (`mmap`) with zero race conditions.

### 6. Process Table Exhaustion (Fork Bomb) Defense (CO: 1 & CO: 3)
```bash
sudo ./minicontainer run --pids 10 ./tests/test_forkbomb 50
```
* **Observed:** Attempts to spawn 50 processes. At the 10th process, `fork()` fails with `EAGAIN: Resource temporarily unavailable (errno=11)`. The host system remains completely unaffected.

---

## 📁 Repository Structure

```
mini-container/
├── Makefile                 # Automated build script
├── README.md                # Technical documentation
├── PROJECT_REPORT.md        # Comprehensive academic project report
├── PROJECT_REPORT.pdf       # Printable formal academic report (PDF)
├── presentation.html        # Interactive slide deck for project review
├── presentation.pdf         # Printable slide deck (PDF)
├── interactive_menu.sh      # Master menu-driven demonstration interface
├── scripts/
│   ├── setup_rootfs.sh      # Alpine minirootfs fetcher
│   ├── run_demo.sh          # 5-in-1 automated evaluation script
│   ├── test_cpu_shares.sh   # Proportional fair-share CPU contest
│   └── monitor.sh           # Real-time ASCII cgroups resource monitor
├── src/
│   ├── main.c               # CLI parser & orchestrator
│   ├── namespaces.h / .c    # Linux namespaces, clone(), and mount logic
│   └── cgroups.h / .c       # Cgroups v2 controllers & memory accounting
└── tests/
    ├── test_info.c          # Container namespace inspection
    ├── test_memory.c        # Memory allocation & OOM stress test
    ├── test_cpu.c           # CPU quota burner
    ├── test_ipc_sync.c      # Producer-Consumer with semaphores & shared memory
    └── test_forkbomb.c      # Safe process exhaustion test
```
