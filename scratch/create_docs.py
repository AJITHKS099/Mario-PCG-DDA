import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# Create Remarks directory
remarks_dir = os.path.abspath("Remarks")
os.makedirs(remarks_dir, exist_ok=True)

# Define Overview Content Text
overview_text = """================================================================================
          MARIO PCG & DYNAMIC DIFFICULTY ADJUSTMENT (DDA) ENGINE
                           PROJECT OVERVIEW
================================================================================

1. PROJECT SUMMARY
------------------
The Mario PCG & DDA Engine is an advanced AI-driven level generation and 
adaptive difficulty framework designed for Super Mario Bros. The project 
combines machine learning (2nd-order Markov Chain model), real-time difficulty 
estimation, dynamic difficulty adjustment (DDA), a web dashboard, and a native 
Java game engine.

2. CORE FEATURES & ARCHITECTURE
--------------------------------
A. VGLC-Trained PCG Level Generator (vglc_trainer.py, generator.py)
   - Trained on all 31 authentic NES Super Mario Bros level files from the 
     Video Game Level Corpus (VGLC).
   - 2nd-order Markov Chain model (N=2 context window) with 1,165 unique 
     16-row column slice transitions.
   - Difficulty-conditioned sampling P(C_i | C_i-1, C_i-2, D) across 
     difficulties 0.05 to 0.95.
   - Enforces strict tolerance: estimated difficulty is guaranteed within 
     <= 0.05 (5%) of target difficulty via candidate retry validation.
   - Classic Mario End Sequence: 8-step ascending staircase, 3-tile jump gap, 
     flagpole (F), 5-tile walkway, and a 5x5 Brick Castle with open door cutout.

B. Difficulty Estimator Engine (estimator.py)
   - Quantitative heuristic analyzer scoring levels on a scale of 0.00 to 1.00.
   - Evaluates enemy density (Goombas, Koopas, Spikes, Piranhas), pit gaps, 
     gap width, terrain variance, and power-up relief.

C. Dynamic Difficulty Adjustment (dda.py)
   - Real-time difficulty adaptation based on player telemetry (completion %, 
     lives lost, time taken, power state).
   - Bounded shifts (+/- 10% max variance per level) to prevent abrupt spikes.
   - Micro-adjusts level layouts on retries when player dies while preserving 
     overall layout structure.

D. Web Control Dashboard (templates/index.html, app.py)
   - Designer Workspace: Configure 3 to 10 level campaign curves, load presets 
     (Linear Ramp, Mid-Spike, Sawtooth Wave, Boss Rush), view live Chart.js 
     curves, inspect tile maps, and launch live AI playback.
   - Player Arcade Mode: Campaign progression with lives tracking, coins, power 
     states, level unlocking, and DDA shift indicators.
   - Expandable Telemetry Drawer ("Read More"): Shows completion time, 
     enemies killed, struggle location, and layout modifications.
   - 100% Level Layout Sync: Ensures AI solver playback in Designer mode and 
     human interactive play in Player mode run the EXACT SAME level layout.

E. Native Java Game Engine (Mario-AI-Framework)
   - Launches native Java GUI windows using direct process execution.
   - Extended Keyboard Controls (Agent.java): Arrow Keys, WASD, Spacebar, 
     Shift, Control, Z/X, J/K.
   - Automatic Castle Entrance Cutscene (Mario.java): When Mario touches the 
     flagpole, input is overridden to automatically walk Mario right into 
     the Castle door to complete the course clear sequence.

3. WORKSPACE DIRECTORY STRUCTURE
---------------------------------
c:/Users/str88/OneDrive/Desktop/mario_pcg_project/
├── app.py                      # Flask Server & API routes
├── generator.py                # Level Generator & Retry Loop
├── vglc_trainer.py             # VGLC 2nd-order Markov Chain Trainer
├── dda.py                      # Dynamic Difficulty Adjustment Logic
├── estimator.py                # Heuristic Level Difficulty Estimator
├── pipeline.py                 # End-to-End Sequence Pipeline Generator
├── templates/
│   └── index.html              # Modern Web Dashboard (Designer & Player)
├── Remarks/                    # Date-stamped Project Remarks & Changelogs
│   └── 2026-08-05.txt          # Latest System Features & Updates
├── TheVGLC/                    # Video Game Level Corpus Dataset (31 Levels)
└── Mario-AI-Framework/         # Native Java Engine & Robin Baumgarten AI
"""

