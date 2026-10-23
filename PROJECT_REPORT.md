# PROJECT REPORT

## DESIGN AND IMPLEMENTATION OF A LIGHTWEIGHT LINUX CONTAINER RUNTIME FROM SCRATCH IN C
**A Systems-Level Exploration of OS Virtualization, Cgroups v2, Concurrency, and Memory Protection**

---

### Submitted in Partial Fulfillment of the Requirements for the Course
### **OPERATING SYSTEMS (CSE Core)**

**Team Members:**  
1. **Tharakesha M** (Reg No: **24BCE2538**)  
2. **Mathu Metha S** (Reg No: **24BCE2805**)  
**Department:** Department of Computer Science & Engineering  
**Academic Year:** 2026  

---

## CERTIFICATE

This is to certify that the project entitled **"DESIGN AND IMPLEMENTATION OF A LIGHTWEIGHT LINUX CONTAINER RUNTIME FROM SCRATCH IN C"** is a bonafide work carried out by **Tharakesha M (24BCE2538)** and **Mathu Metha S (24BCE2805)** in partial fulfillment of the academic requirements for the **Operating Systems** course.

---

## TABLE OF CONTENTS

1. **Abstract**
2. **Introduction & Motivation**
3. **Literature Survey: Containers vs. Virtual Machines**
4. **Course Outcomes (CO 1 to CO 5) Implementation Matrix**
5. **System Architecture & Kernel Primitives**
6. **Detailed Module Design & Algorithms**
   - 6.1 Process & Namespace Virtualization (CO: 1 & CO: 5)
   - 6.2 CPU Scheduling & Proportional Fair-Share Quotas (CO: 2)
   - 6.3 Concurrency, Shared Memory & Semaphores (CO: 3)
   - 6.4 Virtual Memory, Demand Paging & OOM Killer (CO: 4)
   - 6.5 Filesystem Sandboxing & Private VFS Mounts (CO: 5)
7. **Experimental Results & Empirical Validation**
8. **Comprehensive Viva Voce Question Bank (20 Q&A)**
9. **Conclusion & Future Work**
10. **References**

---

## 1. ABSTRACT

Modern cloud computing, microservices, and DevOps infrastructure depend fundamentally on container virtualization platforms such as Docker, containerd, and Kubernetes. However, container technologies are frequently perceived by students and developers as opaque "black boxes." 

This project demystifies containerization by designing, implementing, and empirically evaluating a standalone, lightweight container runtime named **`mini-container`**, engineered from scratch in **C99** with zero third-party dependencies. Leveraging native Linux kernel subsystems—specifically **Linux Namespaces** (`CLONE_NEWPID`, `CLONE_NEWUTS`, `CLONE_NEWNS`, `CLONE_NEWIPC`), **Unified Cgroups v2** (`memory.max`, `cpu.max`, `cpu.weight`, `pids.max`), and **VFS chroot sandboxing**—the runtime achieves full hardware-level resource confinement and process tree isolation.

The project explicitly models and validates all core course outcomes (CO: 1 through CO: 5) of the Operating Systems syllabus, including system call dispatch, Completely Fair Scheduling (CFS), POSIX semaphore synchronization, demand paging accounting (tracking minor/major page faults), and kernel Out-Of-Memory (OOM) Killer invocation.

---

## 2. INTRODUCTION & MOTIVATION

Operating systems serve as the intermediary layer between physical hardware and application workloads, managing CPU cycles, memory frames, file hierarchies, and I/O devices. 

In enterprise server environments, running untrusted or multi-tenant code requires strict execution sandboxing to prevent:
1. **Resource Starvation:** A buggy application consuming 100% of CPU or RAM, crashing adjacent host processes.
2. **Process Table Exhaustion:** Fork bomb attacks depleting the system Process Control Block (PCB) table.
3. **Privilege Leaks:** Unauthorized visibility or modification of host files and network interfaces.

While Virtual Machines (VMs) resolve these challenges via hardware emulation, they impose substantial memory footprint and latency overheads. This project demonstrates that a single Linux kernel can achieve robust multi-tenant sandboxing using lightweight kernel data structures, completing container creation and teardown in under 15 milliseconds.

---

## 3. LITERATURE SURVEY: CONTAINERS VS. VIRTUAL MACHINES

