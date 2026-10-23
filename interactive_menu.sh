#!/usr/bin/env bash
# Master Interactive Project Demonstration Menu for Faculty Review

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Color Codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}[Error] Please run this menu with sudo:${NC}"
    echo "  sudo bash interactive_menu.sh"
    exit 1
fi

show_menu() {
    clear
    echo -e "${CYAN}========================================================================${NC}"
    echo -e "${GREEN}        MINI-CONTAINER: OPERATING SYSTEMS PROJECT DEMONSTRATION         ${NC}"
    echo -e "${YELLOW}        Covering Course Outcomes: CO: 1, CO: 2, CO: 3, CO: 4, CO: 5     ${NC}"
    echo -e "${CYAN}========================================================================${NC}"
    echo ""
    echo -e "  ${BLUE}[1]${NC} Process & Hostname Isolation (CO: 1 & CO: 5 Namespaces)"
    echo -e "  ${BLUE}[2]${NC} Virtual Memory Boundary, Page Faults & OOM Killer (CO: 4)"
    echo -e "  ${BLUE}[3]${NC} CPU Quota & CFS Scheduling Throttling (CO: 2)"
    echo -e "  ${BLUE}[4]${NC} Proportional Fair-Share CPU Contest - 2 Containers (CO: 2)"
    echo -e "  ${BLUE}[5]${NC} Concurrency, Semaphores & Shared Memory IPC (CO: 3)"
    echo -e "  ${BLUE}[6]${NC} Process Table Exhaustion & Fork Bomb Defense (CO: 1 & CO: 3)"
    echo -e "  ${BLUE}[7]${NC} Launch Interactive Alpine Linux Container Shell (CO: 5 Rootfs)"
    echo -e "  ${BLUE}[8]${NC} Live Real-Time Kernel Resource Dashboard (CO: 2 & CO: 4)"
    echo -e "  ${BLUE}[9]${NC} Run Full Automated 5-in-1 Evaluation Demo Suite"
    echo -e "  ${RED}[0]${NC} Exit"
    echo ""
    echo -e "${CYAN}------------------------------------------------------------------------${NC}"
    echo -n "Select an option [0-9]: "
}

while true; do
    show_menu
    read -r choice
    echo ""
    case $choice in
        1)
            echo -e "${GREEN}>>> DEMO 1: Process & Hostname Isolation (CLONE_NEWPID, CLONE_NEWUTS)${NC}"
            echo "Host Hostname: $(hostname)"
            echo "Host Process Count: $(ps -ef | wc -l)"
            echo "Running containerized inspection..."
            ./minicontainer run --hostname isolated-box ./tests/test_info
            read -p "Press [Enter] to return to menu..."
            ;;
        2)
            echo -e "${GREEN}>>> DEMO 2: Memory Ceiling, Demand Paging & Kernel OOM Killer (CO: 4)${NC}"
            echo "Allocating 60MB with a strict 30MB Cgroup limit..."
            ./minicontainer run --memory 30M ./tests/test_memory 60 || true
            read -p "Press [Enter] to return to menu..."
            ;;
        3)
            echo -e "${GREEN}>>> DEMO 3: CPU Scheduling Throttling via CFS Quotas (CO: 2)${NC}"
            echo "Running compute workload clamped at 40% CPU quota..."
            ./minicontainer run --cpu 40 ./tests/test_cpu 3
            read -p "Press [Enter] to return to menu..."
            ;;
        4)
            echo -e "${GREEN}>>> DEMO 4: Proportional Fair-Share CPU Scheduling Contest (CO: 2)${NC}"
            bash scripts/test_cpu_shares.sh
            read -p "Press [Enter] to return to menu..."
            ;;
        5)
            echo -e "${GREEN}>>> DEMO 5: Concurrency, Semaphores & IPC (CO: 3)${NC}"
            echo "Executing Producer-Consumer with POSIX Semaphores & Shared Memory inside container..."
            ./minicontainer run --hostname ipc-box ./tests/test_ipc_sync
            read -p "Press [Enter] to return to menu..."
            ;;
        6)
            echo -e "${GREEN}>>> DEMO 6: Fork Bomb & Process Table Exhaustion Protection (CO: 1 & CO: 3)${NC}"
            echo "Attempting to spawn 50 child processes with pids.max = 10..."
            ./minicontainer run --pids 10 ./tests/test_forkbomb 50
            read -p "Press [Enter] to return to menu..."
            ;;
        7)
            echo -e "${GREEN}>>> DEMO 7: Launching Interactive Alpine Linux Sandbox (CO: 5)${NC}"
            echo "Type 'exit' to leave the container."
            ./minicontainer run --hostname alpine-node --rootfs ./rootfs /bin/sh
            read -p "Press [Enter] to return to menu..."
            ;;
        8)
            echo -e "${GREEN}>>> DEMO 8: Live Kernel Resource Dashboard (CO: 2 & CO: 4)${NC}"
            bash scripts/monitor.sh
            read -p "Press [Enter] to return to menu..."
            ;;
        9)
            echo -e "${GREEN}>>> DEMO 9: Full Automated Evaluation Demo Suite${NC}"
            bash scripts/run_demo.sh
            read -p "Press [Enter] to return to menu..."
            ;;
        0)
            echo -e "${CYAN}Exiting. Good luck with your review!${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid option. Please choose [0-9].${NC}"
            sleep 1
            ;;
    esac
done
