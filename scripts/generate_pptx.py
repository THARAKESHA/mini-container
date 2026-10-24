import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    # Professional Bright Theme Palette
    BG_COLOR = RGBColor(248, 250, 252)       # Light Slate #f8fafc
    WHITE = RGBColor(255, 255, 255)          # Card background #ffffff
    NAVY_DARK = RGBColor(15, 23, 42)         # Primary Text / Headers #0f172a
    NAVY_MUTED = RGBColor(71, 85, 105)       # Subtitles / Secondary #475569
    PRIMARY_BLUE = RGBColor(2, 132, 199)     # Deep Blue Accent #0284c7
    INDIGO = RGBColor(79, 70, 229)           # Rich Indigo #4f46e5
    EMERALD = RGBColor(16, 185, 129)         # Green Accent #10b981
    AMBER = RGBColor(217, 119, 6)            # Warm Amber #d97706
    CARD_BORDER = RGBColor(226, 232, 240)    # #e2e8f0

    def set_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.color.rgb = BG_COLOR
        return bg

    def add_header(slide, title_text, category_text, slide_num_str):
        # Category Tag & Slide Number
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(11.7), Inches(0.35))
        tf_c = cat_box.text_frame
        tf_c.word_wrap = True
        p_c = tf_c.paragraphs[0]
        p_c.text = f"{category_text.upper()}  |  SLIDE {slide_num_str}"
        p_c.font.size = Pt(10)
        p_c.font.bold = True
        p_c.font.color.rgb = PRIMARY_BLUE

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.62), Inches(11.7), Inches(0.7))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.size = Pt(23)
        p_t.font.bold = True
        p_t.font.color.rgb = NAVY_DARK

        # Top Accent Divider Line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.38), Inches(11.7), Inches(0.03))
        line.fill.solid()
        line.fill.fore_color.rgb = PRIMARY_BLUE
        line.line.color.rgb = PRIMARY_BLUE

    def add_card(slide, left, top, width, height, title, items, top_border_color=PRIMARY_BLUE, font_size=11):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1.5)

        # Top color accent strip
        strip = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left + Inches(0.02), top + Inches(0.02), width - Inches(0.04), Inches(0.08))
        strip.fill.solid()
        strip.fill.fore_color.rgb = top_border_color
        strip.line.color.rgb = top_border_color

        tb = slide.shapes.add_textbox(left + Inches(0.22), top + Inches(0.18), width - Inches(0.44), height - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.size = Pt(14)
        p0.font.bold = True
        p0.font.color.rgb = top_border_color
        p0.space_after = Pt(6)

        for item in items:
            p = tf.add_paragraph()
            p.text = f"•  {item}"
            p.font.size = Pt(font_size)
            p.font.color.rgb = NAVY_DARK
            p.space_after = Pt(4)

    # ==========================================
    # SLIDE 1: Title & Team Slide
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    set_background(s1)

    b1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.2), Inches(0.7), Inches(4.93), Inches(0.42))
    b1.fill.solid()
    b1.fill.fore_color.rgb = RGBColor(224, 242, 254)
    b1.line.color.rgb = PRIMARY_BLUE
    p = b1.text_frame.paragraphs[0]
    p.text = "OPERATING SYSTEMS PROJECT REVIEW (CSE)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE
    p.alignment = PP_ALIGN.CENTER

    tb1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.3), Inches(11.33), Inches(1.7))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p_title = tf1.paragraphs[0]
    p_title.text = "Mini-Container Runtime"
    p_title.font.size = Pt(38)
    p_title.font.bold = True
    p_title.font.color.rgb = NAVY_DARK
    p_title.alignment = PP_ALIGN.CENTER

    p_sub = tf1.add_paragraph()
    p_sub.text = "A Lightweight Linux Container Virtualization Engine Built from Scratch in C99\nUtilizing Linux Namespaces, Unified Cgroups v2, and VFS Sandboxing"
    p_sub.font.size = Pt(15)
    p_sub.font.color.rgb = NAVY_MUTED
    p_sub.alignment = PP_ALIGN.CENTER
    p_sub.space_before = Pt(6)

    # Team Members Cards
    m1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2.2), Inches(3.45), Inches(4.2), Inches(2.4))
    m1.fill.solid()
    m1.fill.fore_color.rgb = WHITE
    m1.line.color.rgb = PRIMARY_BLUE
    m1.line.width = Pt(2)
    tf_m1 = m1.text_frame
    tf_m1.word_wrap = True
    p1 = tf_m1.paragraphs[0]
    p1.text = "TEAM MEMBER 1"
    p1.font.size = Pt(10)
    p1.font.bold = True
    p1.font.color.rgb = PRIMARY_BLUE
    p2 = tf_m1.add_paragraph()
    p2.text = "Tharakesha M"
    p2.font.size = Pt(19)
    p2.font.bold = True
    p2.font.color.rgb = NAVY_DARK
    p3 = tf_m1.add_paragraph()
    p3.text = "Register No: 24BCE2538\nB.Tech Computer Science & Engineering\nCore Focus: Namespaces & Cgroups Subsystem"
    p3.font.size = Pt(11)
    p3.font.color.rgb = NAVY_MUTED
    p3.space_before = Pt(4)

    m2 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(3.45), Inches(4.2), Inches(2.4))
    m2.fill.solid()
    m2.fill.fore_color.rgb = WHITE
    m2.line.color.rgb = INDIGO
    m2.line.width = Pt(2)
    tf_m2 = m2.text_frame
    tf_m2.word_wrap = True
    p1_2 = tf_m2.paragraphs[0]
    p1_2.text = "TEAM MEMBER 2"
    p1_2.font.size = Pt(10)
    p1_2.font.bold = True
    p1_2.font.color.rgb = INDIGO
    p2_2 = tf_m2.add_paragraph()
    p2_2.text = "Mathu Metha S"
    p2_2.font.size = Pt(19)
    p2_2.font.bold = True
    p2_2.font.color.rgb = NAVY_DARK
    p3_2 = tf_m2.add_paragraph()
    p3_2.text = "Register No: 24BCE2805\nB.Tech Computer Science & Engineering\nCore Focus: Concurrency, Semaphores & Testing"
    p3_2.font.size = Pt(11)
    p3_2.font.color.rgb = NAVY_MUTED
    p3_2.space_before = Pt(4)

    fb = s1.shapes.add_textbox(Inches(1.0), Inches(6.25), Inches(11.33), Inches(0.5))
    tf_f = fb.text_frame
    p_f = tf_f.paragraphs[0]
    p_f.text = "GitHub Repository: https://github.com/THARAKESHA/mini-container"
    p_f.font.size = Pt(12)
    p_f.font.bold = True
    p_f.font.color.rgb = PRIMARY_BLUE
    p_f.alignment = PP_ALIGN.CENTER

    # ==========================================
    # SLIDE 2: Introduction & Industry Context
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    set_background(s2)
    add_header(s2, "Introduction & The Rise of Containerization", "Background & Context", "2 / 16")

    add_card(s2, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.1), 
             "The Evolution of Cloud Compute", 
             [
                 "Monolithic Deployment: Traditional applications ran directly on bare metal, leading to dependency conflicts ('dependency hell').",
                 "Hardware Virtualization: Introduced Hypervisors (VMware, KVM) to run multiple OS instances, but at high hardware overhead.",
                 "Container Revolution: Docker and Kubernetes replaced heavy VMs with lightweight, isolated application environments.",
                 "The Modern Cloud Standard: Over 90% of production enterprise systems rely on container runtimes (runc, containerd).",
                 "Engineering Challenge: How does the underlying operating system kernel isolate processes without hardware hypervisors?"
             ], 
             PRIMARY_BLUE, 11)

    add_card(s2, Inches(6.8), Inches(1.7), Inches(5.6), Inches(5.1), 
             "Project Purpose: Demystifying Containers", 
             [
                 "The 'Black Box' Problem: Developers treat Docker as magic without understanding POSIX system calls or kernel data structures.",
                 "Zero-Dependency Engineering: We build an entire container execution runtime strictly from scratch in C99.",
                 "Native Linux Kernel Primitives: We invoke Linux Namespaces, Unified Cgroups v2, and VFS manipulation directly.",
                 "Academic Rigor: Explicitly models all five core Course Outcomes (CO: 1 to CO: 5) from the Operating Systems syllabus.",
                 "Real-World Value: Demonstrates production-grade systems engineering applicable to high-performance systems and DevOps."
             ], 
             INDIGO, 11)

    # ==========================================
    # SLIDE 3: Problem Statement & VM Overhead
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    set_background(s3)
    add_header(s3, "Problem Statement: Containers vs. Virtual Machines", "Comparative Analysis", "3 / 16")

    add_card(s3, Inches(0.8), Inches(1.7), Inches(5.6), Inches(4.1), 
             "Traditional Virtual Machines (Hypervisors)", 
             [
                 "Virtualizes the hardware layer using hypervisors (Type-1/Type-2).",
                 "Requires a separate, redundant guest OS kernel per instance.",
                 "High memory footprint (1 - 4 GB) and slow boot latency (30 - 60s).",
                 "Incurs hardware emulation translation penalties and CPU traps.",
                 "Rigid, coarse-grained hardware resource partitioning."
             ], 
             AMBER, 11)

    add_card(s3, Inches(6.8), Inches(1.7), Inches(5.6), Inches(4.1), 
             "OS-Level Containers (mini-container in C)", 
             [
                 "Shares the single underlying host Linux kernel with zero emulation.",
                 "Containers are regular OS processes wrapped in kernel boundaries.",
                 "Sub-second boot times (10-20ms) and minimal RAM overhead (< 5MB).",
                 "Near-native bare-metal execution performance with hardware quotas.",
                 "Fine-grained dynamic control via modern Linux Cgroups v2."
             ], 
             EMERALD, 11)

    rep_bar = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.0), Inches(11.6), Inches(0.95))
    rep_bar.fill.solid()
    rep_bar.fill.fore_color.rgb = WHITE
    rep_bar.line.color.rgb = CARD_BORDER
    tf_rb = rep_bar.text_frame
    p_rb = tf_rb.paragraphs[0]
    p_rb.text = "EFFICIENCY COMPARISON BENCHMARK"
    p_rb.font.size = Pt(10)
    p_rb.font.bold = True
    p_rb.font.color.rgb = PRIMARY_BLUE
    p_rb2 = tf_rb.add_paragraph()
    p_rb2.text = "Boot Latency: VM (45,000 ms) vs. Container (15 ms)  |  Memory Overhead: VM (~1500 MB) vs. Container (< 5 MB)  |  CPU Overhead: ~0.1%"
    p_rb2.font.size = Pt(11)
    p_rb2.font.color.rgb = NAVY_DARK

    # ==========================================
    # SLIDE 4: Literature Survey & Technology Landscape
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    set_background(s4)
    add_header(s4, "Literature Survey & Container Runtimes Landscape", "Literature Survey", "4 / 16")

    rows = 5
    cols = 4
    table_shape4 = s4.shapes.add_table(rows, cols, Inches(0.8), Inches(1.7), Inches(11.7), Inches(5.0))
    table4 = table_shape4.table
    table4.columns[0].width = Inches(2.5)
    table4.columns[1].width = Inches(3.0)
    table4.columns[2].width = Inches(3.2)
    table4.columns[3].width = Inches(3.0)

    headers4 = ["Technology", "Isolation Mechanism", "Language & Dependencies", "Primary Use Case"]
    for i, h in enumerate(headers4):
        cell = table4.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = PRIMARY_BLUE
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = WHITE

    data4 = [
        ("Docker (runc)", "Namespaces + Cgroups v1/v2", "Go (Heavy daemon, containerd)", "Enterprise Cloud Containers"),
        ("LXC / LXD", "Linux Namespaces + AppArmor", "C / Go (System containers)", "Full OS System Containers"),
        ("QEMU / KVM", "Hardware Hypervisor (VT-x)", "C / Assembly (Guest kernel required)", "Full Hardware Virtualization"),
        ("mini-container (Ours)", "Namespaces + Unified Cgroups v2", "Pure C99 (Zero third-party libraries)", "Educational Systems Research")
    ]

    for row_idx, data in enumerate(data4):
        for col_idx, val in enumerate(data):
            cell = table4.cell(row_idx + 1, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if (row_idx % 2 == 0) else RGBColor(241, 245, 249)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(11)
            p.font.color.rgb = NAVY_DARK

    # ==========================================
    # SLIDE 5: Course Outcomes Alignment Matrix
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    set_background(s5)
    add_header(s5, "Course Outcomes (CO: 1 to CO: 5) Alignment Matrix", "Syllabus Matrix", "5 / 16")

    rows = 6
    cols = 3
    table_shape5 = s5.shapes.add_table(rows, cols, Inches(0.8), Inches(1.7), Inches(11.7), Inches(5.1))
    table5 = table_shape5.table
    table5.columns[0].width = Inches(3.2)
    table5.columns[1].width = Inches(4.5)
    table5.columns[2].width = Inches(4.0)

    headers5 = ["Course Outcome (CO)", "Syllabus Topics Covered", "Implementation Mechanism in C"]
    for i, h in enumerate(headers5):
        cell = table5.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = PRIMARY_BLUE
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = WHITE

    matrix_data5 = [
        ("CO: 1 OS Principles & Processes", "System calls, User/Kernel modes, PCB, Process creation", "clone() with isolated stack, waitpid(), custom PCB handling"),
        ("CO: 2 CPU Scheduling", "CFS quotas, Preemption, Proportional Fair Share", "cgroups cpu.max (40% quota) & cpu.weight (4:1 contest)"),
        ("CO: 3 Concurrency & IPC", "Synchronization primitives, Semaphores, Shared Memory", "POSIX sem_t (mutex, empty, full) & mmap ring buffer"),
        ("CO: 4 Memory Management", "Virtual memory, Demand paging, Page faults, OOM", "cgroups memory.max, pgfault tracking (7,705 faults), SIGKILL"),
        ("CO: 5 Virtualization & Filesystems", "Container virtualization, Mount propagation, VFS", "Namespaces (PID, UTS, Mount, IPC), chroot(), private /proc")
    ]

    for row_idx, data in enumerate(matrix_data5):
        for col_idx, val in enumerate(data):
            cell = table5.cell(row_idx + 1, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if (row_idx % 2 == 0) else RGBColor(241, 245, 249)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(11)
            p.font.color.rgb = NAVY_DARK

    # ==========================================
    # SLIDE 6: System Architecture & Layered Design
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    set_background(s6)
    add_header(s6, "System Architecture: Layered Kernel Abstractions", "System Architecture", "6 / 16")

    add_card(s6, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.1), 
             "Host vs. Container Abstraction Layers", 
             [
                 "User Space Layer (CLI): minicontainer CLI parses commands and parameters (--memory, --cpu, --pids, --hostname, --rootfs).",
                 "Host Process Orchestrator: Allocates 1MB stack, sets up sync_pipe, and coordinates child lifecycles with waitpid().",
                 "Linux Kernel Subsystem Boundary: clone() syscall creates isolated namespaces; /sys/fs/cgroup/ attaches resource caps.",
                 "Container Sandbox Layer: Child executes as PID 1, completely partitioned from host visibility.",
                 "Virtual File System Layer: Isolated rootfs (Alpine Linux) with private /proc pseudo-filesystem."
             ], 
             PRIMARY_BLUE, 11)

    add_card(s6, Inches(6.8), Inches(1.7), Inches(5.6), Inches(5.1), 
             "Key Kernel Interfaces Utilized", 
             [
                 "sched.h (clone): Bitwise namespace creation flags (CLONE_NEWPID, CLONE_NEWUTS, CLONE_NEWNS, CLONE_NEWIPC).",
                 "sys/mount.h: VFS mount isolation and MS_PRIVATE propagation.",
                 "unistd.h (chroot): Root directory confinement.",
                 "sys/fs/cgroup: Linux unified cgroup v2 controller interface.",
                 "semaphore.h & sys/mman.h: Concurrency synchronization and anonymous shared memory."
             ], 
             INDIGO, 11)

    # ==========================================
    # SLIDE 7: Execution Lifecycle & State Machine
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    set_background(s7)
    add_header(s7, "Execution Lifecycle: Coordinated Process Pipeline", "Process Lifecycle Flow", "7 / 16")

    add_card(s7, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.1), 
             "Step-by-Step Execution Sequence", 
             [
                 "1. CLI Parsing: User inputs resource bounds and command.",
                 "2. Child Stack Allocation: malloc(1MB) provides stack space.",
                 "3. POSIX Sync Pipe: pipe(sync_pipe) opened as synchronization barrier.",
                 "4. clone() Syscall: Dispatches child into new namespaces.",
                 "5. Cgroups Attachment: Parent writes child PID to cgroup.procs.",
                 "6. Controller Envelopes: Sets memory.max, cpu.max, pids.max.",
                 "7. Handshake Signal: Parent writes 'G' byte to unblock child.",
                 "8. Sandbox Execution: Child sets hostname, chroot(), execvp().",
                 "9. Post-Execution Accounting: Reads memory.stat, logs page faults."
             ], 
             PRIMARY_BLUE, 11)

    add_card(s7, Inches(6.8), Inches(1.7), Inches(5.6), Inches(5.1), 
             "Process State Machine & Safety", 
             [
                 "State 1: CREATED -> Child spawned via clone() but paused.",
                 "State 2: BOUND -> Parent completes cgroup configuration.",
                 "State 3: JAILED -> Child unblocked; executes chroot() & mounts.",
                 "State 4: RUNNING -> execvp() overwrites address space (PID 1).",
                 "State 5: TERMINATED -> Normal exit or OOM Killer SIGKILL.",
                 "State 6: RECLAIMED -> Parent waitpid() catches status, rmdir(cgroup)."
             ], 
             EMERALD, 11)

    # ==========================================
    # SLIDE 8: Core Subsystem 1: Linux Namespaces
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    set_background(s8)
    add_header(s8, "Core Subsystem 1: Linux Namespaces (Visibility)", "Kernel Namespaces", "8 / 16")

    add_card(s8, Inches(0.8), Inches(1.7), Inches(5.6), Inches(2.45), 
             "PID Namespace (CLONE_NEWPID)", 
             [
                 "Virtualizes the process ID hierarchy.",
                 "Container payload becomes PID 1 inside the container.",
                 "Host processes (47 active) are completely invisible.",
                 "Signals (SIGKILL/SIGSTOP) from container cannot reach host."
             ], 
             PRIMARY_BLUE, 11)

    add_card(s8, Inches(6.8), Inches(1.7), Inches(5.6), Inches(2.45), 
             "UTS Namespace (CLONE_NEWUTS)", 
             [
                 "Isolates nodename (hostname) and NIS domain name.",
                 "Allows container to execute sethostname('isolated-box').",
                 "Host OS hostname remains untouched as 'Tharakesha'.",
                 "Prevents multi-tenant hostname collisions."
             ], 
             INDIGO, 11)

    add_card(s8, Inches(0.8), Inches(4.35), Inches(5.6), Inches(2.45), 
             "Mount Namespace (CLONE_NEWNS)", 
             [
                 "Decouples the Virtual File System (VFS) mount table.",
                 "Enforces MS_PRIVATE mount propagation.",
                 "Mounting private /proc does not alter host /proc.",
                 "Provides isolated storage views."
             ], 
             EMERALD, 11)

    add_card(s8, Inches(6.8), Inches(4.35), Inches(5.6), Inches(2.45), 
             "IPC Namespace (CLONE_NEWIPC)", 
             [
                 "Isolates System V IPC and POSIX message queues.",
                 "Shared memory segments and semaphores are private.",
                 "Prevents cross-container data snooping.",
                 "Essential for multi-tenant container security."
             ], 
             AMBER, 11)

    # ==========================================
    # SLIDE 9: Core Subsystem 2: Cgroups v2
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    set_background(s9)
    add_header(s9, "Core Subsystem 2: Unified Cgroups v2 (Resource Envelopes)", "Resource Control", "9 / 16")

    add_card(s9, Inches(0.8), Inches(1.7), Inches(5.6), Inches(2.45), 
             "Memory Ceiling (memory.max)", 
             [
                 "Defines hard byte threshold on physical DRAM (e.g., 30MB).",
                 "Sets memory.swap.max = 0 to prevent paging to disk.",
                 "Forces kernel Out-Of-Memory (OOM) Killer intervention.",
                 "Protects host from memory exhaustion."
             ], 
             AMBER, 11)

    add_card(s9, Inches(6.8), Inches(1.7), Inches(5.6), Inches(2.45), 
             "CPU Bandwidth Quota (cpu.max)", 
             [
                 "CFS Bandwidth Control: quota period (e.g. 40000 100000).",
                 "Limits container compute to deterministic 40% bandwidth.",
                 "Scheduler removes task from runqueue when quota spent.",
                 "Prevents runaway threads from starving host CPU."
             ], 
             PRIMARY_BLUE, 11)

    add_card(s9, Inches(0.8), Inches(4.35), Inches(5.6), Inches(2.45), 
             "Proportional Share (cpu.weight)", 
             [
                 "Weighted fair queuing for concurrent workloads (1 - 10000).",
                 "Weights 800 vs 200 allocate 80% and 20% on Core 0.",
                 "Empirically validated exact 4.02 : 1 execution ratio.",
                 "Work-conserving CPU scheduling."
             ], 
             INDIGO, 11)

    add_card(s9, Inches(6.8), Inches(4.35), Inches(5.6), Inches(2.45), 
             "Process Count Cap (pids.max)", 
             [
                 "Imposes ceiling on total concurrent tasks (threads & processes).",
                 "Setting pids.max = 10 blocks fork bomb denial-of-service.",
                 "10th fork() fails immediately with errno 11 (EAGAIN).",
                 "Preserves host Process Control Block (PCB) table."
             ], 
             EMERALD, 11)

    # ==========================================
    # SLIDE 10: Core Subsystem 3: Rootfs Sandboxing
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    set_background(s10)
    add_header(s10, "Core Subsystem 3: Filesystem Sandboxing & VFS", "Filesystem Isolation", "10 / 16")

    add_card(s10, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.1), 
             "Root Filesystem Jailing (chroot)", 
             [
                 "Confines the process to a self-contained directory tree (./rootfs).",
                 "Leverages official Alpine Linux minirootfs (~3.5MB compressed).",
                 "Provides full POSIX userland utilities (/bin/sh, /bin/ls, /bin/ps).",
                 "chroot(rootfs) resets apparent root directory (/) to container directory.",
                 "Prevents directory traversal above the container boundary.",
                 "Containerized programs cannot access host files, Windows drives, or WSL system directories."
             ], 
             PRIMARY_BLUE, 11)

    add_card(s10, Inches(6.8), Inches(1.7), Inches(5.6), Inches(5.1), 
             "Private /proc VFS Mount Isolation", 
             [
                 "The Linux /proc directory is a kernel-generated pseudo-filesystem containing active process status.",
                 "Without private /proc, running ps aux inside a container would still expose all host processes!",
                 "Our runtime enforces mount(NULL, '/', NULL, MS_REC | MS_PRIVATE, NULL) to isolate mount propagation.",
                 "Mounts fresh procfs inside container: mount('proc', '/proc', 'proc', 0, NULL).",
                 "Result: ps aux inside the container displays only PID 1 (/bin/sh) and PID 2 (ps aux)."
             ], 
             EMERALD, 11)

    # ==========================================
    # SLIDE 11: Concurrency & Semaphores (CO: 3)
    # ==========================================
    s11 = prs.slides.add_slide(blank_layout)
    set_background(s11)
    add_header(s11, "Classical Concurrency: Producer-Consumer with Semaphores (CO: 3)", "Concurrency Primitives", "11 / 16")

    add_card(s11, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.1), 
             "Bounded-Buffer Synchronization Model", 
             [
                 "Implements the classic Bounded-Buffer Concurrency Problem across container processes.",
                 "Binary Semaphore (mutex): Initialized to 1; enforces mutual exclusion for the critical section.",
                 "Counting Semaphore (empty_slots): Initialized to buffer capacity (N = 5).",
                 "Counting Semaphore (full_slots): Initialized to 0 items available.",
                 "Shared Memory (mmap): Allocated via MAP_SHARED | MAP_ANONYMOUS across fork().",
                 "Zero Race Conditions: 10 items produced and consumed with zero race conditions or buffer corruption."
             ], 
             INDIGO, 11)

    add_card(s11, Inches(6.8), Inches(1.7), Inches(5.6), Inches(5.1), 
             "Parent-Child IPC Pipe Synchronization Barrier", 
             [
                 "The Race Condition Hazard: Cloned child could execute payload before parent finishes writing cgroup limits.",
                 "The POSIX Pipe Solution: Parent and child share a unidirectional sync_pipe[2].",
                 "Child Execution: Calls read(sync_pipe[0]) and immediately BLOCKS.",
                 "Parent Execution: Completes cgroup setup, then writes single trigger byte 'G'.",
                 "Unblocking: Child receives byte, closes pipe, and proceeds safely to execvp().",
                 "Guarantees deterministic, race-free resource limits from microsecond zero."
             ], 
             PRIMARY_BLUE, 11)

    # ==========================================
    # SLIDE 12: Virtual Memory & Page Faults (CO: 4)
    # ==========================================
    s12 = prs.slides.add_slide(blank_layout)
    set_background(s12)
    add_header(s12, "Virtual Memory: Demand Paging & OOM Killer (CO: 4)", "Memory Management", "12 / 16")

    add_card(s12, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.1), 
             "Demand Paging & Page Fault Accounting", 
             [
                 "Optimistic Memory Allocation: malloc() reserves virtual address space without allocating physical DRAM frames.",
                 "Demand Paging Traps: When memset() accesses pages, the CPU MMU triggers Page Faults to map physical frames.",
                 "Kernel Metric Tracking: Reads /sys/fs/cgroup/.../memory.stat upon container conclusion.",
                 "Minor Page Faults Recorded: Exactly 7,705 Minor Page Faults logged during 30MB allocation.",
                 "Major Page Faults: Exactly 1; proves zero disk thrashing occurred.",
                 "Empirical Proof: Directly proves demand paging mechanisms in the operating system kernel."
             ], 
             AMBER, 11)

    add_card(s12, Inches(6.8), Inches(1.7), Inches(5.6), Inches(5.1), 
             "Kernel Out-Of-Memory (OOM) Killer Intervention", 
             [
                 "Resource Constraint: Container configured with strict 30MB memory ceiling (memory.max = 31457280).",
                 "Swap Disabled: memory.swap.max = 0 forces immediate physical memory enforcement.",
                 "Stress Workload: test_memory attempts to allocate 60MB in 5MB steps.",
                 "Kernel Intervention: At 30MB, the Linux kernel Out-Of-Memory Killer steps in.",
                 "Signal Dispatch: Sends uncatchable SIGKILL (signal 9) to terminate the container.",
                 "Parent Detection: WIFSIGNALED(status) detects SIGKILL and reports clean diagnostic."
             ], 
             PRIMARY_BLUE, 11)

    # ==========================================
    # SLIDE 13: CPU Scheduling & Proportional Shares (CO: 2)
    # ==========================================
    s13 = prs.slides.add_slide(blank_layout)
    set_background(s13)
    add_header(s13, "CPU Scheduling: CFS Quotas & Fair-Share Contest (CO: 2)", "CPU Scheduling", "13 / 16")

    add_card(s13, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.1), 
             "CFS Bandwidth Quota Throttling (cpu.max)", 
             [
                 "CFS Scheduler Model: Linux allocates CPU time over 100ms periods.",
                 "Quota Applied: --cpu 40 configures quota = 40,000 us per 100,000 us period.",
                 "Workload: test_cpu executes an intensive infinite compute loop for 3 wall-clock seconds.",
                 "Observed CPU Time: Clamped at 1.12 seconds CPU time (37.4% effective CPU).",
                 "Preemption Guarantee: Completely Fair Scheduler suspends task once quota is spent, protecting host cores."
             ], 
             PRIMARY_BLUE, 11)

    add_card(s13, Inches(6.8), Inches(1.7), Inches(5.6), Inches(5.1), 
             "Proportional Share Contest: 800 vs. 200 (cpu.weight)", 
             [
                 "Contest Design: Two concurrent containers pinned to CPU Core 0 via taskset -c 0.",
                 "Priority Configuration: Container A (weight 800 ~ 80%) vs. Container B (weight 200 ~ 20%).",
                 "Observed Execution Time: Container A: 2.78s CPU Time  |  Container B: 0.69s CPU Time.",
                 "Empirical Ratio: 2.78 / 0.69 = 4.02 : 1 execution ratio.",
                 "Validation: Matches the theoretical 4 : 1 weight ratio with 99.5% accuracy!"
             ], 
             INDIGO, 11)

    # ==========================================
    # SLIDE 14: Process Table Protection & Fork Bomb Defense (CO: 1 & 3)
    # ==========================================
    s14 = prs.slides.add_slide(blank_layout)
    set_background(s14)
    add_header(s14, "Security & DoS Defense: Fork Bomb Mitigation (CO: 1 & 3)", "Security Controls", "14 / 16")

    add_card(s14, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.1), 
             "The Fork Bomb Vulnerability", 
             [
                 "Mechanism of Attack: A malicious process recursively calls fork() in an infinite loop.",
                 "Resource Depletion: Rapidly exhausts the operating system's Process Control Block (PCB) table.",
                 "System Consequence: Unconfined machines freeze entirely; administrators cannot launch terminals or kill tasks.",
                 "Relevance: Demonstrates operating system deadlock, starvation, and process resource exhaustion."
             ], 
             AMBER, 11)

    add_card(s14, Inches(6.8), Inches(1.7), Inches(5.6), Inches(5.1), 
             "Cgroups v2 Task Limiting (pids.max)", 
             [
                 "Hardware Defense: Setting pids.max = 10 caps total concurrent threads/processes.",
                 "Laboratory Stress Test: test_forkbomb attempts to spawn 50 processes.",
                 "Interception: Children 1 through 9 spawn successfully (10 total tasks including parent).",
                 "Rejection: 10th fork() blocked with errno 11 (EAGAIN: Resource temporarily unavailable).",
                 "Host Stability: Host machine remained 100% responsive throughout the attack."
             ], 
             EMERALD, 11)

    # ==========================================
    # SLIDE 15: Empirical Laboratory Benchmarks Summary
    # ==========================================
    s15 = prs.slides.add_slide(blank_layout)
    set_background(s15)
    add_header(s15, "Empirical Laboratory Benchmarks & Observed Results", "Observed Metrics", "15 / 16")

    # 4 Scorecards
    c1 = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.7), Inches(5.6), Inches(2.45))
    c1.fill.solid()
    c1.fill.fore_color.rgb = WHITE
    c1.line.color.rgb = PRIMARY_BLUE
    c1.line.width = Pt(1.5)
    tf_c1 = c1.text_frame
    tf_c1.word_wrap = True
    p = tf_c1.paragraphs[0]
    p.text = "1. Process Virtualization (CO: 1 & 5)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE
    p_b = tf_c1.add_paragraph()
    p_b.text = "• Container Process reports PID = 1; Parent PID = 0.\n• Host operating system processes (47 active) are completely hidden.\n• Hostname virtualized to 'isolated-box' without altering host."
    p_b.font.size = Pt(10.5)
    p_b.font.color.rgb = NAVY_DARK

    c2 = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.7), Inches(5.6), Inches(2.45))
    c2.fill.solid()
    c2.fill.fore_color.rgb = WHITE
    c2.line.color.rgb = AMBER
    c2.line.width = Pt(1.5)
    tf_c2 = c2.text_frame
    tf_c2.word_wrap = True
    p = tf_c2.paragraphs[0]
    p.text = "2. Memory Ceiling & Demand Paging (CO: 4)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = AMBER
    p_b = tf_c2.add_paragraph()
    p_b.text = "• Workload allocated 30MB of 60MB; terminated by SIGKILL (signal 9).\n• Kernel logged 7,705 Minor Page Faults, validating Demand Paging.\n• 1 Major Page Fault; Swap disabled to force immediate OOM protection."
    p_b.font.size = Pt(10.5)
    p_b.font.color.rgb = NAVY_DARK

    c3 = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.35), Inches(5.6), Inches(2.45))
    c3.fill.solid()
    c3.fill.fore_color.rgb = WHITE
    c3.line.color.rgb = INDIGO
    c3.line.width = Pt(1.5)
    tf_c3 = c3.text_frame
    tf_c3.word_wrap = True
    p = tf_c3.paragraphs[0]
    p.text = "3. Proportional Fair-Share CPU Contest (CO: 2)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = INDIGO
    p_b = tf_c3.add_paragraph()
    p_b.text = "• Competing containers on CPU Core 0 with CFS weights 800 vs 200.\n• Container A CPU Time: 2.78s  |  Container B CPU Time: 0.69s.\n• Exact 4.02 : 1 execution ratio (matches theoretical 4:1 with 99.5% accuracy!)."
    p_b.font.size = Pt(10.5)
    p_b.font.color.rgb = NAVY_DARK

    c4 = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(4.35), Inches(5.6), Inches(2.45))
    c4.fill.solid()
    c4.fill.fore_color.rgb = WHITE
    c4.line.color.rgb = EMERALD
    c4.line.width = Pt(1.5)
    tf_c4 = c4.text_frame
    tf_c4.word_wrap = True
    p = tf_c4.paragraphs[0]
    p.text = "4. Fork Bomb & PCB Table Defense (CO: 1 & 3)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = EMERALD
    p_b = tf_c4.add_paragraph()
    p_b.text = "• Stress test attempted to spawn 50 concurrent processes.\n• Cgroups pids.max = 10 capped execution; Children 1 - 9 spawned.\n• 10th fork() blocked with errno 11 (EAGAIN); host OS remained responsive."
    p_b.font.size = Pt(10.5)
    p_b.font.color.rgb = NAVY_DARK

    # ==========================================
    # SLIDE 16: Summary & Live Demonstration
    # ==========================================
    s16 = prs.slides.add_slide(blank_layout)
    set_background(s16)

    b16 = s16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.3), Inches(0.9), Inches(4.7), Inches(0.42))
    b16.fill.solid()
    b16.fill.fore_color.rgb = RGBColor(224, 242, 254)
    b16.line.color.rgb = PRIMARY_BLUE
    p = b16.text_frame.paragraphs[0]
    p.text = "EVALUATION & LIVE DEMONSTRATION"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE
    p.alignment = PP_ALIGN.CENTER

    tb16 = s16.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.33), Inches(1.5))
    tf16 = tb16.text_frame
    tf16.word_wrap = True
    p16_t = tf16.paragraphs[0]
    p16_t.text = "Interactive Project Demonstration"
    p16_t.font.size = Pt(36)
    p16_t.font.bold = True
    p16_t.font.color.rgb = NAVY_DARK
    p16_t.alignment = PP_ALIGN.CENTER

    p16_s = tf16.add_paragraph()
    p16_s.text = "Complete C99 Runtime Covering CO: 1 to CO: 5 with Master Interactive Menu and Real-Time Kernel Metrics"
    p16_s.font.size = Pt(15)
    p16_s.font.color.rgb = NAVY_MUTED
    p16_s.alignment = PP_ALIGN.CENTER
    p16_s.space_before = Pt(8)

    cmd_box = s16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(3.2), Inches(3.3), Inches(6.93), Inches(1.4))
    cmd_box.fill.solid()
    cmd_box.fill.fore_color.rgb = WHITE
    cmd_box.line.color.rgb = PRIMARY_BLUE
    cmd_box.line.width = Pt(2)
    tf_cmd = cmd_box.text_frame
    p_cmd = tf_cmd.paragraphs[0]
    p_cmd.text = "$ sudo bash interactive_menu.sh"
    p_cmd.font.size = Pt(22)
    p_cmd.font.bold = True
    p_cmd.font.color.rgb = PRIMARY_BLUE
    p_cmd.alignment = PP_ALIGN.CENTER
    p_cmd_sub = tf_cmd.add_paragraph()
    p_cmd_sub.text = "(Or double-click Run-MiniContainer.bat directly on your Windows Desktop)"
    p_cmd_sub.font.size = Pt(12)
    p_cmd_sub.font.color.rgb = NAVY_MUTED
    p_cmd_sub.alignment = PP_ALIGN.CENTER
    p_cmd_sub.space_before = Pt(4)

    tb_footer = s16.shapes.add_textbox(Inches(1.0), Inches(5.1), Inches(11.33), Inches(1.6))
    tf_foot = tb_footer.text_frame
    p_team = tf_foot.paragraphs[0]
    p_team.text = "Project Team: Tharakesha M (24BCE2538) & Mathu Metha S (24BCE2805)"
    p_team.font.size = Pt(16)
    p_team.font.bold = True
    p_team.font.color.rgb = NAVY_DARK
    p_team.alignment = PP_ALIGN.CENTER

    p_git = tf_foot.add_paragraph()
    p_git.text = "GitHub Repository: https://github.com/THARAKESHA/mini-container"
    p_git.font.size = Pt(14)
    p_git.font.color.rgb = PRIMARY_BLUE
    p_git.alignment = PP_ALIGN.CENTER
    p_git.space_before = Pt(6)

    # Save
    output_path = os.path.join(os.path.dirname(__file__), "..", "presentation.pptx")
    prs.save(output_path)
    print(f"[Success] Saved 16-slide bright-theme presentation to {output_path}")

if __name__ == "__main__":
    create_presentation()