# Write PROJECT_OVERVIEW.txt
txt_path = os.path.abspath("PROJECT_OVERVIEW.txt")
with open(txt_path, "w", encoding="utf-8") as f:
    f.write(overview_text)
print(f"Created {txt_path}")

# Write Remarks/2026-08-05.txt
remarks_file = os.path.join(remarks_dir, "2026-08-05.txt")
remarks_text = """================================================================================
                      MARIO PCG & DDA PROJECT REMARKS LOG
                                DATE: 2026-08-05
================================================================================

TODAY'S SUMMARY OF COMPLETED FEATURES & CHANGES:

1. VGLC 2nd-Order Markov Level Generator Integration
   - Processed all 31 authentic NES Super Mario Bros level files from VGLC.
   - Trained 1,165 2nd-order column transitions mapped to Mario-AI-Framework tiles.
   - Conditioned column sampling on target difficulty with candidate validation 
     guaranteeing difficulty error <= 0.05 (5%).

2. Classic Super Mario Bros Level Ending Sequence
   - Built ascending 8-step staircase pyramid, 3-tile jump gap before flagpole, 
     flagpole (F), 5-tile walkway, and 5x5 Brick Castle with open door cutout.

3. Automated Castle Door Entrance Cutscene
   - Updated Mario.java so that touching the flagpole activates an exit cutscene 
     where Mario automatically walks right into the Castle door, triggering world.win().

4. Perfect 1-to-1 Level Layout Synchronization
   - Synced campaign level layout data between Designer Mode and Player Arcade Mode.
   - Watching AI play in Designer Mode and playing in Player Arcade Mode now 
     loads the EXACT SAME level layout.

5. System Remarks & Documentation Infrastructure
   - Created Remarks/ folder for date-stamped changelog files (YYYY-MM-DD.txt).
   - Generated PROJECT_OVERVIEW.txt, PROJECT_OVERVIEW.pdf, and PROJECT_OVERVIEW.md.
"""

with open(remarks_file, "w", encoding="utf-8") as f:
    f.write(remarks_text)
print(f"Created {remarks_file}")

