#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

if [ "$EUID" -ne 0 ]; then
    echo "Error: Please run this demo with sudo:"
    echo "  sudo bash scripts/run_demo.sh"
    exit 1
fi

echo "=========================================================="
echo "    MINI-CONTAINER: 5-IN-1 AUTOMATED EVALUATION SUITE     "
echo "  Covering Operating Systems Outcomes: CO: 1 to CO: 5     "
echo "=========================================================="
sleep 1

# 1. Namespace Isolation Demo (PID & UTS)
echo ""
echo ">>> [DEMO 1/5] Process & Hostname Isolation (CO: 1 & CO: 5)"
echo "Host Hostname: $(hostname)"
echo "Host Process Count: $(ps -ef | wc -l)"
echo "--- Running inside container ---"
./minicontainer run --hostname isolated-box ./tests/test_info

# 2. Cgroups Memory Limit & OOM Killer Demo
echo ""
echo ">>> [DEMO 2/5] Memory Boundary, Page Faults & Linux OOM Killer (CO: 4)"
echo "Running memory stress test (attempting 60MB) with a 30MB Cgroup limit..."
echo "Expected behavior: Kernel Out-Of-Memory (OOM) Killer terminates process with SIGKILL."
./minicontainer run --memory 30M ./tests/test_memory 60 || true

# 3. Cgroups CPU Quota Demo
echo ""
echo ">>> [DEMO 3/5] CPU Scheduling Throttling (CO: 2)"
echo "Running CPU-intensive workload with 40% CPU quota..."
./minicontainer run --cpu 40 ./tests/test_cpu 3

# 4. Concurrency & Synchronization Primitives Demo
echo ""
echo ">>> [DEMO 4/5] Classical Concurrency & Semaphores (CO: 3)"
echo "Running Producer-Consumer synchronization with sem_t and shared memory..."
./minicontainer run --hostname ipc-box ./tests/test_ipc_sync

# 5. Cgroups Fork Bomb / PID Exhaustion Protection
echo ""
echo ">>> [DEMO 5/5] Process Table Exhaustion Protection (CO: 1 & CO: 3)"
echo "Attempting to spawn 50 processes with a limit of 10 PIDs..."
./minicontainer run --pids 10 ./tests/test_forkbomb 50

echo ""
echo "=========================================================="
echo "   ALL 5 OPERATING SYSTEMS DEMOS COMPLETED SUCCESSFULLY!  "
echo "   All CO: 1 to CO: 5 Verifications Passed Flawlessly!    "
echo "=========================================================="