| Metric / Dimension | Traditional Virtual Machines (VMs) | Operating System Containers (mini-container) |
| :--- | :--- | :--- |
| **Virtualization Layer** | Hardware Level (Type-1 / Type-2 Hypervisor) | Kernel Level (Linux Namespaces & Cgroups) |
| **Guest OS Kernel** | Requires a dedicated, full guest OS kernel | Shares the single underlying host Linux kernel |
| **Boot-up Latency** | Tens of seconds to minutes | Sub-second (10 – 30 milliseconds) |
| **Memory Footprint** | Gigabytes (Guest kernel + Virtual memory overhead) | Megabytes (Confined purely to user processes) |
| **I/O & CPU Efficiency** | Incurs translation penalties (VT-x / AMD-V) | Near-native bare-metal execution speed |
| **Isolation Boundary** | Hardware abstraction / Hypervisor ring -1 | Software kernel data structures (`nsproxy`, `cgroup`) |

---

## 4. COURSE OUTCOMES (CO) IMPLEMENTATION MATRIX

The project maps directly to the five Course Outcomes of the syllabus:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      COURSE OUTCOMES MAPPING MATRIX                         │
├───────┬──────────────────────────┬──────────────────────────────────────────┤
│ CO ID │ Syllabus Topic           │ Implementation in mini-container         │
├───────┼──────────────────────────┼──────────────────────────────────────────┤
│ CO: 1 │ OS Principles & Process  │ clone() syscall with isolated stack;     │
│       │ Management               │ PCB management; waitpid() status checks. │
├───────┼──────────────────────────┼──────────────────────────────────────────┤
│ CO: 2 │ CPU Scheduling & CFS     │ cpu.max CFS bandwidth throttling;        │
│       │ Quotas                   │ cpu.weight proportional fair-share contest│
├───────┼──────────────────────────┼──────────────────────────────────────────┤
│ CO: 3 │ Concurrency, Semaphores  │ POSIX pipe parent-child barrier;         │
│       │ & UNIX IPC               │ Producer-Consumer with sem_t and mmap.   │
├───────┼──────────────────────────┼──────────────────────────────────────────┤
│ CO: 4 │ Memory Management,       │ memory.max ceiling; pgfault accounting;  │
│       │ Demand Paging & OOM      │ kernel OOM Killer SIGKILL intervention.  │
├───────┼──────────────────────────┼──────────────────────────────────────────┤
│ CO: 5 │ Virtualization, VFS &    │ CLONE_NEWNS mount propagation; chroot(); │
│       │ Filesystem Isolation     │ private /proc pseudo-filesystem mount.   │
└───────┴──────────────────────────┴──────────────────────────────────────────┘
```

---

## 5. SYSTEM ARCHITECTURE & KERNEL PRIMITIVES

The execution architecture follows a coordinated two-tier process lifecycle with an IPC synchronization barrier:

```
User CLI Command:
sudo ./minicontainer run --memory 30M --cpu 40 --pids 10 ./tests/test_memory 60
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. PARENT PROCESS (Host Environment)                                        │
│    - Allocates 1MB isolated child stack using malloc()                      │
│    - Initializes POSIX synchronization pipe (sync_pipe[2])                  │
│    - Dispatches clone(container_child, stack, CLONE_NEW* | SIGCHLD)         │
│    - Resolves Child PID (Host PID e.g., 7828)                               │
│    - Creates /sys/fs/cgroup/minicontainer-[PID]                             │
│    - Enforces: memory.max=30M, memory.swap.max=0, cpu.max=40000 100000     │
│    - Attaches Child PID to cgroup.procs                                     │
│    - Releases sync_pipe barrier by writing single trigger byte              │
│    - Enters waitpid() to block until child lifecycle concludes              │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ (IPC Barrier Synchronization)
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 2. CONTAINER CHILD PROCESS (Sandbox Environment)                            │
│    - Blocks on read(sync_pipe[0]) until parent completes cgroup binding     │
│    - Sets independent UTS Hostname via sethostname("isolated-box")          │
│    - Applies MS_PRIVATE mount propagation to decouple VFS hierarchy         │
│    - Executes chroot(rootfs) to cage file traversal                         │
│    - Mounts private /proc pseudo-filesystem (isolates process inspection)   │
│    - Invokes execvp() to overwrite address space (Becomes PID 1)            │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ (Process Exit / OOM Kill)
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 3. PARENT POST-EXECUTION ACCOUNTING & CLEANUP                               │
│    - Parses /sys/fs/cgroup/minicontainer-[PID]/memory.stat                  │
│    - Extracts and displays: Peak RAM, Minor Page Faults, Major Page Faults  │
│    - Evaluates WIFSIGNALED(status): detects OOM SIGKILL (signal 9)          │
│    - Removes cgroup directory via rmdir() and frees child stack             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. DETAILED MODULE DESIGN & ALGORITHMS

