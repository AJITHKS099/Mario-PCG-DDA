================================================================================
                    SUPER MARIO BROS PCG & DDA FRAMEWORK
================================================================================
This root directory contains the core runtime and engine files for the project.

CORE RUNTIME FILES:
- app.py: Main Flask server providing REST APIs, SSE streaming, and route handlers.
- generator.py: 2nd-order Markov chain PCG level generator with DDA layout adaptations.
- vglc_trainer.py: Parses authentic SMB levels in TheVGLC/ to train transition matrices.
- dda.py: Bayesian cumulative dynamic difficulty adjustment engine.
- estimator.py: Evaluates structural metrics (gap, height, enemy frequency) to estimate difficulty.
- game_session.py: Manages active campaign state, life counters, and solvability validation.
- validator.py: Interfaces with the Robin Baumgarten A* pathfinding solver in Java.
- pipeline.py: Orchestrates multi-level trajectory generation and campaign history aggregation.

CORE DIRECTORIES:
- templates/: Modern Glassmorphism (index.html) and Retro Arcade (retro.html) frontends.
- Mario-AI-Framework/: Java 17 framework hosting game engine, A* solver, and Swing UI.
- TheVGLC/: Video Game Level Corpus dataset containing authentic Super Mario Bros maps.
- levels/: Runtime directory where compiled and validated campaign levels are stored.

SUBDIRECTORIES:
- themes/: Alternate frontend skins including Cyberpunk Megacity (cyberpunk.html).
- documentation/: System architecture, DFD diagrams, project specifications, and build scripts.
- tests/: Comprehensive automated test suite for validation, routes, and UI state.
- legacy/: Deprecated prototype generator, early models, and old project backups.
- bin/: Scratch, temporary, and waste files preserved for historical reference.

HOW TO RUN:
Execute: py app.py
Open:    http://127.0.0.1:5000/          (Modern Glassmorphism UI)
         http://127.0.0.1:5000/retro     (Retro 8-Bit Arcade UI)
