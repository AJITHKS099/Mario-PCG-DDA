import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

def build_pdf_overview(filename="PROJECT_OVERVIEW.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Custom Palette
    c_primary = colors.HexColor("#1e293b")    # Slate 800
    c_secondary = colors.HexColor("#334155")  # Slate 700
    c_accent = colors.HexColor("#4f46e5")     # Indigo 600
    c_text = colors.HexColor("#0f172a")       # Slate 900
    c_light_bg = colors.HexColor("#f8fafc")   # Slate 50
    c_border = colors.HexColor("#cbd5e1")     # Slate 300

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=c_primary,
        alignment=TA_CENTER,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=10.5,
        leading=13,
        textColor=c_accent,
        alignment=TA_CENTER,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'H1Style',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=c_primary,
        spaceBefore=12,
        spaceAfter=5
    )

    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=9,
        leading=12.5,
        textColor=c_text,
        alignment=TA_LEFT,
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'BulletStyle',
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Code'],
        fontName='Courier',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#0f172a"),
        backColor=c_light_bg,
        borderColor=c_border,
        borderWidth=0.5,
        borderPadding=3,
        spaceBefore=3,
        spaceAfter=4
    )

    story = []

    # Title Banner
    story.append(Paragraph("SUPER MARIO BROS PCG & DDA FRAMEWORK", title_style))
    story.append(Paragraph("Comprehensive Technical Specification, System Architecture & System Overview", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceBefore=0, spaceAfter=10))

    # Section 1: Executive Summary
    story.append(Paragraph("1. Executive Summary & Core Objectives", h1_style))
    story.append(Paragraph(
        "This project implements a full <b>Difficulty-Trajectory-Conditioned Procedural Content Generation (PCG) Framework</b> "
        "paired with a <b>Bayesian Cumulative Dynamic Difficulty Adjustment (DDA) Engine</b> for Super Mario Bros. "
        "The system transitions Mario PCG from single-level generators into a holistic multi-level campaign engine capable of "
        "generating contiguous, playable levels tuned precisely to arbitrary designer pacing arcs (e.g. Linear Ramp, Spike & Recovery, Sawtooth Wave, Boss Rush).",
        body_style
    ))
    story.append(Paragraph("<b>Key Features & Innovations:</b>", body_style))
    story.append(Paragraph("• <b>Trajectory-Conditioned 2nd-Order Markov Chain:</b> Trained on 31 authentic Super Mario Bros VGLC level maps.", bullet_style))
    story.append(Paragraph("• <b>A* Pathfinding Playability Guarantees:</b> Integrates Robin Baumgarten A* search solver to validate solvability and enforce a tight difficulty variance constraint (&le; 5%).", bullet_style))
    story.append(Paragraph("• <b>Selective Cumulative Session DDA Engine:</b> Evaluates player telemetry across all preceding levels played in the session using exponential decay weighting, adjusting ONLY the next upcoming level.", bullet_style))
    story.append(Paragraph("• <b>Cumulative Death Zone Telemetry Inspector:</b> Records and renders ALL death points (X, Y) accumulated across multiple playthrough attempts per level map. Persists across 3-life resets and clears ONLY when brand-new maps are generated.", bullet_style))
    story.append(Paragraph("• <b>Unified 0–100 Metric Scale:</b> Harmonizes Chart.js wave-like graphs, designer curve input boxes (5 to 95), telemetry cards, and DDA target metrics onto a single unified 0 to 100% scale.", bullet_style))
    story.append(Paragraph("• <b>Authentic Classic SMB Level Structures:</b> Guarantees 8-step staircase intros, 8-step staircase endings with flagpole distance jumps, and automated castle walking sequences.", bullet_style))
    story.append(Paragraph("• <b>Progressive Enemy Hazards & Stack Block Sanitizer:</b> Dynamic Green/Red Koopas, Flying Koopas, Spikies, Bullet Bill Cannons, Piranha Plants, and stack block sanitizer guaranteeing 100% hittable reward blocks.", bullet_style))
    story.append(Paragraph("• <b>Proportional Real-Time Loading Progress Bar:</b> Modal displaying step-by-step progress (0% to 100%) in exact 1:1 proportion to actual levels compiled and validated.", bullet_style))

    # Architecture Overview Table
    story.append(Spacer(1, 4))
    table_data = [
        [Paragraph("<b>Module / File</b>", body_style), Paragraph("<b>Core Technical Functionality & Responsibility</b>", body_style)],
        [Paragraph("<code>pipeline.py</code>", code_style), Paragraph("Coordinates full multi-point trajectory generation, DDA simulation, and campaign history aggregation.", body_style)],
        [Paragraph("<code>generator.py</code>", code_style), Paragraph("Executes conditioned Markov sampling, post-processing decoration enhancements, stack block sanitization, and level generation.", body_style)],
        [Paragraph("<code>vglc_trainer.py</code>", code_style), Paragraph("Parses 31 VGLC level text files, extracts 2nd-order column transition matrices, and computes difficulty metrics.", body_style)],
        [Paragraph("<code>validator.py</code>", code_style), Paragraph("Invokes Java Robin Baumgarten A* agent to test solvability and measure structural jump difficulty.", body_style)],
        [Paragraph("<code>dda.py</code>", code_style), Paragraph("Calculates weighted cumulative session performance indices and enforces bounded micro-adjustments (&plusmn;10% max variance).", body_style)],
        [Paragraph("<code>game_session.py</code>", code_style), Paragraph("Manages player arcade campaign state, life system, coin accumulation, and session progression tracking.", body_style)],
        [Paragraph("<code>app.py</code>", code_style), Paragraph("Flask web engine providing REST API endpoints for real-time generation, interactive Java play launching, and telemetry polling.", body_style)],
        [Paragraph("<code>index.html</code>", code_style), Paragraph("Modern glassmorphism Web UI featuring proportional loading progress modal, difficulty curve inspector, tile viewer, and Death Zone overlays.", body_style)],
        [Paragraph("<code>PlayLevel.java</code>", code_style), Paragraph("Java Swing entry point executing human interactive play and AI playback, returning full telemetry via <code>last_result.txt</code>.", body_style)]
    ]
    t = Table(table_data, colWidths=[110, 430])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_light_bg),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t)

    # Section 2: Sequence Generator & Markov Modeling
    story.append(Paragraph("2. Module 1: Trajectory-Conditioned Sequence Generator", h1_style))
    story.append(Paragraph(
        "Level generation is powered by a 2nd-Order Markov Chain model trained on 31 Super Mario Bros VGLC text levels. "
        "The generator conditions contiguous column transitions $P(C_i \\mid C_{i-1}, C_{i-2}, D)$ to match designer difficulty vectors $D = [d_1, d_2, \\dots, d_N]$.",
        body_style
    ))
    story.append(Paragraph("• <b>Proportional Loading Bar Modal:</b> Displays an animated progress bar updating step-by-step (0% to 100%) in exact proportion to actual levels compiled and validated.", bullet_style))
    story.append(Paragraph("• <b>Authentic Level Intros & Outros:</b> Every level features an 8-step upward staircase leading to a flagpole placed 4-6 tiles away, followed by an automated walk to a castle door.", bullet_style))
    story.append(Paragraph("• <b>Unhittable Stack Block Sanitizer:</b> Includes <code>_fix_stacked_special_blocks()</code> to detect reward blocks (?, Q, 1, 2) stacked directly on top of solid obstacles and shift them up to jumping clearance heights or clear them.", bullet_style))

    # Section 3: A* Playability Validator
    story.append(Paragraph("3. Module 2: A* Pathfinding Playability Validator", h1_style))
    story.append(Paragraph(
        "Candidate level grids are evaluated using an automated Robin Baumgarten A* pathfinding search agent. "
        "The validator tests if Mario can navigate from start to finish within 200 seconds while tracking jump heights, gap clearances, and hazard avoidance.",
        body_style
    ))
    story.append(Paragraph("• <b>Strict Solvability Enforcement:</b> If a candidate level is unplayable or violates target difficulty by >5%, the generator automatically retries up to 50 times.", bullet_style))
    story.append(Paragraph("• <b>Live AI Playback Window:</b> Designers can launch a live 3.5x scaled Java window to observe the A* agent solve any generated level in real-time.", bullet_style))

    # Section 4: Cumulative Session DDA Engine
    story.append(Paragraph("4. Module 3: Selective Cumulative Session DDA Engine", h1_style))
    story.append(Paragraph(
        "The DDA engine dynamically adjusts level difficulty based on cumulative player telemetry across all preceding levels played in the active session. "
        "It uses exponential decay weighting ($w_i = 0.70^{n-1-i}$) to combine overall session trend with recent performance.",
        body_style
    ))
    story.append(Paragraph("• <b>Selective Next-Level Tuning & Slot Retention:</b> On course clear, DDA pre-adjusts the upcoming level k+1. On player death, the session strictly remains locked to Level slot k with targeted spatial DDA micro-adjustments (pit platform injection, enemy demotion, power-up insertion).", bullet_style))
    story.append(Paragraph("• <b>Strict 10% Variance Bound:</b> Bounds difficulty adjustments to $\\pm 10\\%$ of the designer's target curve.", bullet_style))
    story.append(Paragraph("• <b>Automatic Session Reset:</b> Generating a new campaign sequence automatically clears cumulative DDA session history and resets active DDA shifts to 0.0%.", bullet_style))

    # Section 5: Telemetry, Death Zones & Unified Scale
    story.append(Paragraph("5. Module 4: Visualizer, Death Zones & Life System", h1_style))
    story.append(Paragraph("• <b>Bounded Horizontal Scrolling Visualizer:</b> Locks tile view to grid height (260px) with custom glowing horizontal scrollbars spanning all 220 columns.", bullet_style))
    story.append(Paragraph("• <b>Synchronized Canvas Coordinate Space:</b> Wraps `#tileGrid` and `#heatmapCanvas` in 1:1 pixel coordinate alignment across all 220 columns for death markers (`💀`) and AI playback.", bullet_style))
    story.append(Paragraph("• <b>Cumulative Death Zone Telemetry:</b> Records and renders ALL death points (X, Y) accumulated across multiple attempts/retries for each level map. Death markers persist across 3-life campaign resets and are ONLY cleared when brand-new maps are generated.", bullet_style))
    story.append(Paragraph("• <b>Unified 0–100 Metric Scale:</b> Harmonizes Chart.js wave-like graphs, designer curve input boxes (5 to 95), telemetry cards, and DDA target metrics onto a single unified 0 to 100% scale.", bullet_style))
    story.append(Paragraph("• <b>3-Life System & Game Over Guard:</b> Clamps lives at 0 on death; on 3rd death, halts play with Game Over state and disables the Play button until 'Reset Arcade Progression' is clicked.", bullet_style))
    story.append(Paragraph("• <b>In-Game Swing HUD Sync:</b> Passes player lives and coins into Java <code>MarioWorld</code>, cleanly rendering remaining lives on the top-left in-game HUD.", bullet_style))

    # Section 6: Remarks & Audit Log Summary
    story.append(Paragraph("6. Project Remarks & Audit Logging System", h1_style))
    story.append(Paragraph(
        "All updates and architecture changes are systematically recorded in the <code>Remarks/</code> directory with date-stamped logs (e.g. <code>Remarks/2026-08-06.txt</code>). "
        "This maintains a transparent, complete historical record of project progress.",
        body_style
    ))

    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=8, spaceAfter=6))
    story.append(Paragraph("Generated automatically by Mario PCG & DDA Framework Build System | Date: 2026-08-06", ParagraphStyle('FooterStyle', parent=styles['Normal'], fontSize=8, textColor=colors.gray, alignment=TA_CENTER)))

    doc.build(story)
    print(f"[SUCCESS] Built {filename} cleanly!")

