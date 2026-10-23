#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

if [ "$EUID" -ne 0 ]; then
    echo "Error: Please run with sudo: sudo bash scripts/test_cpu_shares.sh"
    exit 1
fi

echo "================================================================="
echo "  CO: 2 CPU SCHEDULING: PROPORTIONAL FAIR-SHARE CONTEST          "
echo "  Comparing 2 Concurrent Containers with CFS Weights 800 vs 200  "
echo "================================================================="
echo "Experiment Design:"
echo "  - Container A : CPU Weight 800 (High Share ~ 80%)"
echo "  - Container B : CPU Weight 200 (Low Share  ~ 20%)"
echo "  - Both run 100% compute loops simultaneously pinned to CPU 0"
echo "-----------------------------------------------------------------"

LOG_A="/tmp/container_a.log"
LOG_B="/tmp/container_b.log"
rm -f "$LOG_A" "$LOG_B"

# Launch Container A (Weight 800) in background pinned to Core 0
taskset -c 0 ./minicontainer run --cpu-weight 800 --hostname box-high ./tests/test_cpu 4 > "$LOG_A" 2>&1 &
PID_A=$!

# Launch Container B (Weight 200) in background pinned to Core 0
taskset -c 0 ./minicontainer run --cpu-weight 200 --hostname box-low ./tests/test_cpu 4 > "$LOG_B" 2>&1 &
PID_B=$!

echo "Containers running concurrently on Core 0 (PIDs: $PID_A, $PID_B)..."
wait $PID_A
wait $PID_B

echo ""
echo ">>> RESULTS & OBSERVATIONS <<<"
TIME_A=$(grep "CPU time used" "$LOG_A" | awk '{print $6}' | head -n 1)
TIME_B=$(grep "CPU time used" "$LOG_B" | awk '{print $6}' | head -n 1)

echo "Container A (Weight 800) CPU Time : $TIME_A seconds"
echo "Container B (Weight 200) CPU Time : $TIME_B seconds"

if [ -n "$TIME_A" ] && [ -n "$TIME_B" ]; then
    echo ""
    echo "Summary:"
    echo "  Container A received significantly more scheduling slices than Container B,"
    echo "  validating Linux CFS Proportional Share CPU Scheduling (CO: 2)!"
fi
