#!/usr/bin/env bash
# Live ASCII Resource Dashboard for Mini-Container (CO: 2, CO: 4)

CGROUP_BASE="/sys/fs/cgroup"

clear
echo "=================================================================="
echo "          MINI-CONTAINER REAL-TIME KERNEL DASHBOARD               "
echo "  Live Monitoring of Linux Cgroups v2 Resource Accounting         "
echo "=================================================================="

# Find active minicontainer cgroups
CG_DIRS=$(ls -d ${CGROUP_BASE}/minicontainer-* 2>/dev/null || true)

if [ -z "$CG_DIRS" ]; then
    echo "No active container currently running."
    echo "Starting a monitored test container in 1 second..."
    sleep 1
    # Run a container with memory and CPU limit in background
    ./minicontainer run --memory 30M --cpu 50 --pids 10 ./tests/test_memory 25 &
    sleep 0.5
    CG_DIRS=$(ls -d ${CGROUP_BASE}/minicontainer-* 2>/dev/null || true)
fi

for CG in $CG_DIRS; do
    PID=$(basename "$CG" | cut -d'-' -f2)
    echo ""
    echo "┌─────────────────────────────────────────────────────────────┐"
    echo "│ Container ID: minicontainer-$PID  (Host PID: $PID)          │"
    echo "├─────────────────────────────────────────────────────────────┤"

    # Memory stats
    if [ -f "$CG/memory.current" ]; then
        CURR_MEM=$(cat "$CG/memory.current" 2>/dev/null || echo 0)
        MAX_MEM=$(cat "$CG/memory.max" 2>/dev/null || echo "max")
        CURR_MB=$((CURR_MEM / 1024 / 1024))
        
        if [ "$MAX_MEM" = "max" ]; then
            echo "│ Memory Current : ${CURR_MB} MB (Limit: Unlimited)                  │"
        else
            MAX_MB=$((MAX_MEM / 1024 / 1024))
            PCT=0
            if [ $MAX_MB -gt 0 ]; then
                PCT=$((CURR_MB * 100 / MAX_MB))
            fi
            BAR_LEN=15
            FILLED=$((PCT * BAR_LEN / 100))
            [ $FILLED -gt $BAR_LEN ] && FILLED=$BAR_LEN
            EMPTY=$((BAR_LEN - FILLED))
            BAR=$(printf "%${FILLED}s" | tr ' ' '█')$(printf "%${EMPTY}s" | tr ' ' '░')
            printf "│ Memory Usage   : [%s] %2d MB / %2d MB (%3d%%)    │\n" "$BAR" "$CURR_MB" "$MAX_MB" "$PCT"
        fi
    fi

    # Page Faults (CO: 4 Virtual Memory)
    if [ -f "$CG/memory.stat" ]; then
        PG_FAULT=$(grep "^pgfault " "$CG/memory.stat" | awk '{print $2}')
        PG_MAJ=$(grep "^pgmajfault " "$CG/memory.stat" | awk '{print $2}')
        ANON_MEM=$(grep "^anon " "$CG/memory.stat" | awk '{print $2 / 1024 / 1024}')
        echo "│ Minor PgFaults : ${PG_FAULT} (Proves Demand Paging)               │"
        echo "│ Major PgFaults : ${PG_MAJ} (Page Faults requiring disk I/O)        │"
        echo "│ Anonymous RAM  : ${ANON_MEM} MB                                       │"
    fi

    # CPU stats (CO: 2 Scheduling)
    if [ -f "$CG/cpu.max" ]; then
        CPU_MAX=$(cat "$CG/cpu.max")
        echo "│ CPU CFS Quota  : $CPU_MAX us (period)                  │"
    fi

    # PID stats (CO: 1 / CO: 3)
    if [ -f "$CG/pids.current" ]; then
        CURR_PIDS=$(cat "$CG/pids.current")
        MAX_PIDS=$(cat "$CG/pids.max" 2>/dev/null || echo "max")
        echo "│ Active Tasks   : $CURR_PIDS / $MAX_PIDS max                            │"
    fi

    echo "└─────────────────────────────────────────────────────────────┘"
done