def build_text_overview(filename="PROJECT_OVERVIEW.txt"):
    content = """================================================================================
                    SUPER MARIO BROS PCG & DDA FRAMEWORK
       COMPREHENSIVE PROJECT SPECIFICATION, SYSTEM ARCHITECTURE & OVERVIEW
                                 DATE: 2026-08-06
================================================================================

1. EXECUTIVE SUMMARY & CORE OBJECTIVES
--------------------------------------------------------------------------------
This project implements a full Difficulty-Trajectory-Conditioned Procedural Content 
Generation (PCG) Framework paired with a Bayesian Cumulative Dynamic Difficulty 
Adjustment (DDA) Engine for Super Mario Bros.

The system transitions Mario PCG from single-level generators into a holistic 
multi-level campaign engine capable of generating contiguous, playable levels 
tuned precisely to arbitrary designer pacing arcs (e.g. Linear Ramp, Spike & Recovery, 
Sawtooth Wave, Boss Rush).

KEY FEATURES & INNOVATIONS:
- Trajectory-Conditioned 2nd-Order Markov Chain trained on 31 VGLC level maps.
- A* Pathfinding Playability Guarantees using Robin Baumgarten A* solver (tolerance <= 5%).
- Selective Cumulative Session DDA Engine with exponential decay weighting over session history.
- Death Retry Slot Retention & Spatial DDA (locks to Level k slot with targeted layout tweaks).
- Level Map Visualizer Horizontal Scrolling & Synchronized 1:1 Canvas Overlay.
- Cumulative Death Zone Telemetry Inspector displaying ALL death coordinates (X, Y) per level map.
- 3-Life Lower Bounding & Game Over System (stops on 3rd death; restores 3 lives on reset).
- Unified 0-100 Metric Scale harmonizing wave graphs, input boxes (5-95), and telemetry cards.
- Authentic Classic SMB Structures (8-step stair intros, 8-step stair flagpoles, castle walks).
- Progressive Enemy & Hazard Scaling (Green/Red Koopas, Flying Koopas, Spikies, Bullet Bills).
- Unhittable Stack Block Sanitizer (_fix_stacked_special_blocks() ensuring 100% hittable blocks).
- Proportional Real-Time Loading Bar Modal updating step-by-step (0% to 100%).
- Arcade Campaign Level Preservation preserving unlocked maps across 3-life resets.
- In-Game Java Swing HUD displaying accurate remaining lives (Lives: 3, 2, 1).


2. SYSTEM ARCHITECTURE & MODULE SUMMARY
--------------------------------------------------------------------------------
- pipeline.py: Coordinates trajectory generation, DDA simulation, and campaign history.
- generator.py: Conditioned Markov sampling, decoration enhancement, stack block sanitizer, tweak_level_for_dda.
- vglc_trainer.py: Parses 31 VGLC level files, extracts 2nd-order Markov transitions.
- validator.py: Invokes Java Robin Baumgarten A* agent to test solvability and jump metrics.
- dda.py: Weighted cumulative session DDA calculation with 10% max variance bounds.
- game_session.py: Manages player arcade campaign state, life system, and coin tracking.
- app.py: Flask web engine providing REST API endpoints for generation, play, and telemetry.
- index.html: Glassmorphism UI featuring loading progress modal, tile visualizer, Death Zones.
- PlayLevel.java: Java Swing engine executing human interactive play and AI playback.


3. MODULE DETAILS & FUNCTIONAL SPECIFICATIONS
--------------------------------------------------------------------------------
MODULE 1: TRAJECTORY-CONDITIONED SEQUENCE GENERATOR (pipeline.py & generator.py)
- Multi-Point Trajectory Conditioning: Accepts vector D = [d1, d2, ..., dN].
- Proportional Loading Bar Modal: Displays progress bar updating step-by-step (0% to 100%).
- Outro Staircase & Castle Walk: 8-step stair leading to flagpole, auto castle walk finish.
- Unhittable Stack Block Sanitizer: _fix_stacked_special_blocks() ensures all special 
  blocks (?, Q, 1, 2) have jumping clearance to be hit from below.
- Targeted Spatial DDA Micro-Adjuster: tweak_level_for_dda() modifies existing level layout on retry.

MODULE 2: A* PATHFINDING PLAYABILITY VALIDATOR (validator.py & Java Framework)
- Solvability Guarantee: Robin Baumgarten A* agent tests jump trajectories and completion.
- Automated Retries: Re-generates up to 50 attempts if candidate level is unsolvable.
- Live AI Playback Window: Displays A* agent solving levels in a 3.5x scaled Java window.

MODULE 3: BAYESIAN CUMULATIVE DDA ENGINE (dda.py & game_session.py)
- Selective Next-Level Tuning & Slot Retention: Applies DDA shifts to Level k on death (retaining slot k) 
  and Level k+1 on win.
- Cumulative Session Telemetry: Computes weighted session performance index P_cum.
- Exponential Decay Weighting: w_i = 0.70^(n-1-i) weights recent levels while considering session trend.
- Bounded Adjustments: Strictly bounds difficulty shifts to +/-10% max variance.

MODULE 4: DEATH ZONE TELEMETRY, VISUALIZER & LIFE SYSTEM (app.py & index.html)
- Level Map Visualizer Horizontal Scrolling: Custom styled horizontal scrollbar across 220 columns.
- Synchronized Coordinate Space: .level-canvas-wrapper locks tile text and canvas overlay in 1:1 sync.
- Cumulative Death Zone Telemetry: Records and renders ALL death points (X, Y) across all retries.
- 3-Life Lower Bounding & Game Over: Clamps lives at 0; disables Play button on Game Over.
- Unified 0-100 Metric Scale: Harmonizes Chart.js graphs, input boxes (5 to 95), and telemetry.


4. PROJECT REMARKS & AUDIT LOGGING SYSTEM
--------------------------------------------------------------------------------
All updates and architecture changes are systematically recorded in date-stamped logs 
inside the Remarks/ directory (e.g. Remarks/2026-08-06.txt) for transparent tracking.
"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[SUCCESS] Built {filename} cleanly!")

def build_md_overview(filename="PROJECT_OVERVIEW.md"):
    content = """# Super Mario Bros PCG & DDA Framework
