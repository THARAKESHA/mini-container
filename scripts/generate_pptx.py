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

    # Clean, Professional Bright Theme Palette
    BG_COLOR = RGBColor(248, 250, 252)       # Light Slate #f8fafc
    WHITE = RGBColor(255, 255, 255)          # Card background #ffffff
    BORDER_LIGHT = RGBColor(226, 232, 240)   # #e2e8f0
    NAVY_DARK = RGBColor(15, 23, 42)         # Primary Text / Headers #0f172a
    NAVY_MUTED = RGBColor(71, 85, 105)       # Subtitles / Secondary #475569
    PRIMARY_BLUE = RGBColor(2, 132, 199)     # Deep Blue Accent #0284c7
    INDIGO = RGBColor(79, 70, 229)           # Rich Indigo #4f46e5
    EMERALD = RGBColor(16, 185, 129)         # Green Accent #10b981
    AMBER = RGBColor(217, 119, 6)            # Warm Amber #d97706
    CARD_SHADOW_BORDER = RGBColor(203, 213, 225) # #cbd5e1

    def set_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.color.rgb = BG_COLOR
        return bg

    def add_header(slide, title_text, category_text):
        # Category Tag
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.35))
        tf_c = cat_box.text_frame
        tf_c.word_wrap = True
        p_c = tf_c.paragraphs[0]
        p_c.text = category_text.upper()
        p_c.font.size = Pt(11)
        p_c.font.bold = True
        p_c.font.color.rgb = PRIMARY_BLUE

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(11.7), Inches(0.7))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.size = Pt(24)
        p_t.font.bold = True
        p_t.font.color.rgb = NAVY_DARK

        # Top Accent Divider
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.42), Inches(11.7), Inches(0.03))
        line.fill.solid()
        line.fill.fore_color.rgb = PRIMARY_BLUE
        line.line.color.rgb = PRIMARY_BLUE

    def add_card(slide, left, top, width, height, title, items, top_border_color=PRIMARY_BLUE):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = CARD_SHADOW_BORDER
        card.line.width = Pt(1.5)

        # Top color strip representation
        strip = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left + Inches(0.02), top + Inches(0.02), width - Inches(0.04), Inches(0.1))
        strip.fill.solid()
        strip.fill.fore_color.rgb = top_border_color
        strip.line.color.rgb = top_border_color

        tb = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.22), width - Inches(0.5), height - Inches(0.35))
        tf = tb.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.size = Pt(15)
        p0.font.bold = True
        p0.font.color.rgb = top_border_color
        p0.space_after = Pt(8)

        for item in items:
            p = tf.add_paragraph()
            p.text = f"•  {item}"
            p.font.size = Pt(12)
            p.font.color.rgb = NAVY_DARK
            p.space_after = Pt(6)

    # ==========================================
    # SLIDE 1: Title & Team Slide (Bright Background)
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    set_background(s1)

    # Top Tag
    b1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.3), Inches(0.8), Inches(4.7), Inches(0.45))
    b1.fill.solid()
    b1.fill.fore_color.rgb = RGBColor(224, 242, 254)  # light blue
    b1.line.color.rgb = PRIMARY_BLUE
    p = b1.text_frame.paragraphs[0]
    p.text = "OPERATING SYSTEMS PROJECT REVIEW"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE
    p.alignment = PP_ALIGN.CENTER

    # Main Title & Subtitle
    tb1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.4), Inches(11.33), Inches(1.8))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p_title = tf1.paragraphs[0]
    p_title.text = "Mini-Container Runtime"
    p_title.font.size = Pt(40)
    p_title.font.bold = True
    p_title.font.color.rgb = NAVY_DARK
    p_title.alignment = PP_ALIGN.CENTER

    p_sub = tf1.add_paragraph()
    p_sub.text = "A Lightweight Linux Container Virtualization Engine Built from Scratch in C99\nUtilizing Linux Namespaces, Unified Cgroups v2, and VFS Sandboxing"
    p_sub.font.size = Pt(16)
    p_sub.font.color.rgb = NAVY_MUTED
    p_sub.alignment = PP_ALIGN.CENTER
    p_sub.space_before = Pt(8)

    # Team Members Cards
    # Member 1: Tharakesha M
    m1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2.2), Inches(3.6), Inches(4.2), Inches(2.3))
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
    p2.font.size = Pt(20)
    p2.font.bold = True
    p2.font.color.rgb = NAVY_DARK
    p3 = tf_m1.add_paragraph()
    p3.text = "Register No: 24BCE2538\nB.Tech Computer Science & Engineering\nCore Developer (Namespaces & Cgroups)"
    p3.font.size = Pt(11)
    p3.font.color.rgb = NAVY_MUTED
    p3.space_before = Pt(4)

    # Member 2: Mathu Metha S
    m2 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(3.6), Inches(4.2), Inches(2.3))
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
    p2_2.font.size = Pt(20)
    p2_2.font.bold = True
    p2_2.font.color.rgb = NAVY_DARK
    p3_2 = tf_m2.add_paragraph()
    p3_2.text = "Register No: 24BCE2805\nB.Tech Computer Science & Engineering\nCore Developer (Concurrency & Testing)"
    p3_2.font.size = Pt(11)
    p3_2.font.color.rgb = NAVY_MUTED
    p3_2.space_before = Pt(4)

    # Footer
    fb = s1.shapes.add_textbox(Inches(1.0), Inches(6.3), Inches(11.33), Inches(0.5))
    tf_f = fb.text_frame
    p_f = tf_f.paragraphs[0]
    p_f.text = "GitHub Repository: https://github.com/THARAKESHA/mini-container"
    p_f.font.size = Pt(12)
    p_f.font.bold = True
    p_f.font.color.rgb = PRIMARY_BLUE
    p_f.alignment = PP_ALIGN.CENTER

    # ==========================================
    # SLIDE 2: Motivation & Paradigm Shift
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    set_background(s2)
    add_header(s2, "Motivation: OS Virtualization vs. Hardware Emulation", "Problem Statement & Concepts")

    add_card(s2, Inches(0.8), Inches(1.75), Inches(5.6), Inches(4.0), 
             "Traditional Virtual Machines (Hypervisors)", 
             [
                 "Virtualizes the physical hardware layer via a hypervisor (Type-1/2).",
                 "Requires a dedicated, redundant guest OS kernel per instance.",
                 "High memory footprint (1 - 4 GB) and slow boot latency (30 - 60s).",
                 "Incurs hardware emulation translation penalties and CPU traps.",
                 "Rigid, coarse-grained hardware resource partitioning."
             ], 
             AMBER)

    add_card(s2, Inches(6.8), Inches(1.75), Inches(5.6), Inches(4.0), 
             "OS-Level Containers (mini-container in C)", 
             [
                 "Shares the single underlying host Linux kernel with zero emulation.",
                 "Containers are regular OS processes wrapped in kernel-enforced limits.",
                 "Sub-second boot times (10-20ms) and minimal RAM overhead (~5MB).",
                 "Near-native bare-metal execution performance with hardware quotas.",
                 "Fine-grained dynamic control via modern Linux Cgroups v2."
             ], 
             EMERALD)

    # Visual Representation Bar at bottom
    rep_bar = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.95), Inches(11.6), Inches(0.95))
    rep_bar.fill.solid()
    rep_bar.fill.fore_color.rgb = WHITE
    rep_bar.line.color.rgb = CARD_SHADOW_BORDER
    tf_rb = rep_bar.text_frame
    tf_rb.word_wrap = True
    p_rb = tf_rb.paragraphs[0]
    p_rb.text = "EFFICIENCY COMPARISON REPRESENTATION"
    p_rb.font.size = Pt(10)
    p_rb.font.bold = True
    p_rb.font.color.rgb = PRIMARY_BLUE
    p_rb2 = tf_rb.add_paragraph()
    p_rb2.text = "Boot Latency: VM (45,000 ms) vs. Container (15 ms)  |  RAM Overhead: VM (~1500 MB) vs. Container (< 5 MB)  |  CPU Overhead: ~0.1%"
    p_rb2.font.size = Pt(11)
    p_rb2.font.color.rgb = NAVY_DARK

    # ==========================================
    # SLIDE 3: Course Outcomes Alignment Matrix
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    set_background(s3)
    add_header(s3, "Syllabus Alignment: Complete CO 1 to CO 5 Coverage", "Course Outcomes Matrix")

    rows = 6
    cols = 3
    table_shape = s3.shapes.add_table(rows, cols, Inches(0.8), Inches(1.75), Inches(11.7), Inches(5.0))
    table = table_shape.table
    table.columns[0].width = Inches(3.2)
    table.columns[1].width = Inches(4.5)
    table.columns[2].width = Inches(4.0)

    headers = ["Course Outcome (CO)", "Syllabus Topics Covered", "Implementation Mechanism in C"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = PRIMARY_BLUE
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = WHITE

    matrix_data = [
        ("CO: 1 OS Principles & Processes", "System calls, User/Kernel modes, PCB, Process creation", "clone() with isolated stack, waitpid(), custom PCB handling"),
        ("CO: 2 CPU Scheduling", "CFS quotas, Preemption, Proportional Fair Share", "cgroups cpu.max (40% quota) & cpu.weight (4:1 contest)"),
        ("CO: 3 Concurrency & IPC", "Synchronization primitives, Semaphores, Shared Memory", "POSIX sem_t (mutex, empty, full) & mmap ring buffer"),
        ("CO: 4 Memory Management", "Virtual memory, Demand paging, Page faults, OOM", "cgroups memory.max, pgfault tracking (7,705 faults), SIGKILL"),
        ("CO: 5 Virtualization & Filesystems", "Container virtualization, Mount propagation, VFS", "Namespaces (PID, UTS, Mount, IPC), chroot(), private /proc")
    ]

    for row_idx, data in enumerate(matrix_data):
        for col_idx, val in enumerate(data):
            cell = table.cell(row_idx + 1, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if (row_idx % 2 == 0) else RGBColor(241, 245, 249)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(11)
            p.font.color.rgb = NAVY_DARK

    # ==========================================
    # SLIDE 4: Architecture & Lifecycle
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    set_background(s4)
    add_header(s4, "System Architecture & Execution Lifecycle", "Process Lifecycle Flow")

    add_card(s4, Inches(0.8), Inches(1.75), Inches(5.6), Inches(5.1), 
             "Coordinated Execution Pipeline", 
             [
                 "1. CLI Parsing: Processes flags (--memory 30M, --cpu 40, --pids 10).",
                 "2. Child Stack Allocation: 1MB isolated stack allocated via malloc().",
                 "3. POSIX Sync Pipe: pipe(sync_pipe) opened to eliminate race conditions.",
                 "4. clone() Syscall: Dispatches child with CLONE_NEW* namespace flags.",
                 "5. Cgroups Attachment: Parent writes child PID to cgroup.procs.",
                 "6. Controller Envelopes: Sets memory.max, cpu.max, and pids.max.",
                 "7. Handshake Signal: Parent writes trigger byte to unblock child.",
                 "8. Sandbox Execution: Child sets hostname, chroot(), execvp().",
                 "9. Post-Execution Accounting: Reads memory.stat, logs page faults."
             ], 
             PRIMARY_BLUE)

    add_card(s4, Inches(6.8), Inches(1.75), Inches(5.6), Inches(5.1), 
             "Architectural Safety Guarantees", 
             [
                 "Barrier Synchronization: The child process pauses on read(pipe[0]) until the parent confirms cgroup bounds are active.",
                 "Mount Privacy (MS_PRIVATE): Prevents container mounts (/proc, rootfs) from leaking into the host operating system.",
                 "Automated Resource Reclamation: Parent captures termination signals (OOM SIGKILL) via waitpid() and removes temporary cgroups.",
                 "Zero-Dependency Engineering: Built with pure C99 and native Linux system calls without third-party runtime frameworks."
             ], 
             INDIGO)

    # ==========================================
    # SLIDE 5: Core Mechanisms (3 Pillars)
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    set_background(s5)
    add_header(s5, "Core Isolation Subsystems: The Three Pillars", "Kernel Subsystems")

    add_card(s5, Inches(0.8), Inches(1.75), Inches(3.7), Inches(5.1), 
             "1. Namespaces (Visibility)", 
             [
                 "Controls what the process can SEE.",
                 "CLONE_NEWPID: Virtualizes process tree; child becomes PID 1; host tasks hidden.",
                 "CLONE_NEWUTS: Isolates nodename/hostname without altering host identity.",
                 "CLONE_NEWNS: Isolates Virtual File System (VFS) mount table.",
                 "CLONE_NEWIPC: Isolates POSIX and System V message queues & semaphores."
             ], 
             PRIMARY_BLUE)

    add_card(s5, Inches(4.8), Inches(1.75), Inches(3.7), Inches(5.1), 
             "2. Cgroups v2 (Resources)", 
             [
                 "Controls what the process can USE.",
                 "memory.max: Strict RAM ceiling; triggers kernel OOM Killer.",
                 "cpu.max: CFS scheduler bandwidth quota (e.g. 40% compute cap).",
                 "cpu.weight: Proportional fair-share scheduling (1 - 10000).",
                 "pids.max: Prevents process table saturation & fork bombs."
             ], 
             INDIGO)

    add_card(s5, Inches(8.8), Inches(1.75), Inches(3.7), Inches(5.1), 
             "3. Rootfs Sandboxing", 
             [
                 "Controls where the process can TOUCH.",
                 "Alpine Linux Rootfs: Lightweight ~3.5MB container userland.",
                 "chroot(): Confines process inside container directory tree.",
                 "Private /proc: Pseudo-filesystem isolated to container PID 1.",
                 "Prevents traversal into host root filesystems."
             ], 
             EMERALD)

    # ==========================================
    # SLIDE 6: Concurrency & IPC Synchronization (Replacing Viva Slide!)
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    set_background(s6)
    add_header(s6, "Classical Concurrency & IPC Synchronization (CO: 3)", "Concurrency Primitives")

    add_card(s6, Inches(0.8), Inches(1.75), Inches(5.6), Inches(5.1), 
             "Producer-Consumer with Semaphores (sem_t)", 
             [
                 "Classical Bounded-Buffer Concurrency Problem implemented inside the container sandbox.",
                 "Binary Semaphore (mutex): Initialized to 1; enforces mutual exclusion for the critical section.",
                 "Counting Semaphore (empty_slots): Initialized to buffer capacity (N = 5).",
                 "Counting Semaphore (full_slots): Initialized to 0 items available.",
                 "Shared Memory (mmap): Allocated via MAP_SHARED | MAP_ANONYMOUS across processes.",
                 "Result: All 10 operations exchanged with zero race conditions or buffer corruption."
             ], 
             EMERALD)

    add_card(s6, Inches(6.8), Inches(1.75), Inches(5.6), Inches(5.1), 
             "Parent-Child IPC Pipe Synchronization", 
             [
                 "The Race Condition Hazard: Cloned child process could execute payload before parent attaches cgroups limits.",
                 "The POSIX Pipe Solution: Parent and child share a unidirectional sync_pipe[2].",
                 "Child Execution: Calls read(sync_pipe[0]) and immediately BLOCKS.",
                 "Parent Execution: Completes cgroup setup, then writes single trigger byte 'G'.",
                 "Unblocking: Child receives byte, closes pipe, and proceeds safely to execvp().",
                 "Ensures deterministic, race-free resource limits from microsecond zero."
             ], 
             PRIMARY_BLUE)

    # ==========================================
    # SLIDE 7: Empirical Laboratory Benchmarks & Observed Results
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    set_background(s7)
    add_header(s7, "Empirical Laboratory Benchmarks & Verification", "Observed Metrics")

    # 4 Scorecard Cards
    # Card 1: PID Isolation
    c1 = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.75), Inches(5.6), Inches(2.4))
    c1.fill.solid()
    c1.fill.fore_color.rgb = WHITE
    c1.line.color.rgb = PRIMARY_BLUE
    c1.line.width = Pt(1.5)
    tf_c1 = c1.text_frame
    tf_c1.word_wrap = True
    p = tf_c1.paragraphs[0]
    p.text = "1. Process Virtualization (CO: 1 & 5)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE
    p_b = tf_c1.add_paragraph()
    p_b.text = "• Container Process reports PID = 1; Parent PID = 0.\n• Host operating system processes (47 active) are completely hidden.\n• Hostname virtualized to 'isolated-box' without altering host."
    p_b.font.size = Pt(11)
    p_b.font.color.rgb = NAVY_DARK

    # Card 2: Memory OOM & Page Faults
    c2 = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.75), Inches(5.6), Inches(2.4))
    c2.fill.solid()
    c2.fill.fore_color.rgb = WHITE
    c2.line.color.rgb = AMBER
    c2.line.width = Pt(1.5)
    tf_c2 = c2.text_frame
    tf_c2.word_wrap = True
    p = tf_c2.paragraphs[0]
    p.text = "2. Memory Ceiling & Demand Paging (CO: 4)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = AMBER
    p_b = tf_c2.add_paragraph()
    p_b.text = "• Workload allocated 30MB of 60MB; terminated by SIGKILL (signal 9).\n• Kernel logged 7,705 Minor Page Faults, validating Demand Paging.\n• 1 Major Page Fault; Swap disabled to force immediate OOM protection."
    p_b.font.size = Pt(11)
    p_b.font.color.rgb = NAVY_DARK

    # Card 3: Proportional CPU Contest
    c3 = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.4), Inches(5.6), Inches(2.4))
    c3.fill.solid()
    c3.fill.fore_color.rgb = WHITE
    c3.line.color.rgb = INDIGO
    c3.line.width = Pt(1.5)
    tf_c3 = c3.text_frame
    tf_c3.word_wrap = True
    p = tf_c3.paragraphs[0]
    p.text = "3. Proportional Fair-Share CPU Contest (CO: 2)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = INDIGO
    p_b = tf_c3.add_paragraph()
    p_b.text = "• Competing containers on CPU Core 0 with CFS weights 800 vs 200.\n• Container A CPU Time: 2.78s  |  Container B CPU Time: 0.69s.\n• Exact 4.02 : 1 execution ratio (matches theoretical 4:1 with 99.5% accuracy!)."
    p_b.font.size = Pt(11)
    p_b.font.color.rgb = NAVY_DARK

    # Card 4: Fork Bomb Mitigation
    c4 = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(4.4), Inches(5.6), Inches(2.4))
    c4.fill.solid()
    c4.fill.fore_color.rgb = WHITE
    c4.line.color.rgb = EMERALD
    c4.line.width = Pt(1.5)
    tf_c4 = c4.text_frame
    tf_c4.word_wrap = True
    p = tf_c4.paragraphs[0]
    p.text = "4. Fork Bomb & PCB Table Defense (CO: 1 & 3)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = EMERALD
    p_b = tf_c4.add_paragraph()
    p_b.text = "• Stress test attempted to spawn 50 concurrent processes.\n• Cgroups pids.max = 10 capped execution; Children 1 - 9 spawned.\n• 10th fork() blocked with errno 11 (EAGAIN); host OS remained responsive."
    p_b.font.size = Pt(11)
    p_b.font.color.rgb = NAVY_DARK

    # ==========================================
    # SLIDE 8: Summary & Interactive Evaluation
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    set_background(s8)

    # Header Tag
    b8 = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.3), Inches(1.1), Inches(4.7), Inches(0.45))
    b8.fill.solid()
    b8.fill.fore_color.rgb = RGBColor(224, 242, 254)
    b8.line.color.rgb = PRIMARY_BLUE
    p = b8.text_frame.paragraphs[0]
    p.text = "EVALUATION & LIVE DEMONSTRATION"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE
    p.alignment = PP_ALIGN.CENTER

    tb8 = s8.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(11.33), Inches(1.5))
    tf8 = tb8.text_frame
    tf8.word_wrap = True
    p8_t = tf8.paragraphs[0]
    p8_t.text = "Interactive Project Demonstration"
    p8_t.font.size = Pt(36)
    p8_t.font.bold = True
    p8_t.font.color.rgb = NAVY_DARK
    p8_t.alignment = PP_ALIGN.CENTER

    p8_s = tf8.add_paragraph()
    p8_s.text = "Complete C99 Runtime Covering CO: 1 to CO: 5 with Master Interactive Menu and Real-Time Kernel Metrics"
    p8_s.font.size = Pt(15)
    p8_s.font.color.rgb = NAVY_MUTED
    p8_s.alignment = PP_ALIGN.CENTER
    p8_s.space_before = Pt(8)

    # Command Box representation
    cmd_box = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(3.2), Inches(3.5), Inches(6.93), Inches(1.3))
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

    # Team & Links
    tb_footer = s8.shapes.add_textbox(Inches(1.0), Inches(5.1), Inches(11.33), Inches(1.5))
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
    print(f"[Success] Saved bright-theme presentation to {output_path}")

if __name__ == "__main__":
    create_presentation()