### 6.1 Process & Namespace Virtualization (CO: 1 & CO: 5)
Unlike standard `fork()`, which creates duplicate processes in identical kernel namespaces, `clone()` accepts bitwise flags that instruct the Linux kernel to instantiate fresh namespace objects:
- **`CLONE_NEWPID`:** Instantiates a new PID hierarchy where the child process registers as **`PID 1`** (container init).
- **`CLONE_NEWUTS`:** Virtualizes `nodename` and `domainname`, allowing container hostnames to change independently of the host.
- **`CLONE_NEWNS`:** Decouples the filesystem mount hierarchy from the host.
- **`CLONE_NEWIPC`:** Isolates POSIX message queues and System V IPC primitives.

### 6.2 CPU Scheduling & Proportional Fair-Share Quotas (CO: 2)
Linux Cgroups v2 manages CPU allocation using the Completely Fair Scheduler (CFS):
1. **CFS Bandwidth Ceiling (`cpu.max`):** Specifies an execution quota over a base period (e.g., `40000 100000` = 40% CPU). When the process exhausts its 40ms allocation within the 100ms window, the scheduler throttles the process.
2. **Proportional Fair Share (`cpu.weight`):** Implements weighted fair queuing. When multiple containers compete on the same CPU core, execution time is partitioned proportionally to their weights.

### 6.3 Concurrency, Shared Memory & Semaphores (CO: 3)
The project demonstrates classical concurrency by implementing the Producer-Consumer problem in shared memory:
- **`sem_t mutex`:** Binary semaphore enforcing mutual exclusion during buffer insertions/removals.
- **`sem_t empty_slots`:** Counting semaphore initialized to buffer capacity ($N=5$).
- **`sem_t full_slots`:** Counting semaphore initialized to 0.

### 6.4 Virtual Memory, Demand Paging & OOM Killer (CO: 4)
When memory is allocated via `malloc()`, Linux implements optimistic overcommit and demand paging:
1. Virtual address space is mapped without committing physical DRAM frames.
2. When pages are written to (`memset()`), page faults occur. The MMU raises a trap, causing the OS kernel to allocate physical page frames.
3. Cgroups v2 tracks these in `/sys/fs/cgroup/minicontainer-[PID]/memory.stat` under `pgfault`.
4. When total physical memory usage exceeds `memory.max`, the Linux kernel **Out-Of-Memory (OOM) Killer** is invoked, terminating the offending container with `SIGKILL (signal 9)`.

### 6.5 Filesystem Sandboxing & Private VFS Mounts (CO: 5)
To isolate file storage:
1. `mount(NULL, "/", NULL, MS_REC | MS_PRIVATE, NULL)` prevents mount events from propagating to the host.
2. `chroot(rootfs)` resets the root directory of the container process to an isolated directory tree.
3. `mount("proc", "/proc", "proc", 0, NULL)` mounts a private `procfs` reflecting only containerized processes.

---

## 7. EXPERIMENTAL RESULTS & EMPIRICAL VALIDATION

All test scenarios were executed and validated on Linux Kernel 6.18 (WSL2 / Ubuntu):

### Experiment 1: Process ID Virtualization (CO: 1 & CO: 5)
* **Host Environment:** 47 active processes, Hostname: `Tharakesha`.
* **Container Observation:** `PID = 1`, Parent PID = 0, Hostname = `isolated-box`. Host processes completely invisible.

### Experiment 2: Memory Ceiling, Demand Paging & OOM Killer (CO: 4)
* **Configuration:** `--memory 30M`, workload attempting to commit 60MB.
* **Observed Metrics:**
  - Peak Physical Memory: **30.00 MB** (100.0% utilization)
  - Minor Page Faults: **7,705** (Demand paging verified)
  - Major Page Faults: **1**
  - Termination: Process killed by **`SIGKILL (signal 9)`** by Linux OOM Killer.

### Experiment 3: CPU Scheduling Bandwidth Throttling (CO: 2)
* **Configuration:** `--cpu 40%` quota (40,000 us / 100,000 us).
* **Observed Metrics:** Infinite compute loop achieved **27.8% - 37.4%** effective CPU utilization, clamped deterministically by the CFS scheduler.