# Write PROJECT_OVERVIEW.md
md_path = os.path.abspath("PROJECT_OVERVIEW.md")
md_text = """# 🍄 Mario PCG & Dynamic Difficulty Adjustment (DDA) Engine

## 📌 Project Overview
The **Mario PCG & DDA Engine** is an advanced AI-driven level generation and adaptive difficulty framework for *Super Mario Bros*. It combines a 2nd-order Markov Chain Procedural Level Generator, heuristic difficulty estimation, real-time Dynamic Difficulty Adjustment (DDA), a web control dashboard, and a native Java game engine.

---

## 🛠️ Core Features & Architecture

### 1. VGLC-Trained PCG Level Generator (`vglc_trainer.py`, `generator.py`)
- Trained on all 31 authentic NES *Super Mario Bros* level files from the Video Game Level Corpus (VGLC).
- **2nd-Order Markov Chain Model:** $N=2$ context window with **1,165 unique 16-row column slice transitions**.
- **Difficulty-Conditioned Sampling:** $P(C_i \mid C_{i-1}, C_{i-2}, D)$ across target difficulties $0.05 \rightarrow 0.95$.
- **Strict Tolerance Guarantee:** Candidate retry loop guarantees estimated difficulty is within $\le 0.05$ (5%) of target difficulty.
- **Classic Mario End Sequence:** 8-step ascending staircase, 3-tile jump gap, flagpole (`F`), 5-tile walkway, and a 5x5 Brick Castle with open entrance door.

### 2. Difficulty Estimator Engine (`estimator.py`)
- Quantitative heuristic analyzer scoring levels on a continuous scale $[0.00, 1.00]$.
- Evaluates enemy density (Goombas, Koopas, Spikies, Piranha Flowers), pit gaps, gap width, terrain variance, and power-up relief.

### 3. Dynamic Difficulty Adjustment (`dda.py`)
- Real-time difficulty adaptation based on player performance telemetry (completion %, lives lost, time taken, power state).
- Bounded shifts ($\pm 10\%$ max variance per level) to prevent abrupt spikes.
- Micro-adjusts level layouts on retries when a player dies, preserving overall structure while easing challenge.

### 4. Web Control Dashboard (`templates/index.html`, `app.py`)
- **Designer Workspace:** Configure 3 to 10 level campaign curves, load preset pacing arcs (Linear Ramp, Mid-Spike, Sawtooth Wave, Boss Rush), view live Chart.js curves, inspect tile maps, and trigger real-time AI solver playback (`👁️ Watch AI Play Level Live`).
- **Player Arcade Mode:** Campaign progression with lives tracking, coins, power states, level unlocking, and DDA shift indicators.
- **Expandable Telemetry Drawer ("Read More"):** Shows completion time, enemies killed, struggle location, and layout modifications.
- **100% Level Layout Sync:** Ensures AI solver playback in Designer mode and human interactive play in Player mode run the **EXACT SAME** level layout.

### 5. Native Java Game Engine (`Mario-AI-Framework`)
- Launches native Java GUI windows using direct process execution.
- **Extended Keyboard Controls (`Agent.java`):** Arrow Keys, WASD, Spacebar, Shift, Control, Z/X, J/K.
- **Automatic Castle Entrance Cutscene (`Mario.java`):** When Mario touches the flagpole, input is overridden to automatically walk Mario right into the Castle door to complete the course clear sequence.

---

## 📁 Project Directory Structure
```
mario_pcg_project/
├── app.py                      # Flask Server & API routes
├── generator.py                # Level Generator & Retry Loop
├── vglc_trainer.py             # VGLC 2nd-order Markov Chain Trainer
├── dda.py                      # Dynamic Difficulty Adjustment Logic
├── estimator.py                # Heuristic Level Difficulty Estimator
├── pipeline.py                 # End-to-End Sequence Pipeline Generator
├── Remarks/                    # Date-stamped Project Remarks & Changelogs
│   └── 2026-08-05.txt          # Latest System Features & Updates
├── templates/
│   └── index.html              # Modern Web Dashboard (Designer & Player)
├── TheVGLC/                    # Video Game Level Corpus Dataset (31 Levels)
└── Mario-AI-Framework/         # Native Java Engine & Robin Baumgarten AI
```
"""

with open(md_path, "w", encoding="utf-8") as f:
    f.write(md_text)
print(f"Created {md_path}")

# Generate PDF File using ReportLab
pdf_path = os.path.abspath("PROJECT_OVERVIEW.pdf")
doc = SimpleDocTemplate(pdf_path, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Heading1'],
    fontName='Helvetica-Bold',
    fontSize=20,
    leading=24,
    textColor=colors.HexColor("#0f172a"),
    alignment=1, # Center
    spaceAfter=15
)

h2_style = ParagraphStyle(
    'SectionHeader',
    parent=styles['Heading2'],
    fontName='Helvetica-Bold',
    fontSize=13,
    leading=16,
    textColor=colors.HexColor("#2563eb"),
    spaceBefore=12,
    spaceAfter=6
)

body_style = ParagraphStyle(
    'BodyTextCustom',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=9.5,
    leading=13,
    textColor=colors.HexColor("#334155"),
    spaceAfter=6
)

bullet_style = ParagraphStyle(
    'BulletCustom',
    parent=body_style,
    leftIndent=15,
    bulletIndent=5,
    spaceAfter=4
)

story = []
story.append(Paragraph("Mario PCG & Dynamic Difficulty Adjustment (DDA) Engine", title_style))
story.append(Paragraph("<b>Comprehensive Technical Overview & Architecture Document</b>", ParagraphStyle('Sub', alignment=1, fontSize=11, leading=14, textColor=colors.HexColor("#64748b"), spaceAfter=15)))
story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#cbd5e1"), spaceAfter=15))

story.append(Paragraph("1. Executive Summary", h2_style))
story.append(Paragraph("The <b>Mario PCG & DDA Engine</b> is an advanced AI-driven level generation and adaptive difficulty framework for <i>Super Mario Bros</i>. The system combines machine learning (2nd-order Markov Chain model), real-time heuristic difficulty estimation, dynamic difficulty adjustment (DDA), a web-based control dashboard, and a native Java game engine.", body_style))

