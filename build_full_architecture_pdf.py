import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))

        # Header (Pages 2+)
        if self._pageNumber > 1:
            self.drawString(36, 756, "SUPER MARIO BROS PCG & DDA FRAMEWORK — ARCHITECTURE & DFD SPECIFICATION")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(36, 750, 576, 750)

        # Footer (All pages)
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(576, 25, page_str)
        self.drawString(36, 25, "SUPER MARIO BROS PCG & DDA ADAPTIVE ENGINE — SYSTEM TECHNICAL SPECIFICATION")
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(36, 35, 576, 35)

        self.restoreState()


def create_architecture_pdf(filename="PROJECT_ARCHITECTURE_AND_DFD.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    # Custom Color Palette
    c_primary = colors.HexColor("#1e293b")    # Slate 800
    c_secondary = colors.HexColor("#334155")  # Slate 700
    c_accent = colors.HexColor("#4f46e5")     # Indigo 600
    c_accent_gold = colors.HexColor("#d97706")# Amber 600
    c_text = colors.HexColor("#0f172a")       # Slate 900
    c_light_bg = colors.HexColor("#f8fafc")   # Slate 50
    c_callout_bg = colors.HexColor("#f1f5f9") # Slate 100
    c_border = colors.HexColor("#cbd5e1")     # Slate 300

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=c_primary,
        alignment=TA_CENTER,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=c_accent,
        alignment=TA_CENTER,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'H1Style',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12.5,
        leading=15.5,
        textColor=c_primary,
        spaceBefore=12,
        spaceAfter=5,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2Style',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=c_secondary,
        spaceBefore=9,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.8,
        textColor=c_text,
        alignment=TA_JUSTIFY,
        spaceAfter=4.5
    )

    bullet_style = ParagraphStyle(
        'BulletStyle',
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3,
        alignment=TA_LEFT
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Code'],
        fontName='Courier',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#0f172a"),
        backColor=c_light_bg,
        borderColor=c_border,
        borderWidth=0.5,
        borderPadding=3,
        spaceBefore=3,
        spaceAfter=4
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=body_style,
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=11.5,
        textColor=c_secondary,
        alignment=TA_LEFT
    )

    story = []

    # ================= HEADER BANNER =================
    story.append(Paragraph("SUPER MARIO BROS PCG & DDA FRAMEWORK", title_style))
    story.append(Paragraph("COMPREHENSIVE TECHNICAL ARCHITECTURE, DATA FLOW DIAGRAMS (DFDs) & SYSTEM MODULES SPECIFICATION", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceBefore=0, spaceAfter=10))

    # ================= SECTION 1: EXECUTIVE OVERVIEW & ARCHITECTURE =================
    story.append(Paragraph("1. Executive Overview & System Architecture", h1_style))
    story.append(Paragraph(
        "This document provides the definitive, complete technical specification of the <b>Super Mario Bros Trajectory-Conditioned Procedural Content Generation (PCG) & Bayesian Cumulative Dynamic Difficulty Adjustment (DDA) Framework</b>. "
        "The system transitions procedural level generation from static, single-level algorithms into an adaptive, multi-level campaign generator. "
        "Levels are generated dynamically to match designer-specified pacing curves (e.g. Linear Ramp, Spike & Recovery, Sawtooth Wave, Boss Rush) while continuously calibrating difficulty in real-time based on cumulative human gameplay telemetry.",
        body_style
    ))

    story.append(Paragraph("1.1 Layered System Architecture", h2_style))
    story.append(Paragraph(
        "The framework is built upon a 4-tier decoupled architecture separating presentation, orchestration, procedural intelligence, and native game engine execution:",
        body_style
    ))

    arch_layers = [
        [Paragraph("<b>Architecture Layer</b>", body_style), Paragraph("<b>Components & Technologies</b>", body_style), Paragraph("<b>Key Responsibilities</b>", body_style)],
        [
            Paragraph("<b>1. Presentation Layer</b>", body_style),
            Paragraph("HTML5, Vanilla CSS3 (Glassmorphism), Chart.js, HTML Canvas API", body_style),
            Paragraph("Interactive Difficulty Curve Designer, Tile Grid Visualizer, Proportional Spinner Loading Screen, Cumulative Death Zone Heatmap Canvas, Player Arcade Campaign Workspace.", body_style)
        ],
        [
            Paragraph("<b>2. REST API & Controller Layer</b>", body_style),
            Paragraph("Python 3.13, Flask WSGI Engine, Subprocess IPC", body_style),
            Paragraph("RESTful endpoints for campaign generation, interactive Java game launching, death zone telemetry polling, and session progression state management.", body_style)
        ],
        [
            Paragraph("<b>3. PCG Intelligence Core</b>", body_style),
            Paragraph("2nd-Order Markov Model, VGLC Trainer, Robin Baumgarten A* Solver, Bayesian DDA Engine", body_style),
            Paragraph("Trajectory-conditioned column sampling, playability validation (&le;5% tolerance), stack block sanitization, exponential decay DDA weighting (w_i = 0.70^(n-1-i)).", body_style)
        ],
        [
            Paragraph("<b>4. Native Execution Layer</b>", body_style),
            Paragraph("Java 17, Swing AWT Window Framework, Mario-AI-Framework Engine", body_style),
            Paragraph("3.5x scaled interactive human play window, live A* agent visualizer, real-time physics engine, in-game Swing HUD (Lives/Coins), IPC result logger (<code>last_result.txt</code>).", body_style)
        ]
    ]
    t_arch = Table(arch_layers, colWidths=[110, 140, 290])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_light_bg),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_arch)
    story.append(Spacer(1, 8))

    # Architectural Structural Diagram (ASCII / Table Representation)
    story.append(Paragraph("1.2 Structural Component Interaction Diagram", h2_style))
    diag_data = [
        [Paragraph(
            "<b>[ USER / DESIGNER ]</b><br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;&vert;<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;+&mdash;&mdash;&gt; <b>Web UI (index.html)</b> &lt;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;+<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&vert; (JSON API Requests)<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;v<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Flask API Server (app.py)</b> &lt;&mdash;&mdash;&gt; <b>Campaign State (game_session.py)</b><br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&vert;<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;+&mdash;&mdash;&mdash;&mdash;+&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;+&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;+<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;v&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;v&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;v<br/>"
            "<b>PCG Pipeline</b>&nbsp;&nbsp;&nbsp;&nbsp;<b>A* Validator</b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Bayesian DDA Engine</b><br/>"
            "<code>(generator.py)</code>&nbsp;&nbsp;<code>(validator.py)</code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<code>(dda.py)</code><br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;&vert;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&vert;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&vert;<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;+&mdash;&mdash;&mdash;&mdash;+&mdash;&mdash;&mdash;&mdash;+&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;+&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;+<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&vert; (Subprocess Spawn / Level Text File)<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;v<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Java Play Engine (PlayLevel.java / MarioGame.java)</b><br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&vert; (Telemetry Log Write-out)<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;v<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>IPC Result Store (levels/last_result.txt)</b>",
            code_style
        )]
    ]
    t_diag = Table(diag_data, colWidths=[540])
    t_diag.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_callout_bg),
        ('BOX', (0,0), (-1,-1), 1, c_accent),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_diag)
    story.append(Spacer(1, 10))

    # ================= SECTION 2: DATA FLOW DIAGRAMS (DFDs) =================
    story.append(Paragraph("2. Data Flow Diagrams (DFDs)", h1_style))
    story.append(Paragraph(
        "Data Flow Diagrams model the movement, transformation, and storage of data across the system. "
        "The following diagrams document the system from high-level context (Level 0) down to granular subsystem process flows (Level 2).",
        body_style
    ))

    # 2.1 DFD Level 0 Context Diagram
    story.append(Paragraph("2.1 DFD Level 0: Context Diagram", h2_style))
    story.append(Paragraph(
        "The Context Diagram defines the global system boundary, external entities (Game Designer, Human Player), and primary input/output data streams.",
        body_style
    ))

    dfd0_data = [
        [Paragraph("<b>External Entity</b>", body_style), Paragraph("<b>Input Data Stream to System</b>", body_style), Paragraph("<b>Output Data Stream from System</b>", body_style)],
        [
            Paragraph("<b>Game Designer</b><br/>(Web UI User)", body_style),
            Paragraph("&bull; Target Difficulty Vector D = [d_1 ... d_N] (5&ndash;95)<br/>&bull; Curve Presets (Linear, Spike, Wave, Boss)<br/>&bull; Simulated Skill Profile (Novice, Average, Pro)<br/>&bull; Level Count N (3 to 10)", body_style),
            Paragraph("&bull; Rendered Chart.js Wave Graph<br/>&bull; Solvability & Difficulty Metrics<br/>&bull; Tile Grid Visualizer & Inspection<br/>&bull; Real-Time Loading Progress Spinner<br/>&bull; Session DDA Telemetry Summary", body_style)
        ],
        [
            Paragraph("<b>Human Player</b><br/>(Arcade Mode User)", body_style),
            Paragraph("&bull; Selected Unlocked Level Index<br/>&bull; Real-Time Keyboard Controls (Arrows, S, A)<br/>&bull; Campaign Reset Command (3 Lives Lost)", body_style),
            Paragraph("&bull; 3.5x Scaled Java Game Window<br/>&bull; Live Top-Left HUD (Lives: 3/2/1, Coins)<br/>&bull; Flagpole Course Clear Unlock Signal<br/>&bull; Cumulative Death Zone Heatmap Overlay", body_style)
        ]
    ]
    t_dfd0 = Table(dfd0_data, colWidths=[110, 215, 215])
    t_dfd0.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_light_bg),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_dfd0)
    story.append(Spacer(1, 10))

    # 2.2 DFD Level 1 System-Level Flow Diagram
    story.append(Paragraph("2.2 DFD Level 1: System-Level Data Flow Diagram", h2_style))
    story.append(Paragraph(
        "Level 1 decomposes Process 0.0 into 5 core functional processes, highlighting data transformations and data store interactions:",
        body_style
    ))

    dfd1_data = [
        [Paragraph("<b>Process ID & Name</b>", body_style), Paragraph("<b>Input Data Flows</b>", body_style), Paragraph("<b>Data Transformation / Operation</b>", body_style), Paragraph("<b>Output Data Flows & Data Stores</b>", body_style)],
        [
            Paragraph("<b>1.0 Sequence Generator</b>", body_style),
            Paragraph("Target Vector D, Markov Matrix Store", body_style),
            Paragraph("Conditions 2nd-order column transitions; inserts 8-step stair intros/outros; executes <code>_fix_stacked_special_blocks</code>.", body_style),
            Paragraph("Candidate Level Text &rarr; <i>Data Store: Candidate Buffer</i>", body_style)
        ],
        [
            Paragraph("<b>2.0 Solvability Validator</b>", body_style),
            Paragraph("Candidate Level Text", body_style),
            Paragraph("Spawns Robin Baumgarten A* solver; measures completion time, jump heights, gap clearance; checks &le; 5% tolerance.", body_style),
            Paragraph("Validated Level Text, Est. Diff &rarr; <i>Data Store: Active Level Store</i>", body_style)
        ],
        [
            Paragraph("<b>3.0 API & Session Controller</b>", body_style),
            Paragraph("UI Requests, Player Selections", body_style),
            Paragraph("Orchestrates pipeline execution; tracks active level index, unlocked maps, 3-life system, and coin counts.", body_style),
            Paragraph("JSON API Responses &rarr; <i>Data Store: Session State Store</i>", body_style)
        ],
        [
            Paragraph("<b>4.0 Java Play Engine</b>", body_style),
            Paragraph("Level File, Mario State, Lives", body_style),
            Paragraph("Executes real-time physics loop; renders 3.5x AWT window & HUD; detects death/win events.", body_style),
            Paragraph("<code>SESSION_UPDATE:</code> string &rarr; <i>Data Store: last_result.txt</i>", body_style)
        ],
        [
            Paragraph("<b>5.0 Bayesian DDA Engine</b>", body_style),
            Paragraph("Telemetry Data, Session History", body_style),
            Paragraph("Calculates weighted performance P_cum using w_i = 0.70^(n-1-i); computes bounded shift &Delta;d in [-0.10, +0.10].", body_style),
            Paragraph("Adjusted Target d'_{k+1} &rarr; <i>Data Store: DDA History Store</i>", body_style)
        ]
    ]
    t_dfd1 = Table(dfd1_data, colWidths=[110, 110, 180, 140])
    t_dfd1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_light_bg),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_dfd1)
    story.append(Spacer(1, 10))

    # 2.3 DFD Level 2 Detailed Process Flow Diagrams
    story.append(Paragraph("2.3 DFD Level 2: Detailed Process Flow Breakdown", h2_style))
    story.append(Paragraph(
        "Level 2 details the internal sub-process mechanics of critical system operations:",
        body_style
    ))

    story.append(Paragraph("&bull; <b>DFD 2.1 Generation & Sanitization Sub-Process:</b>", bullet_style))
    story.append(Paragraph(
        "1.1 Receive d_k &rarr; 1.2 Query VGLC 2nd-Order Markov Matrix P(C_i | C_{i-1}, C_{i-2}, d_k) &rarr; 1.3 Generate raw 220-column grid &rarr; "
        "1.4 Inject 8-step upward intro staircase & 8-step flagpole outro staircase with castle walk &rarr; "
        "1.5 Scan columns for special blocks (?, Q, 1, 2) stacked on obstacles & execute <code>_fix_stacked_special_blocks()</code> to shift up/clear &rarr; "
        "1.6 Populate Goomba, Koopa, Spiky, Bullet Cannon, and Piranha Pipe decorations.",
        body_style
    ))

    story.append(Paragraph("&bull; <b>DFD 2.2 Solvability Validation Sub-Process:</b>", bullet_style))
    story.append(Paragraph(
        "2.1 Convert level text grid to Java <code>MarioLevel</code> &rarr; 2.2 Launch background A* search agent (200s limit) &rarr; "
        "2.3 Evaluate completion (&ge; 85% or WIN status) & calculate estimated difficulty d_est &rarr; "
        "2.4 Check constraint |d_est - d_k| &le; 0.05 &rarr; If Pass: return validated level; If Fail: increment attempt counter (max 50) & re-seed generator.",
        body_style
    ))

    story.append(Paragraph("&bull; <b>DFD 2.3 Real-Time DDA & Telemetry Sub-Process:</b>", bullet_style))
    story.append(Paragraph(
        "3.1 Player completes attempt in Java window &rarr; 3.2 <code>PlayLevel.java</code> writes <code>SESSION_UPDATE:WON=b:MODE=m:LIVES=l:COINS=c:COMPLETION=pct:KILLS=k:HURTS=h:JUMPS=j</code> to <code>levels/last_result.txt</code> &rarr; "
        "3.3 <code>app.py</code> parses key-value pairs & extracts death coordinates (X, Y) &rarr; 3.4 Append death marker to <code>ACTIVE_DEATH_ZONES[current_lvl]</code> &rarr; "
        "3.5 <code>dda.py</code> calculates P_cum & shifts target d_k (on death) or d_{k+1} (on win) &rarr; 3.6 Web UI re-renders telemetry cards & Canvas heatmap overlay.",
        body_style
    ))
    story.append(Spacer(1, 10))

    # ================= SECTION 3: SYSTEM MODULES SPECIFICATION =================
    story.append(Paragraph("3. Detailed System Modules Specification", h1_style))
    story.append(Paragraph(
        "This section provides an exhaustive line-item specification of all software modules composing the system.",
        body_style
    ))

    # Module 1: app.py
    story.append(Paragraph("3.1 Module 1: Web Engine & REST API Controller (<code>app.py</code>)", h2_style))
    story.append(Paragraph(
        "<code>app.py</code> serves as the central API gateway and web application server built using Python Flask. "
        "It manages web routes, asynchronous Java subprocess invocations, IPC telemetry file parsing, and death zone registry state.",
        body_style
    ))
    story.append(Paragraph("<b>Primary API Endpoints:</b>", body_style))
    
    app_endpoints = [
        [Paragraph("<b>Endpoint Route</b>", body_style), Paragraph("<b>HTTP Method</b>", body_style), Paragraph("<b>Function & Data Payload</b>", body_style)],
        [Paragraph("<code>/</code>", code_style), Paragraph("GET", body_style), Paragraph("Renders main HTML5 Web UI visualizer dashboard (<code>templates/index.html</code>).", body_style)],
        [
            Paragraph("<code>/api/generate-sequence</code>", code_style),
            Paragraph("POST", body_style),
            Paragraph("Accepts <code>{curve: [d1..dN], player_skill: 'average', max_variance: 0.10}</code>. Executes full campaign pipeline, returning level grids, solvability metrics, and telemetry.", body_style)
        ],
        [
            Paragraph("<code>/api/generate-sequence-stream</code>", code_style),
            Paragraph("POST", body_style),
            Paragraph("Server-Sent Events (SSE) streaming real-time compilation and validation progress (<code>progress</code>, <code>level_complete</code>, <code>complete</code> events).", body_style)
        ],
        [
            Paragraph("<code>/api/play-human-level</code>", code_style),
            Paragraph("POST", body_style),
            Paragraph("Accepts <code>{level_index: k, mario_mode: m, lives: l, coins: c, level_text: t}</code>. Enforces <code>lives &gt; 0</code> and generated map guards; spawns interactive 3.5x Java Swing window executing <code>PlayLevel.java</code>.", body_style)
        ],
        [
            Paragraph("<code>/api/watch-ai-play</code>", code_style),
            Paragraph("POST", body_style),
            Paragraph("Spawns visual 3.5x Java Swing window displaying Robin Baumgarten A* agent actively solving the validated level.", body_style)
        ],
        [
            Paragraph("<code>/api/check-session-result</code>", code_style),
            Paragraph("POST", body_style),
            Paragraph("Polls <code>levels/last_result.txt</code>. Parses key-value pairs (<code>WON=true/false</code>, <code>LIVES=l</code>, <code>COMPLETION=pct</code>), records cumulative death coordinates in <code>ACTIVE_DEATH_ZONES</code>, applies DDA spatial tweaks on death (retaining level slot k) or generates pre-adjusted level k+1 on win.", body_style)
        ],
        [
            Paragraph("<code>/api/telemetry/death-zone/&lt;idx&gt;</code>", code_style),
            Paragraph("GET", body_style),
            Paragraph("Returns cumulative death points (X, Y), struggle reasons, and death counts for level index <code>idx</code> across all playthroughs.", body_style)
        ]
    ]
    t_app = Table(app_endpoints, colWidths=[130, 50, 360])
    t_app.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_light_bg),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_app)
    story.append(Spacer(1, 10))

    # Module 2: generator.py & vglc_model.py
    story.append(Paragraph("3.2 Module 2: Procedural Generator & Markov Model (<code>generator.py</code> & <code>vglc_model.py</code>)", h2_style))
    story.append(Paragraph(
        "This module constructs candidate level grids conditioned on target difficulty metrics. "
        "It uses a 2nd-order Markov chain model trained on 31 VGLC Super Mario Bros levels (<code>vglc_trainer.py</code>).",
        body_style
    ))
    story.append(Paragraph("<b>Key Procedural Generation Rules & Algorithms:</b>", body_style))
    story.append(Paragraph("&bull; <b>Conditioned Column Sampling:</b> Computes transition probability matrix P(C_i | C_{i-1}, C_{i-2}, d_k) where C_i represents a 16-tile vertical column.", bullet_style))
    story.append(Paragraph("&bull; <b>Authentic Level Intros:</b> Columns 0&ndash;12 feature flat ground ('X') ensuring safe player spawning.", bullet_style))
    story.append(Paragraph("&bull; <b>Authentic Level Outros:</b> Columns (W-30) to (W-15) feature an 8-step upward staircase leading to a flagpole placed 4&ndash;6 tiles away, followed by an automated walk to a castle door.", bullet_style))
    story.append(Paragraph("&bull; <b>Unhittable Stack Block Sanitizer (<code>_fix_stacked_special_blocks</code>):</b> Scans columns for reward blocks ('?', 'Q', '1', '2') stacked directly on top of solid blocks ('S', '#', '%') and shifts them up to guarantee jumping clearance height.", bullet_style))
    story.append(Paragraph("&bull; <b>Targeted DDA Spatial Micro-Adjuster (<code>tweak_level_for_dda</code>):</b> On player death retries, modifies the exact level layout by injecting safety stepping platforms across pits, demoting aggressive enemies near the failure column X_fail, and inserting power-up ? blocks 5 columns prior to failure point.", bullet_style))
    story.append(Paragraph("&bull; <b>Enemy & Pipe Decoration Post-Processing:</b> Dynamically places Goombas ('g'), Koopas ('k'/'r'), Flying Koopas ('K'/'R'), Spikies ('y'/'Y'), Bullet Bill Cannons ('B'/'b'), and Piranha Flower Pipes ('T').", bullet_style))
    story.append(Spacer(1, 10))

    # Module 3: validator.py
    story.append(Paragraph("3.3 Module 3: A* Playability Validator (<code>validator.py</code>)", h2_style))
    story.append(Paragraph(
        "<code>validator.py</code> acts as an automated quality assurance engine. "
        "It invokes the Robin Baumgarten A* search agent (from the Mario AI Framework) in headless background mode to test if Mario can successfully navigate from start to finish within 200 seconds.",
        body_style
    ))
    story.append(Paragraph("&bull; <b>Solvability Verification:</b> Measures completion percentage (&ge; 85% required) and game status (WIN).", bullet_style))
    story.append(Paragraph("&bull; <b>Difficulty Calibration:</b> Calculates structural jump difficulty d_est based on required jump heights, gap widths, and enemy densities.", bullet_style))
    story.append(Paragraph("&bull; <b>Automated Retries:</b> If |d_est - d_k| &gt; 0.05 or the level is unsolvable, the generator automatically re-seeds and retries up to 50 times.", bullet_style))
    story.append(Spacer(1, 10))

    # Module 4: dda.py
    story.append(Paragraph("3.4 Module 4: Bayesian Cumulative DDA Engine (<code>dda.py</code>)", h2_style))
    story.append(Paragraph(
        "The DDA engine dynamically adapts level difficulty based on cumulative human performance telemetry across all preceding levels played in the active session.",
        body_style
    ))
    story.append(Paragraph("<b>Mathematical Formulations:</b>", body_style))
    story.append(Paragraph("<b>1. Individual Level Performance Index (P_i):</b>", body_style))
    story.append(Paragraph("P_i = 0.40 * Won_i + 0.30 * CompletionPct_i + 0.15 * (1 - min(1, Hurts_i / 5)) + 0.15 * (Mode_i / 2)", callout_style))
    story.append(Paragraph("<b>2. Exponential Decay Session Weighting (w_i):</b>", body_style))
    story.append(Paragraph("w_i = 0.70^(n - 1 - i)   for level i in {0 ... n-1}", callout_style))
    story.append(Paragraph("<b>3. Cumulative Performance Index (P_cum):</b>", body_style))
    story.append(Paragraph("P_cum = ( Sum_{i=0}^{n-1} w_i * P_i ) / ( Sum_{i=0}^{n-1} w_i )", callout_style))
    story.append(Paragraph("<b>4. Bounded Difficulty Target Shift (&Delta;d):</b>", body_style))
    story.append(Paragraph("&Delta;d = Clamp( &alpha; * (P_cum - P_target), -0.10, +0.10 )   where &alpha; = 0.25", callout_style))
    story.append(Paragraph("&bull; <b>Scoped Level Tuning & Slot Retention:</b> When a player dies on Level k, the session strictly locks to Level slot k with a micro-adjusted layout. When Level k is cleared, DDA shifts target Level k+1 before play begins.", bullet_style))
    story.append(Spacer(1, 10))

    # Module 5: game_session.py
    story.append(Paragraph("3.5 Module 5: Campaign & Session State Manager (<code>game_session.py</code>)", h2_style))
    story.append(Paragraph(
        "<code>game_session.py</code> manages player arcade progression state, life system (3 lives bounded at 0), coin accumulation (100 coins = +1 life), and campaign level preservation.",
        body_style
    ))
    story.append(Paragraph("&bull; <b>Campaign Sequence Generation:</b> Generates initial level sequences matching designer curve targets with 0.0% initial DDA shift without simulated skill guessing.", bullet_style))
    story.append(Paragraph("&bull; <b>Arcade Level Preservation:</b> When a player loses 3 lives and resets the campaign, previously generated level layouts are preserved so players replay the exact same levels unlocked earlier.", bullet_style))
    story.append(Paragraph("&bull; <b>Life System Lower Bounding & Game Over:</b> Bounded at 0 lives; on 3rd death, execution halts with Game Over status until manual reset.", bullet_style))
    story.append(Spacer(1, 10))

    # Module 6: index.html
    story.append(Paragraph("3.6 Module 6: Web Interface & Visualizer (<code>templates/index.html</code>)", h2_style))
    story.append(Paragraph(
        "The frontend is built using Vanilla CSS glassmorphism aesthetics, Chart.js graphs, HTML Canvas overlays, and modal progress animations.",
        body_style
    ))
    story.append(Paragraph("&bull; <b>Chart.js Wave Curve Designer:</b> Shows ONLY designer-intended curve on initial load; gates actual difficulty and DDA-adjusted curves behind generation completion.", bullet_style))
    story.append(Paragraph("&bull; <b>Level Map Visualizer Inactive Lifecycle:</b> Displays clean placeholder guidance and disabled buttons prior to generation; activates upon validated campaign return.", bullet_style))
    story.append(Paragraph("&bull; <b>Bounded Horizontal Scrolling (<code>.level-view-container</code>):</b> Locks viewing box to grid height (260px) with custom glowing horizontal scrollbars across all 220 columns.", bullet_style))
    story.append(Paragraph("&bull; <b>Synchronized Canvas Coordinate Space (<code>.level-canvas-wrapper</code>):</b> Locks `#heatmapCanvas` and `#tileGrid` in exact 1:1 pixel coordinate alignment, accurately rendering death skull markers (`💀`) and AI playback across the full level width.", bullet_style))
    story.append(Paragraph("&bull; <b>Arcade Progression Workspace & HUD:</b> Level selection buttons (`World 1-1 ✔`, `World 1-2 🎮`), live life counter (`❤️ 3`), and Game Over play locking.", bullet_style))
    story.append(Spacer(1, 10))

    # Module 7: Java Engine Framework
    story.append(Paragraph("3.7 Module 7: Java Swing Engine Framework (<code>Mario-AI-Framework</code>)", h2_style))
    story.append(Paragraph(
        "The native execution engine is implemented in Java 17 and Swing AWT.",
        body_style
    ))
    story.append(Paragraph("&bull; <b><code>PlayLevel.java</code>:</b> Main entry point handling command-line arguments (level path, mode, state, lives, coins), clamping <code>newLives = Math.max(0, newLives)</code> on death.", bullet_style))
    story.append(Paragraph("&bull; <b>In-Game Swing HUD:</b> Passes player lives and coin counts into <code>MarioWorld</code>, rendering remaining lives on the top-left HUD.", bullet_style))
    story.append(Paragraph("&bull; <b>IPC Telemetry Logger:</b> Writes `SESSION_UPDATE:WON=b:MODE=m:LIVES=l:COINS=c:COMPLETION=pct:KILLS=k:HURTS=h:JUMPS=j` to `levels/last_result.txt` upon game over or course clear.", bullet_style))
    story.append(Spacer(1, 14))

    # ================= SECTION 4: VERIFICATION & AUDIT =================
    story.append(Paragraph("4. System Verification & Audit System", h1_style))
    story.append(Paragraph(
        "All structural modifications, API updates, and algorithm enhancements are systematically validated and recorded in date-stamped logs inside the <code>Remarks/</code> directory (e.g. <code>Remarks/2026-08-06.txt</code>).",
        body_style
    ))

    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=10, spaceAfter=8))
    story.append(Paragraph("Mario PCG & Dynamic Difficulty Adjustment Framework | Complete Architecture Specification Document", ParagraphStyle('FooterStyle', parent=styles['Normal'], fontSize=8, textColor=colors.gray, alignment=TA_CENTER)))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] Built {filename} cleanly!")

if __name__ == "__main__":
    create_architecture_pdf()
