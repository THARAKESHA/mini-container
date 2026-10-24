import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    # Colors
    BG_COLOR = RGBColor(11, 15, 25)        # #0b0f19
    CARD_BG = RGBColor(21, 29, 48)         # #151d30
    CARD_BORDER = RGBColor(36, 51, 84)     # #243354
    PRIMARY = RGBColor(56, 189, 248)       # #38bdf8 (Cyan)
    SECONDARY = RGBColor(129, 140, 248)    # #818cf8 (Indigo)
    ACCENT = RGBColor(52, 211, 153)        # #34d399 (Emerald)
    TEXT_MAIN = RGBColor(241, 245, 249)    # #f1f5f9
    TEXT_MUTED = RGBColor(148, 163, 184)   # #94a3b8

    def set_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.color.rgb = BG_COLOR
        return bg

    def add_header(slide, title_text, category_text):
        # Category tag
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.5), Inches(0.4))
        tf_c = cat_box.text_frame
        tf_c.word_wrap = True
        p_c = tf_c.paragraphs[0]
        p_c.text = category_text.upper()
        p_c.font.size = Pt(11)
        p_c.font.bold = True
        p_c.font.color.rgb = SECONDARY

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.5), Inches(0.7))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.size = Pt(24)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_MAIN

        # Divider line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.45), Inches(11.7), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = CARD_BORDER
        line.line.color.rgb = CARD_BORDER

    def add_card(slide, left, top, width, height, title, items, title_color=PRIMARY):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1.5)

        tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), width - Inches(0.4), height - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.size = Pt(16)
        p0.font.bold = True
        p0.font.color.rgb = title_color
        p0.space_after = Pt(10)

        for item in items:
            p = tf.add_paragraph()
            p.text = f"•  {item}"
            p.font.size = Pt(13)
            p.font.color.rgb = TEXT_MAIN
            p.space_after = Pt(8)

    # ==========================================
    # SLIDE 1: Title Slide
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    set_background(s1)

    # Badge
    b1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.5), Inches(0.9), Inches(4.33), Inches(0.45))
    b1.fill.solid()
    b1.fill.fore_color.rgb = RGBColor(15, 35, 60)
    b1.line.color.rgb = PRIMARY
    b1.text = "OPERATING SYSTEMS PROJECT REVIEW"
    p = b1.text_frame.paragraphs[0]
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = PRIMARY
    p.alignment = PP_ALIGN.CENTER

    # Title & Subtitle
    tb1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.33), Inches(1.8))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p_title = tf1.paragraphs[0]
    p_title.text = "Mini-Container Runtime"
    p_title.font.size = Pt(40)
    p_title.font.bold = True
    p_title.font.color.rgb = PRIMARY
    p_title.alignment = PP_ALIGN.CENTER

    p_sub = tf1.add_paragraph()
    p_sub.text = "A Lightweight Linux Container Virtualization Engine Built from Scratch in C99\nUsing Linux Namespaces and Unified Cgroups v2"
    p_sub.font.size = Pt(17)
    p_sub.font.color.rgb = TEXT_MUTED
    p_sub.alignment = PP_ALIGN.CENTER
    p_sub.space_before = Pt(10)

    # Team Members Cards
    # Member 1
    m1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2.2), Inches(3.7), Inches(4.2), Inches(2.1))
    m1.fill.solid()
    m1.fill.fore_color.rgb = CARD_BG
    m1.line.color.rgb = PRIMARY
    m1.line.width = Pt(2)
    tf_m1 = m1.text_frame
    tf_m1.word_wrap = True
    p1 = tf_m1.paragraphs[0]
    p1.text = "TEAM MEMBER 1"
    p1.font.size = Pt(10)
    p1.font.bold = True
    p1.font.color.rgb = SECONDARY
    p2 = tf_m1.add_paragraph()
    p2.text = "Tharakesha M"
    p2.font.size = Pt(19)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_MAIN
    p3 = tf_m1.add_paragraph()
    p3.text = "Reg No: 24BCE2538\nB.Tech Computer Science & Engineering"
    p3.font.size = Pt(12)
    p3.font.color.rgb = PRIMARY
    p3.space_before = Pt(4)

    # Member 2
    m2 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(3.7), Inches(4.2), Inches(2.1))
    m2.fill.solid()
    m2.fill.fore_color.rgb = CARD_BG
    m2.line.color.rgb = SECONDARY
    m2.line.width = Pt(2)
    tf_m2 = m2.text_frame
    tf_m2.word_wrap = True
    p1_2 = tf_m2.paragraphs[0]
    p1_2.text = "TEAM MEMBER 2"
    p1_2.font.size = Pt(10)
    p1_2.font.bold = True
    p1_2.font.color.rgb = SECONDARY
    p2_2 = tf_m2.add_paragraph()
    p2_2.text = "Mathu Metha S"
    p2_2.font.size = Pt(19)
    p2_2.font.bold = True
    p2_2.font.color.rgb = TEXT_MAIN
    p3_2 = tf_m2.add_paragraph()
    p3_2.text = "Reg No: 24BCE2805\nB.Tech Computer Science & Engineering"
    p3_2.font.size = Pt(12)
    p3_2.font.color.rgb = SECONDARY
    p3_2.space_before = Pt(4)

    # Footer
    fb = s1.shapes.add_textbox(Inches(1.0), Inches(6.3), Inches(11.33), Inches(0.6))
    tf_f = fb.text_frame
    p_f = tf_f.paragraphs[0]
    p_f.text = "Repository: https://github.com/THARAKESHA/mini-container"
    p_f.font.size = Pt(13)
    p_f.font.color.rgb = PRIMARY
    p_f.alignment = PP_ALIGN.CENTER

    # ==========================================
    # SLIDE 2: Problem Statement & Motivation
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    set_background(s2)
    add_header(s2, "Motivation: Containers vs. Virtual Machines", "Concept & Objectives")

    add_card(s2, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.9), 
             "Traditional Virtual Machines (VMs)", 
             [
                 "Virtualize the hardware layer using a hypervisor (Type-1/Type-2).",
                 "Requires a separate, complete guest OS kernel per virtual machine.",
                 "High memory footprint (Gigabytes) and slow multi-second boot latency.",
                 "Incurs hardware emulation translation penalties and CPU overhead.",
                 "Resource limits are rigid and coarse-grained."
             ], 
             RGBColor(245, 158, 11))

    add_card(s2, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.9), 
             "OS-Level Containers (mini-container)", 
             [
                 "Shares the single underlying host Linux kernel with zero emulation.",
                 "Containers are regular OS processes wrapped in kernel-enforced boundaries.",
                 "Sub-second boot times (10-20ms) and minimal RAM overhead (Megabytes).",
                 "Near-native bare-metal execution performance.",
                 "Cgroups v2 enforces dynamic CPU quotas, memory ceilings, and task limits."
             ], 
             ACCENT)

    # ==========================================
    # SLIDE 3: Course Outcomes Alignment Matrix
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    set_background(s3)
    add_header(s3, "Syllabus Alignment: Complete CO 1 to CO 5 Coverage", "Course Outcomes Matrix")

    # Table
    rows = 6
    cols = 3
    table_shape = s3.shapes.add_table(rows, cols, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.8))
    table = table_shape.table
    table.columns[0].width = Inches(3.2)
    table.columns[1].width = Inches(4.5)
    table.columns[2].width = Inches(4.0)

    headers = ["Course Outcome (CO)", "Syllabus Topics Covered", "Implementation Mechanism in C"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(30, 41, 59)
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = PRIMARY

    matrix_data = [
        ("CO: 1 OS Principles & Processes", "System calls, User/Kernel modes, PCB, Process creation", "clone() with isolated stack, waitpid(), custom PCB"),
        ("CO: 2 CPU Scheduling", "CFS quotas, Preemption, Proportional Fair Share", "cgroups cpu.max (40% quota) & cpu.weight (4:1 contest)"),
        ("CO: 3 Concurrency & IPC", "Synchronization primitives, Semaphores, Shared Memory", "POSIX sem_t (mutex, empty, full) & mmap ring buffer"),
        ("CO: 4 Memory Management", "Virtual memory, Demand paging, Page faults, OOM", "cgroups memory.max, pgfault tracking (7,705 faults), SIGKILL"),
        ("CO: 5 Virtualization & Filesystems", "Container virtualization, Mount propagation, VFS", "Namespaces (PID, UTS, Mount, IPC), chroot(), private /proc")
    ]

    for row_idx, data in enumerate(matrix_data):
        for col_idx, val in enumerate(data):
            cell = table.cell(row_idx + 1, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = CARD_BG
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(11)
            p.font.color.rgb = TEXT_MAIN

    # ==========================================
    # SLIDE 4: Architecture & Lifecycle
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    set_background(s4)
    add_header(s4, "System Architecture & Execution Flow", "Process Lifecycle")

    add_card(s4, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.9), 
             "Execution Lifecycle Flow", 
             [
                 "1. CLI Invocation: Parses arguments (--memory, --cpu, --pids, etc.)",
                 "2. Host Parent: Allocates 1MB stack & creates POSIX sync pipe.",
                 "3. clone() Syscall: Dispatches child with CLONE_NEW* namespace flags.",
                 "4. Cgroups Binding: Parent creates /sys/fs/cgroup/minicontainer-[PID].",
                 "5. Sync Barrier: Parent signals child via pipe (eliminates race condition).",
                 "6. Sandbox Init: Child sethostname(), chroot(), mounts private /proc.",
                 "7. Execution: Child calls execvp(), becomes PID 1 inside container.",
                 "8. Teardown: Parent waitpid() catches exit/OOM kill, cleans cgroups."
             ], 
             PRIMARY)

    add_card(s4, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.9), 
             "Key Engineering Highlights", 
             [
                 "Race-Free Attachment: Child blocks on pipe until parent establishes cgroup limits, preventing unconstrained child execution.",
                 "VFS Isolation: Mount propagation set to MS_PRIVATE to prevent container mount events from leaking into the host OS.",
                 "Kernel Accounting: Reads memory.stat upon exit to capture peak RAM, minor page faults, and major page faults.",
                 "Zero-Dependency: Written entirely in C99 with native POSIX syscalls; runs on any standard Linux kernel 5.x/6.x."
             ], 
             SECONDARY)

    # ==========================================
    # SLIDE 5: Core Mechanisms
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    set_background(s5)
    add_header(s5, "Core Isolation Primitives in Linux", "Kernel Subsystems")

    add_card(s5, Inches(0.8), Inches(1.8), Inches(3.7), Inches(4.9), 
             "1. Namespaces (Visibility)", 
             [
                 "What the process can SEE.",
                 "CLONE_NEWPID: Child becomes PID 1; host processes hidden.",
                 "CLONE_NEWUTS: Independent hostname without altering host OS.",
                 "CLONE_NEWNS: Decouples VFS mount table.",
                 "CLONE_NEWIPC: Separate System V / POSIX IPC queues."
             ], 
             PRIMARY)

    add_card(s5, Inches(4.8), Inches(1.8), Inches(3.7), Inches(4.9), 
             "2. Cgroups v2 (Resources)", 
             [
                 "What the process can USE.",
                 "memory.max: Strict RAM ceiling; triggers kernel OOM Killer.",
                 "cpu.max: CFS scheduler bandwidth quota (e.g. 40% cap).",
                 "cpu.weight: Proportional fair-share scheduling (1-10000).",
                 "pids.max: Prevents fork bomb process exhaustion."
             ], 
             SECONDARY)

    add_card(s5, Inches(8.8), Inches(1.8), Inches(3.7), Inches(4.9), 
             "3. Rootfs Sandboxing", 
             [
                 "Where the process can TOUCH.",
                 "Alpine Linux Rootfs: Lightweight ~3.5MB userland.",
                 "chroot(): Cages process inside container directory tree.",
                 "Private /proc: Pseudo-filesystem isolated to container PID 1.",
                 "Prevents host directory traversal."
             ], 
             ACCENT)

    # ==========================================
    # SLIDE 6: Empirical Results & Live Verification
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    set_background(s6)
    add_header(s6, "Empirical Results & Live Verification", "Laboratory Benchmarks")

    add_card(s6, Inches(0.8), Inches(1.8), Inches(5.6), Inches(2.35), 
             "1. PID & Hostname Isolation (CO: 1 & 5)", 
             [
                 "Command: sudo ./minicontainer run ./tests/test_info",
                 "Result: Child reports PID = 1; Parent PID = 0.",
                 "Host processes (47 running) are completely hidden."
             ], 
             PRIMARY)

    add_card(s6, Inches(6.8), Inches(1.8), Inches(5.6), Inches(2.35), 
             "2. Memory Limit & OOM Killer (CO: 4)", 
             [
                 "Command: sudo ./minicontainer run --memory 30M ./tests/test_memory 60",
                 "Result: Process terminated by SIGKILL (signal 9).",
                 "Recorded 7,705 Minor Page Faults proving Demand Paging!"
             ], 
             RGBColor(245, 158, 11))

    add_card(s6, Inches(0.8), Inches(4.35), Inches(5.6), Inches(2.35), 
             "3. CPU Fair-Share Contest (CO: 2)", 
             [
                 "Command: sudo bash scripts/test_cpu_shares.sh",
                 "Result: Contest on Core 0 with Weights 800 vs 200.",
                 "CPU Time: 2.78s vs 0.69s -> Exact 4.02 : 1 execution ratio!"
             ], 
             SECONDARY)

    add_card(s6, Inches(6.8), Inches(4.35), Inches(5.6), Inches(2.35), 
             "4. Concurrency & Semaphores (CO: 3)", 
             [
                 "Command: sudo ./minicontainer run ./tests/test_ipc_sync",
                 "Result: 10 items exchanged via sem_t (mutex, empty, full).",
                 "Shared memory ring buffer executed with zero race conditions."
             ], 
             ACCENT)

    # ==========================================
    # SLIDE 7: Technical Review & Viva Defense
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    set_background(s7)
    add_header(s7, "Technical Review & Viva Voce Defense", "Evaluator Q&A")

    add_card(s7, Inches(0.8), Inches(1.8), Inches(5.6), Inches(2.35), 
             "Q1: Why clone() instead of fork()?", 
             [
                 "fork() duplicates the process within identical namespaces.",
                 "clone() accepts flags like CLONE_NEWPID and CLONE_NEWUTS to instantiate the child inside brand-new, isolated kernel namespaces."
             ], 
             PRIMARY)

    add_card(s7, Inches(6.8), Inches(1.8), Inches(5.6), Inches(2.35), 
             "Q2: Why did memory limit trigger SIGKILL?", 
             [
                 "Linux uses optimistic memory overcommit & demand paging.",
                 "When memset() committed physical pages exceeding memory.max with swap disabled, the kernel OOM Killer dispatched SIGKILL."
             ], 
             SECONDARY)

    add_card(s7, Inches(0.8), Inches(4.35), Inches(5.6), Inches(2.35), 
             "Q3: Why is an IPC pipe needed between parent & child?", 
             [
                 "To eliminate a critical race condition. The child must not call execvp() before the parent finishes creating cgroups and attaching the child's PID."
             ], 
             ACCENT)

    add_card(s7, Inches(6.8), Inches(4.35), Inches(5.6), Inches(2.35), 
             "Q4: How did you prove CPU scheduling fairness?", 
             [
                 "Two containers with CFS weights 800 vs 200 ran concurrently on CPU 0. CFS allocated 2.78s and 0.69s, verifying the theoretical 4:1 ratio with 99.5% accuracy."
             ], 
             PRIMARY)

    # ==========================================
    # SLIDE 8: Summary & Live Demo Command
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    set_background(s8)

    # Badge
    b8 = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.5), Inches(1.2), Inches(4.33), Inches(0.45))
    b8.fill.solid()
    b8.fill.fore_color.rgb = RGBColor(15, 35, 60)
    b8.line.color.rgb = PRIMARY
    b8.text = "EVALUATION DASHBOARD"
    p = b8.text_frame.paragraphs[0]
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = PRIMARY
    p.alignment = PP_ALIGN.CENTER

    tb8 = s8.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.33), Inches(1.5))
    tf8 = tb8.text_frame
    tf8.word_wrap = True
    p8_t = tf8.paragraphs[0]
    p8_t.text = "Ready for Live Demonstration"
    p8_t.font.size = Pt(36)
    p8_t.font.bold = True
    p8_t.font.color.rgb = PRIMARY
    p8_t.alignment = PP_ALIGN.CENTER

    p8_s = tf8.add_paragraph()
    p8_s.text = "Complete C Runtime Covering CO: 1 to CO: 5 with Master Interactive Menu and Real-Time Kernel Metrics"
    p8_s.font.size = Pt(16)
    p8_s.font.color.rgb = TEXT_MUTED
    p8_s.alignment = PP_ALIGN.CENTER
    p8_s.space_before = Pt(8)

    # Command Box
    cmd_box = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(3.2), Inches(3.5), Inches(6.93), Inches(1.2))
    cmd_box.fill.solid()
    cmd_box.fill.fore_color.rgb = RGBColor(9, 13, 22)
    cmd_box.line.color.rgb = PRIMARY
    cmd_box.line.width = Pt(2)
    tf_cmd = cmd_box.text_frame
    p_cmd = tf_cmd.paragraphs[0]
    p_cmd.text = "$ sudo bash interactive_menu.sh"
    p_cmd.font.size = Pt(22)
    p_cmd.font.bold = True
    p_cmd.font.color.rgb = PRIMARY
    p_cmd.alignment = PP_ALIGN.CENTER
    p_cmd_sub = tf_cmd.add_paragraph()
    p_cmd_sub.text = "(Or double-click Run-MiniContainer.bat on Windows Desktop)"
    p_cmd_sub.font.size = Pt(12)
    p_cmd_sub.font.color.rgb = TEXT_MUTED
    p_cmd_sub.alignment = PP_ALIGN.CENTER

    # Team & Links
    tb_footer = s8.shapes.add_textbox(Inches(1.0), Inches(5.0), Inches(11.33), Inches(1.5))
    tf_foot = tb_footer.text_frame
    p_team = tf_foot.paragraphs[0]
    p_team.text = "Project Team: Tharakesha M (24BCE2538) & Mathu Metha S (24BCE2805)"
    p_team.font.size = Pt(16)
    p_team.font.bold = True
    p_team.font.color.rgb = TEXT_MAIN
    p_team.alignment = PP_ALIGN.CENTER

    p_git = tf_foot.add_paragraph()
    p_git.text = "GitHub Repository: https://github.com/THARAKESHA/mini-container"
    p_git.font.size = Pt(14)
    p_git.font.color.rgb = SECONDARY
    p_git.alignment = PP_ALIGN.CENTER
    p_git.space_before = Pt(6)

    # Save
    output_path = os.path.join(os.path.dirname(__file__), "..", "presentation.pptx")
    prs.save(output_path)
    print(f"[Success] Saved presentation to {output_path}")

if __name__ == "__main__":
    create_presentation()