### Experiment 4: Proportional Fair-Share CPU Contest (CO: 2)
* **Configuration:** Container A (`cpu.weight 800`) vs Container B (`cpu.weight 200`) pinned to CPU Core 0.
* **Observed Metrics:**
  - Container A CPU Time: **2.78 seconds**
  - Container B CPU Time: **0.69 seconds**
  - **Ratio:** $2.78 / 0.69 \approx 4.02 : 1$ (Matches theoretical $800 : 200 = 4 : 1$ ratio with 99.5% accuracy).

### Experiment 5: Process Table Exhaustion & Fork Bomb Defense (CO: 1 & CO: 3)
* **Configuration:** `--pids 10`, attempting to spawn 50 processes.
* **Observed Metrics:** Children 1 through 9 spawned successfully. Process #10 was blocked by the kernel with **`EAGAIN: Resource temporarily unavailable (errno=11)`**. Host system remained completely responsive.

---

## 8. COMPREHENSIVE VIVA VOCE QUESTION BANK (20 Q&A)

### Q1: What is the fundamental difference between `fork()` and `clone()`?
> **Answer:** `fork()` creates an exact duplicate of the calling process inside the *same* namespaces and resource contexts. `clone()` accepts bitwise flags (`CLONE_NEWPID`, `CLONE_NEWUTS`, `CLONE_NEWNS`, `CLONE_NEWIPC`) and a user-provided stack, allowing the kernel to birth the child process inside brand-new, isolated namespaces.

### Q2: Why is container virtualization referred to as "OS-level virtualization"?
> **Answer:** Because there is no hypervisor or guest operating system. The single host Linux kernel provides virtualization by partitioning its internal kernel tables and data structures (namespaces and control groups).

### Q3: What is a Process Control Block (PCB) and how is it affected by PID namespaces?
> **Answer:** The PCB (represented by `struct task_struct` in Linux) contains process state, PID, priority, and parent links. With PID namespaces, a single process has two PIDs: a global PID in the host's root PID namespace (e.g., 7828) and a virtual local PID inside the container namespace (where it is `PID 1`).

### Q4: Why did `test_memory` trigger `SIGKILL` instead of `malloc()` returning `NULL`?
> **Answer:** Linux uses optimistic memory overcommit and demand paging. `malloc()` reserves virtual address space without allocating physical frames. When `memset()` accessed the pages, physical memory allocation hit `memory.max` with swap disabled. The kernel Out-Of-Memory (OOM) Killer intervened directly, dispatching `SIGKILL`.

### Q5: What is the purpose of the POSIX pipe between parent and child?
> **Answer:** It serves as a barrier synchronization mechanism (CO: 3). Without it, a race condition occurs where the child might execute `execvp()` before the parent finishes creating `/sys/fs/cgroup/minicontainer-[PID]` and attaching the child's PID to `cgroup.procs`.

### Q6: What are Minor Page Faults and Major Page Faults?
> **Answer:** A Minor Page Fault occurs when a virtual memory page is mapped to a physical RAM frame that is already present in memory without requiring disk I/O. A Major Page Fault occurs when the required page is not in memory and must be retrieved from secondary storage (swap or disk).

### Q7: How does Cgroups v2 differ from Cgroups v1?
> **Answer:** Cgroups v1 used separate, decoupled hierarchies for each resource controller (`/sys/fs/cgroup/cpu`, `/sys/fs/cgroup/memory`), causing synchronization and accounting conflicts. Cgroups v2 uses a single unified hierarchy where all controllers (`cpu`, `memory`, `pids`, `io`) operate on the same tree structure.

### Q8: What does `chroot()` do and why is it essential for containers?
> **Answer:** `chroot()` changes the perceived root directory (`/`) for the calling process and its descendants. It prevents container processes from navigating above the designated root filesystem into host system directories.

### Q9: Why is `mount(NULL, "/", NULL, MS_REC | MS_PRIVATE, NULL)` executed?
> **Answer:** In modern systemd environments, mounts default to `MS_SHARED`, which propagates mount and unmount events across namespaces. Setting `MS_PRIVATE` ensures container mounts (like `/proc`) remain private and do not alter the host filesystem.

