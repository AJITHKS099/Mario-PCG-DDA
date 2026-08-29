# Super Mario Bros PCG & DDA Framework
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
- **Proportional Real-Time Loading Progress Bar:** Modal displaying step-by-step progress ($0\% \to 100\%$) in exact 1:1 proportion to actual levels compiled and validated.
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
- **Multi-Point Curve Conditioning:** Accepts target vector $D = [d_1, d_2, \dots, d_N]$.
- **Proportional Loading Bar Modal:** Displays an animated progress bar updating step-by-step ($0\% \to 100\%$) as each level is compiled and validated.
- **Targeted Spatial DDA Micro-Adjuster:** `tweak_level_for_dda()` injects safety stepping platforms across pits, demotes aggressive enemies, and inserts power-up blocks near failure points on retry.
- **Unhittable Stack Block Sanitizer:** `_fix_stacked_special_blocks()` ensures all special blocks (`?`, `Q`, `1`, `2`) have jumping clearance to be hit from below.

#### Module 2: A* Pathfinding Playability Validator (`validator.py` & Java Framework)
- **Solvability Guarantee:** Robin Baumgarten A* agent tests jump trajectories and completion within 200s.
- **Automated Retries:** Re-generates up to 50 attempts if candidate level is unsolvable.
- **Live AI Playback Window:** Displays A* agent solving levels in a 3.5x scaled Java window.

#### Module 3: Bayesian Cumulative DDA Engine (`dda.py` & `game_session.py`)
- **Selective Next-Level Tuning & Slot Retention:** Applies DDA shifts strictly to Level $k$ on death (retaining slot $k$) and Level $k+1$ on win.
- **Cumulative Session Telemetry:** Computes weighted session performance index $P_{\text{cum}}$.
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