## Comprehensive Technical Specification, System Architecture & Overview
**Date:** 2026-08-06

---

### 1. Executive Summary & Core Objectives
This project implements a full **Difficulty-Trajectory-Conditioned Procedural Content Generation (PCG) Framework** paired with a **Bayesian Cumulative Dynamic Difficulty Adjustment (DDA) Engine** for Super Mario Bros.

The system transitions Mario PCG from single-level generators into a holistic multi-level campaign engine capable of generating contiguous, playable levels tuned precisely to arbitrary designer pacing arcs (e.g. *Linear Ramp*, *Spike & Recovery*, *Sawtooth Wave*, *Boss Rush*).

#### Key Features & Innovations:
- **Trajectory-Conditioned 2nd-Order Markov Chain:** Trained on 31 authentic Super Mario Bros VGLC level maps.
- **A* Pathfinding Playability Guarantees:** Integrates Robin Baumgarten A* search solver to validate solvability and enforce a tight difficulty variance constraint (tolerance <= 5%).
- **Selective Cumulative Session DDA Engine:** Evaluates player telemetry across all preceding levels played in the session using exponential decay weighting, adjusting ONLY the upcoming level.
- **Death Retry Slot Retention & Spatial DDA:** Locks to Level $k$ slot on death and applies targeted spatial micro-adjustments (`tweak_level_for_dda`) to the existing layout.
- **Level Map Visualizer Horizontal Scrolling:** Viewport-bounded 220-column map inspection with glowing horizontal scrollbars.
- **Synchronized Canvas Coordinate Space:** Locks `#tileGrid` and `#heatmapCanvas` in 1:1 pixel coordinate alignment across all 220 columns.
- **3-Life Lower Bounding & Game Over Guard:** Clamps lives at 0 on death; halts session and disables Play button on Game Over until manual reset.
- **Cumulative Death Zone Telemetry Inspector:** Records and renders ALL death points $(X, Y)$ accumulated across multiple playthrough attempts per level map.
- **Unified 0–100 Metric Scale:** Harmonizes Chart.js wave-like graphs, designer curve input boxes (5 to 95), telemetry cards, and DDA target metrics onto a single unified 0 to 100% scale.
- **Authentic Classic SMB Level Structures:** Guarantees 8-step staircase intros, 8-step staircase endings with flagpole distance jumps, and automated castle walking sequences.
- **Progressive Enemy Hazards & Stack Block Sanitizer:** Dynamic Green/Red Koopas, Flying Koopas, Spikies, Bullet Bill Cannons, Piranha Plants, and stack block sanitizer guaranteeing 100% hittable reward blocks.
- **Proportional Real-Time Loading Progress Bar:** Modal displaying step-by-step progress ($0\% \\to 100\%$) in exact 1:1 proportion to actual levels compiled and validated.
- **Arcade Campaign Level Preservation:** Preserves generated campaign levels across 3-life resets so players replay the exact same levels unlocked earlier.
- **In-Game Java Swing HUD Sync:** Displays accurate remaining lives (`Lives: 3`, `Lives: 2`, `Lives: 1`) on the top-left HUD.