### Q10: How does `pids.max` protect against a fork bomb?
> **Answer:** A fork bomb rapidly exhausts the kernel's process table by spawning exponential processes. Setting `pids.max = 10` enforces a hard ceiling on concurrent tasks. Once 10 tasks exist, subsequent `fork()` syscalls fail immediately with `EAGAIN`.

### Q11: How does Linux CFS throttle CPU usage with `cpu.max`?
> **Answer:** `cpu.max` takes two numbers: `quota` and `period` (e.g., `40000 100000`). If a process uses its 40,000 microseconds of CPU time before the 100,000 microsecond window concludes, CFS suspends the process from the runqueue until the next period begins.

### Q12: What is the difference between CPU Quota and CPU Weight?
> **Answer:** CPU Quota (`cpu.max`) sets a hard ceiling on CPU utilization regardless of whether the system is idle. CPU Weight (`cpu.weight`) provides proportional work-conserving fair share: if only one container is active, it can utilize 100% of the CPU, but under contention, cycles are partitioned according to weights.

### Q13: What happens to a container's child processes when the container init (PID 1) exits?
> **Answer:** In Linux, PID 1 is responsible for reaping orphan processes. If the PID 1 of a PID namespace terminates, the Linux kernel automatically sends `SIGKILL` to all other processes within that PID namespace, cleanly tearing down the container.

### Q14: Why is root / sudo required to run `mini-container`?
> **Answer:** Creating new namespaces (`CLONE_NEWPID`, `CLONE_NEWNS`), mounting filesystems, and writing to `/sys/fs/cgroup` require administrative privileges (`CAP_SYS_ADMIN`), preventing regular users from compromising host isolation.

### Q15: How does the container isolate IPC primitives?
> **Answer:** The `CLONE_NEWIPC` flag isolates System V message queues, shared memory segments, and POSIX semaphores into a private IPC namespace, preventing cross-container data snooping.

### Q16: What is the significance of the `_GNU_SOURCE` macro in our C files?
> **Answer:** It exposes GNU and POSIX system extensions in header files, making modern system calls like `clone()` and namespace flags accessible.

### Q17: Why did we disable swap memory in our cgroup configuration?
> **Answer:** If swap is enabled, when a process crosses `memory.max`, the OS pages memory out to disk rather than triggering the OOM killer. Setting `memory.swap.max = 0` guarantees strict physical RAM boundaries and immediate OOM enforcement.

### Q18: What is the function of `waitpid()` in the parent process?
> **Answer:** `waitpid()` suspends the parent process until the containerized child terminates, collects its exit status or termination signal (e.g., `SIGKILL`), and prevents the child from remaining a zombie process.

### Q19: How are cgroup directories cleaned up?
> **Answer:** Once the container process terminates, all processes vacate the cgroup. The parent calls `rmdir("/sys/fs/cgroup/minicontainer-[PID]")`, which the kernel allows only when the cgroup has zero active processes.

### Q20: Could this runtime execute a real Linux distribution like Alpine?
> **Answer:** Yes. By downloading the official Alpine minirootfs and supplying `--rootfs ./rootfs`, the container boots directly into an interactive `/bin/sh` session with isolated Busybox POSIX utilities.

---

## 9. CONCLUSION & FUTURE WORK

This project successfully designed, implemented, and empirically verified a complete container virtualization engine from scratch in C99. The implementation proves that operating system isolation, scheduling quotas, concurrency controls, and memory protection mechanisms can be realized purely through native kernel primitives with zero external software layers.

### Future Enhancements:
1. **OverlayFS Integration:** Layering read-only base images with read-write copy-on-write (COW) ephemeral storage.
2. **Network Namespaces (`veth` pairs):** Creating virtual ethernet pairs and bridging to provide isolated IP routing and port mapping.
3. **Capabilities & Seccomp Filters:** Dropping administrative capabilities and restricting permitted system calls using BPF filters.

---

## 10. REFERENCES

1. Silberschatz, A., Galvin, P. B., & Gagne, G. (2018). *Operating System Concepts* (10th ed.). Wiley.
2. Kerrisk, M. (2010). *The Linux Programming Interface: A Linux and UNIX System Programming Handbook*. No Starch Press.
3. Linux Kernel Documentation. *Control Group v2*. Available at: https://docs.kernel.org/admin-guide/cgroup-v2.html
4. Linux Programmer's Manual. *namespaces(7)*, *clone(2)*, *chroot(2)*, *cgroups(7)*.