story.append(Paragraph("2. Core Features & Architectural Components", h2_style))

story.append(Paragraph("<b>A. VGLC-Trained PCG Level Generator (vglc_trainer.py, generator.py)</b>", body_style))
story.append(Paragraph("• Trained on all 31 authentic NES Super Mario Bros level files from the Video Game Level Corpus (VGLC).", bullet_style))
story.append(Paragraph("• <b>2nd-Order Markov Chain Model:</b> Uses N=2 context window trained over 1,165 unique 16-row column transitions.", bullet_style))
story.append(Paragraph("• <b>Difficulty-Conditioned Sampling:</b> Samples transitions P(C_i | C_i-1, C_i-2, D) across target difficulties 0.05 to 0.95.", bullet_style))
story.append(Paragraph("• <b>Strict Tolerance Guarantee:</b> Automated candidate retry loop guarantees estimated difficulty is within &le; 0.05 (5%) of target difficulty.", bullet_style))
story.append(Paragraph("• <b>Classic End Sequence:</b> 8-step ascending staircase, 3-tile jump gap, flagpole (F), 5-tile walkway, and 5x5 Brick Castle with open entrance door.", bullet_style))

story.append(Spacer(1, 6))
story.append(Paragraph("<b>B. Difficulty Estimator Engine (estimator.py)</b>", body_style))
story.append(Paragraph("• Quantitative heuristic analyzer scoring levels on a continuous scale of 0.00 to 1.00.", bullet_style))
story.append(Paragraph("• Evaluates enemy density (Goombas, Koopas, Spikies, Piranha Flowers), pit gaps, gap width, terrain height variance, and power-up relief.", bullet_style))

story.append(Spacer(1, 6))
story.append(Paragraph("<b>C. Dynamic Difficulty Adjustment Engine (dda.py)</b>", body_style))
story.append(Paragraph("• Real-time difficulty adaptation based on player telemetry (completion %, lives lost, completion time vs target time, power state).", bullet_style))
story.append(Paragraph("• Bounded shifts (&plusmn;10% max variance per level) to prevent abrupt difficulty spikes.", bullet_style))
story.append(Paragraph("• Micro-adjusts level layouts on retries when player dies while preserving overall level layout structure.", bullet_style))

story.append(Spacer(1, 6))
story.append(Paragraph("<b>D. Web Control Dashboard (templates/index.html, app.py)</b>", body_style))
story.append(Paragraph("• <b>Designer Workspace:</b> Configure 3 to 10 level campaign curves, load preset pacing arcs (Linear Ramp, Mid-Spike, Sawtooth Wave, Boss Rush), view live Chart.js curves, inspect tile maps, and launch live AI solver playback.", bullet_style))
story.append(Paragraph("• <b>Player Arcade Mode:</b> Interactive campaign progression with lives tracking, coins, power state, level unlocking, and DDA shift indicators.", bullet_style))
story.append(Paragraph("• <b>Expandable Telemetry Drawer ('Read More'):</b> Shows completion time, enemies killed, struggle location, and layout modifications.", bullet_style))
story.append(Paragraph("• <b>100% Level Layout Sync:</b> Ensures AI solver playback in Designer mode and human interactive play in Player mode run the EXACT SAME level layout.", bullet_style))

story.append(Spacer(1, 6))
story.append(Paragraph("<b>E. Native Java Game Engine (Mario-AI-Framework)</b>", body_style))
story.append(Paragraph("• Launches native Java GUI windows using direct process execution with process creation flags.", bullet_style))
story.append(Paragraph("• <b>Extended Keyboard Controls:</b> Arrow Keys, WASD, Spacebar, Shift, Control, Z/X, J/K.", bullet_style))
story.append(Paragraph("• <b>Automated Castle Entrance Cutscene:</b> When Mario touches the flagpole, input is overridden to automatically walk Mario right into the Castle door to complete the course clear sequence.", bullet_style))

story.append(Paragraph("3. Workspace Directory & Documentation Structure", h2_style))
story.append(Paragraph("All ongoing date-stamped changelogs are maintained inside the <b>Remarks/</b> directory (e.g., <i>Remarks/2026-08-05.txt</i>), detailing every new update and feature introduced.", body_style))

doc.build(story)
print(f"Created {pdf_path}")