---

### 2. Core System Architecture & Module Map

| Module / File | Core Technical Functionality & Responsibility |
| :--- | :--- |
| `pipeline.py` | Coordinates full multi-point trajectory generation, DDA simulation, and campaign history aggregation. |
| `generator.py` | Executes conditioned Markov sampling, post-processing decoration enhancements, stack block sanitization, and level generation. |
| `vglc_trainer.py` | Parses 31 VGLC level text files, extracts 2nd-order column transition matrices, and computes difficulty metrics. |
| `validator.py` | Invokes Java Robin Baumgarten A* agent to test solvability and measure structural jump difficulty. |
| `dda.py` | Calculates weighted cumulative session performance indices and enforces bounded micro-adjustments ($\pm 10\%$ max variance). |
| `game_session.py` | Manages player arcade campaign state, life system, coin accumulation, and session progression tracking. |
| `app.py` | Flask web engine providing REST API endpoints for real-time generation, interactive Java play launching, and telemetry polling. |
| `index.html` | Modern glassmorphism Web UI featuring proportional loading progress modal, difficulty curve inspector, tile viewer, and Death Zone overlays. |
| `PlayLevel.java` | Java Swing entry point executing human interactive play and AI playback, returning full telemetry via `last_result.txt`. |

---

### 3. Detailed Module Specifications

#### Module 1: Trajectory-Conditioned Sequence Generator (`pipeline.py` & `generator.py`)
- **Multi-Point Curve Conditioning:** Accepts target vector $D = [d_1, d_2, \\dots, d_N]$.
- **Proportional Loading Bar Modal:** Displays an animated progress bar updating step-by-step ($0\% \\to 100\%$) as each level is compiled and validated.
- **Targeted Spatial DDA Micro-Adjuster:** `tweak_level_for_dda()` injects safety stepping platforms across pits, demotes aggressive enemies, and inserts power-up blocks near failure points on retry.
- **Unhittable Stack Block Sanitizer:** `_fix_stacked_special_blocks()` ensures all special blocks (`?`, `Q`, `1`, `2`) have jumping clearance to be hit from below.

#### Module 2: A* Pathfinding Playability Validator (`validator.py` & Java Framework)
- **Solvability Guarantee:** Robin Baumgarten A* agent tests jump trajectories and completion within 200s.
- **Automated Retries:** Re-generates up to 50 attempts if candidate level is unsolvable.
- **Live AI Playback Window:** Displays A* agent solving levels in a 3.5x scaled Java window.

#### Module 3: Bayesian Cumulative DDA Engine (`dda.py` & `game_session.py`)
- **Selective Next-Level Tuning & Slot Retention:** Applies DDA shifts strictly to Level $k$ on death (retaining slot $k$) and Level $k+1$ on win.
- **Cumulative Session Telemetry:** Computes weighted session performance index $P_{\\text{cum}}$.
- **Exponential Decay Weighting:** $w_i = 0.70^{n-1-i}$ weights recent levels while considering session trend.
- **Bounded Adjustments:** Strictly bounds difficulty shifts to $\pm 10\%$ max variance.

#### Module 4: Death Zone Telemetry, Visualizer & Life System (`app.py` & `index.html`)
- **Level Map Visualizer Horizontal Scrolling:** Fixed-height box with glowing horizontal scrollbars spanning all 220 columns.
- **Synchronized Coordinate Space:** `.level-canvas-wrapper` locks tile text and canvas overlay in 1:1 pixel sync.
- **Cumulative Death Zone Telemetry:** Records and renders ALL death points $(X, Y)$ accumulated across multiple attempts/retries for each level map.
- **3-Life Lower Bounding & Game Over:** Clamps lives at 0 on death; disables Play button on Game Over until manual reset.

---

### 4. Remarks & Audit Logging System
All updates and architecture changes are systematically recorded in date-stamped logs inside the `Remarks/` directory (e.g. `Remarks/2026-08-06.txt`) for transparent tracking.
"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[SUCCESS] Built {filename} cleanly!")

if __name__ == "__main__":
    build_pdf_overview()
    build_text_overview()
    build_md_overview()


if __name__ == "__main__":
    build_pdf_overview()
    build_text_overview()
    build_md_overview()
