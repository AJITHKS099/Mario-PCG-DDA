from flask import Flask, render_template, request, jsonify, Response, stream_with_context, send_from_directory
from pipeline import run_pipeline_sequence, generate_single_level_pipeline
from dda import DynamicDifficultyAdjuster
from generator import generate_mario_level, tweak_level_for_dda
from estimator import calculate_difficulty
from game_session import MarioCampaignSession
import os
import subprocess
import time
import json
import jinja2

app = Flask(__name__, template_folder='templates', static_folder='static')
app.jinja_loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'themes'))
])

MARIO_DIR = os.path.abspath("Mario-AI-Framework")

PRESETS = {
    "linear_ramp": {
        "name": "Linear Ramp (Progressive)",
        "curve": [0.2, 0.35, 0.5, 0.65, 0.8]
    },
    "mid_spike": {
        "name": "Spike & Recovery (Pacing Arc)",
        "curve": [0.25, 0.45, 0.85, 0.35, 0.70]
    },
    "wave_pacing": {
        "name": "Sawtooth Pacing Wave",
        "curve": [0.3, 0.6, 0.4, 0.75, 0.5, 0.85]
    },
    "boss_rush": {
        "name": "Climax Peak (Boss Rush)",
        "curve": [0.3, 0.4, 0.55, 0.7, 0.95]
    }
}

# Explanation: Renders and serves the default modern Glassmorphism dashboard user interface.
@app.route('/')
def home():
    return render_template('index.html')

# Explanation: Renders and serves the retro 8-bit arcade cabinet web user interface.
@app.route('/retro')
def retro_home():
    return render_template('retro.html')

# Explanation: Renders and serves the TOXIN//GRID cyberpunk theme web user interface.
@app.route('/cyberpunk')
def cyberpunk_home():
    return render_template('cyberpunk.html')

THEMES_STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'themes')

# Explanation: Serves static media files, background artwork, and theme assets from the themes directory.
@app.route('/themes/<path:filename>')
def themes_static(filename):
    return send_from_directory(THEMES_STATIC_DIR, filename)

# Explanation: Returns a JSON dictionary of standard designer pacing difficulty curves (Linear, Spike, Wave, Boss).
@app.route('/api/presets', methods=['GET'])
def get_presets():
    return jsonify(PRESETS)

ACTIVE_DEATH_ZONES = {}
ACTIVE_SESSION_DDA = DynamicDifficultyAdjuster(max_variance=0.10)
ACTIVE_DESIGNER_CURVE = [0.20, 0.40, 0.65, 0.80, 0.50]

# Explanation: Generates a single procedural Mario level conditioned on target difficulty and returns its ASCII layout.
@app.route('/api/generate-single-level', methods=['POST'])
def generate_single_level():
    """Generates a single campaign level tuned to target_difficulty."""
    data = request.get_json() or {}
    level_index = int(data.get("level_index", 1))
    target_diff = float(data.get("target_difficulty", 0.5))
    target_diff = target_diff / 100.0 if target_diff > 1.0 else target_diff
    
    level_text = generate_mario_level(target_diff)
    est_diff = calculate_difficulty(level_text)

    return jsonify({
        "status": "Success",
        "level_index": level_index,
        "target_difficulty": target_diff,
        "estimated_difficulty": est_diff,
        "level_text": level_text
    })

# Explanation: Streams real-time Server-Sent Events (SSE) while compiling and validating each level in a campaign sequence.
@app.route('/api/generate-sequence-stream', methods=['POST'])
def generate_sequence_stream():
    """Streams real-time level compilation & validation progress for full campaign sequence generation."""
    global ACTIVE_DESIGNER_CURVE
    data = request.get_json() or {}
    curve = data.get("curve", [0.20, 0.40, 0.65, 0.80, 0.50])
    player_skill = data.get("player_skill", "average")
    max_variance = data.get("max_variance", 0.10)

    ACTIVE_SESSION_DDA.reset_session()
    normalized_curve = [float(v) / 100.0 if float(v) > 1.0 else float(v) for v in curve]
    ACTIVE_DESIGNER_CURVE = list(normalized_curve)
    ACTIVE_DEATH_ZONES.clear()

    # Explanation: Generator yielding Server-Sent Events with progress updates and completed level payloads during campaign compilation.
    def generate_events():
        session = MarioCampaignSession(dda_max_variance=max_variance)
        history = []
        total_levels = len(normalized_curve)

        for idx, base_target in enumerate(normalized_curve):
            lvl_num = idx + 1
            start_msg = f"Compiling & Validating Level {lvl_num} of {total_levels} (Target: {int(base_target * 100)}%)..."
            yield f"data: {json.dumps({'type': 'progress', 'level': lvl_num, 'total': total_levels, 'message': start_msg})}\n\n"

            rel_path, level_text, estimated_diff = session.generate_and_validate(lvl_num, base_target)
            ACTIVE_DEATH_ZONES[lvl_num] = []

            initial_dda_result = {
                "designer_target": base_target,
                "adjusted_target": base_target,
                "delta": 0.0,
                "delta_pct": "+0.0%",
                "raw_performance": 0.0,
                "reason": "Initial campaign map generated. Awaiting human player session telemetry.",
                "dda_changes": ["Maintained designer target difficulty curve without structural shifts"]
            }

            step = {
                "level": lvl_num,
                "designer_target": base_target,
                "target_difficulty": base_target,
                "estimated_difficulty": estimated_diff,
                "player_performance": {"played": False, "won": False, "completion_pct": 0.0},
                "death_info": {"died": False},
                "dda_result": initial_dda_result,
                "level_text": level_text
            }
            history.append(step)

            done_msg = f"Level {lvl_num} of {total_levels} Validated! (Est. Diff: {int(estimated_diff * 100)}%)"
            yield f"data: {json.dumps({'type': 'level_complete', 'level': lvl_num, 'total': total_levels, 'step': step, 'message': done_msg})}\n\n"

        final_data = {
            "status": "Success",
            "data": {
                "curve": normalized_curve,
                "history": history,
                "summary": {
                    "total_levels": total_levels,
                    "player_skill": player_skill,
                    "max_variance": max_variance,
                    "designer_curve": normalized_curve,
                    "dda_adjusted_curve": [h["target_difficulty"] for h in history],
                    "actual_estimated_curve": [h["estimated_difficulty"] for h in history]
                }
            }
        }
        yield f"data: {json.dumps({'type': 'complete', 'result': final_data})}\n\n"

    return Response(stream_with_context(generate_events()), mimetype='text/event-stream')

# Explanation: Generates and validates a complete campaign sequence synchronously and returns all level layouts.
@app.route('/api/generate-sequence', methods=['POST'])
def generate_sequence():
    """Generates a sequence of levels for a full campaign based on designer curve."""
    data = request.get_json() or {}
    curve = data.get("curve", [0.20, 0.40, 0.65, 0.80, 0.50])
    player_skill = data.get("player_skill", "average")
    max_variance = data.get("max_variance", 0.10)

    global ACTIVE_DESIGNER_CURVE
    # Reset cumulative DDA session history for newly generated campaign sequence
    ACTIVE_SESSION_DDA.reset_session()

    # Normalize input values to 0.0 - 1.0 if provided on 0 - 100 scale
    normalized_curve = [float(v) / 100.0 if float(v) > 1.0 else float(v) for v in curve]
    ACTIVE_DESIGNER_CURVE = list(normalized_curve)
    
    results = run_pipeline_sequence(normalized_curve, dda_variance=max_variance, player_skill=player_skill)
    
    ACTIVE_DEATH_ZONES.clear()
    if "history" in results:
        for step in results["history"]:
            lvl_num = step.get("level", 1)
            d_info = step.get("death_info", {})
            if isinstance(d_info, dict) and d_info.get("died", False):
                ACTIVE_DEATH_ZONES[lvl_num] = [{
                    "x": d_info.get("x", 50),
                    "y": d_info.get("y", 11),
                    "intensity": 1.0,
                    "reason": d_info.get("reason", "Simulated death"),
                    "completion_pct": d_info.get("completion_pct", 0.5)
                }]
            else:
                ACTIVE_DEATH_ZONES[lvl_num] = []

    return jsonify({
        "status": "Success",
        "data": results
    })

# Explanation: Runs headless A* agent simulation on a level and returns the 2D coordinate trajectory for overlay visualization.
@app.route('/api/watch-ai-play', methods=['POST'])
def watch_ai_play():
    """Launches Java window with Robin Baumgarten AI agent solving the level in real-time."""
    data = request.get_json() or {}
    level_text = data.get("level_text", None)
    target_diff = float(data.get("target_difficulty", 0.5))
    level_idx = data.get("level_index", 1)

    levels_dir = os.path.join(MARIO_DIR, "levels")
    os.makedirs(levels_dir, exist_ok=True)
    
    timestamp = int(time.time())
    rel_path = f"levels/level_ai_vis_{level_idx}_{timestamp}.txt"
    abs_path = os.path.abspath(os.path.join(MARIO_DIR, rel_path))

    if not level_text:
        return jsonify({
            "status": "Error",
            "message": "Cannot watch AI: No validated level layout found for the current session. Please generate campaign levels first!"
        }), 400

    with open(abs_path, "w") as f:
        f.write(level_text)

    theme_id = (level_idx - 1) % 3
    run_cmd = [
        "java", "-cp", "bin", "PlayLevel",
        abs_path, "validate_vis", str(theme_id), "0"
    ]

    try:
        print(f"[API] Launching AI Playback Window for Level {level_idx} (Target Diff: {target_diff:.2f})...", flush=True)
        flags = subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
        subprocess.Popen(run_cmd, cwd=MARIO_DIR, creationflags=flags)
        return jsonify({
            "status": "Success",
            "message": f"AI playback window launched for Level {level_idx}!"
        })
    except Exception as e:
        print(f"[API ERROR] Failed to launch AI playback: {e}", flush=True)
        return jsonify({"status": "Error", "message": str(e)}), 500

# Explanation: Launches the interactive Java Mario game window in a subprocess for player evaluation.
@app.route('/api/play-human-level', methods=['POST'])
def play_human_level():
    """Launches Java interactive game window for human player."""
    data = request.get_json() or {}
    level_index = int(data.get("level_index", 1))
    target_difficulty = float(data.get("target_difficulty", 0.5))
    lives = int(data.get("lives", 3))
    coins = int(data.get("coins", 0))
    mario_mode = int(data.get("mario_mode", 0))
    is_retry = bool(data.get("is_retry", False))
    prev_level_text = data.get("prev_level_text", None)
    retry_dda_delta = float(data.get("retry_dda_delta", -0.05))

    if lives <= 0:
        return jsonify({
            "status": "Error",
            "message": "Game Over! You have 0 lives remaining. Please reset arcade campaign progression to play again."
        }), 400

    levels_dir = os.path.join(MARIO_DIR, "levels")
    os.makedirs(levels_dir, exist_ok=True)
    
    res_path = os.path.join(levels_dir, "last_result.txt")
    if os.path.exists(res_path):
        try:
            os.remove(res_path)
        except Exception:
            pass

    timestamp = int(time.time())
    rel_path = f"levels/level_human_{level_index}_{timestamp}.txt"
    abs_path = os.path.abspath(os.path.join(MARIO_DIR, rel_path))

    req_level_text = data.get("level_text", None)

    structural_changes = []
    if req_level_text and req_level_text.strip():
        level_text = req_level_text
        structural_changes = ["Loaded active campaign sequence level layout"]
    elif is_retry and prev_level_text and prev_level_text.strip():
        bounded_retry_delta = max(-0.10, min(0.10, retry_dda_delta))
        level_text, structural_changes = tweak_level_for_dda(prev_level_text, bounded_retry_delta)
    else:
        return jsonify({
            "status": "Error",
            "message": "Cannot play: No validated level layout exists for the current session. Please generate a level sequence in the Designer Workspace first!"
        }), 400

    with open(abs_path, "w") as f:
        f.write(level_text)

    theme_id = (level_index - 1) % 3
    run_cmd = [
        "java", "-cp", "bin", "PlayLevel",
        abs_path, "play", str(theme_id), str(mario_mode), str(lives), str(coins)
    ]

    try:
        print(f"[API] Launching Interactive Java Mario Window for World 1-{level_index} (Lives: {lives}, Mode: {mario_mode})...", flush=True)
        flags = subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
        subprocess.Popen(run_cmd, cwd=MARIO_DIR, creationflags=flags)
        return jsonify({
            "status": "Success",
            "message": f"Interactive Java Mario window launched for World 1-{level_index}!",
            "played_level": {
                "level_index": level_index,
                "target_difficulty": target_difficulty,
                "level_text": level_text,
                "estimated_difficulty": calculate_difficulty(level_text)
            },
            "structural_changes": structural_changes
        })
    except Exception as e:
        print(f"[API ERROR] Failed to launch interactive game window: {e}", flush=True)
        return jsonify({"status": "Error", "message": str(e)}), 500

# Explanation: Polls game session results from file, calculates Bayesian DDA adjustments on win or death, and returns adapted levels.
@app.route('/api/check-session-result', methods=['POST'])
def check_session_result():
    """Polls for completion of human interactive play in Java window."""
    data = request.get_json() or {}
    current_lvl_num = int(data.get("level_index", 1))
    next_designer_target = float(data.get("next_designer_target", 0.5))
    current_designer_target = float(data.get("current_designer_target", next_designer_target))

    res_path = os.path.join(MARIO_DIR, "levels", "last_result.txt")
    if not os.path.exists(res_path):
        return jsonify({"status": "Waiting", "message": "Game in progress..."})

    stdout_text = ""
    try:
        with open(res_path, "r", encoding="utf-8", errors="replace") as f:
            stdout_text = f.read()
    except Exception:
        return jsonify({"status": "Waiting", "message": "Reading result..."})

    if "SESSION_UPDATE:" not in stdout_text:
        return jsonify({"status": "Waiting", "message": "Game in progress..."})

    session_update = {
        "won": False,
        "lives": 3,
        "coins": 0,
        "completion_pct": 0.0,
        "mario_mode": 0,
        "kills": 0,
        "total_enemies": 5,
        "hurts": 0,
        "jumps": 0
    }

    # Check both last_result.txt paths (Mario-AI-Framework/last_result.txt and Mario-AI-Framework/levels/last_result.txt)
    possible_paths = [
        os.path.join(MARIO_DIR, "last_result.txt"),
        os.path.join(MARIO_DIR, "levels", "last_result.txt"),
        os.path.abspath("last_result.txt")
    ]
    
    last_res_content = ""
    for p in possible_paths:
        if os.path.exists(p):
            try:
                with open(p, "r") as f:
                    last_res_content = f.read()
                if last_res_content.strip():
                    break
            except Exception:
                pass

    if last_res_content:
        raw_parts = last_res_content.replace("SESSION_UPDATE:", "").strip().split(":")
        kv_pairs = {}
        for item in raw_parts:
            if "=" in item:
                k, v = item.split("=", 1)
                kv_pairs[k.strip().upper()] = v.strip()

        session_update["won"] = (kv_pairs.get("WON", "false").lower() == "true")
        session_update["lives"] = int(kv_pairs.get("LIVES", 3))
        session_update["coins"] = int(kv_pairs.get("COINS", 0))
        session_update["kills"] = int(kv_pairs.get("KILLS", 0))
        session_update["total_enemies"] = int(kv_pairs.get("TOTAL_ENEMIES", 5))
        session_update["hurts"] = int(kv_pairs.get("HURTS", 0))
        session_update["jumps"] = int(kv_pairs.get("JUMPS", 0))
        session_update["mario_mode"] = int(kv_pairs.get("MODE", 0))
        if "COMPLETION" in kv_pairs:
            try:
                session_update["completion_pct"] = float(kv_pairs["COMPLETION"])
            except ValueError:
                pass

    if current_lvl_num not in ACTIVE_DEATH_ZONES:
        ACTIVE_DEATH_ZONES[current_lvl_num] = []

    # Determine which level slot is being evaluated / adjusted
    if session_update["won"]:
        session_update["struggle_reason"] = "Course Clear! Flagpole reached."
        target_lvl_num = current_lvl_num + 1
        target_fallback = next_designer_target
    else:
        pct_int = int(session_update["completion_pct"] * 100)
        session_update["struggle_reason"] = f"Died at {pct_int}% distance."
        death_x = int(session_update["completion_pct"] * 220)
        death_x = max(10, min(200, death_x))
        death_marker = {
            "x": death_x,
            "y": 11,
            "intensity": 1.0,
            "reason": session_update["struggle_reason"],
            "completion_pct": session_update["completion_pct"]
        }
        ACTIVE_DEATH_ZONES[current_lvl_num].append(death_marker)
        target_lvl_num = current_lvl_num
        target_fallback = current_designer_target

    # Determine authoritative immutable designer baseline for target_lvl_num
    if 1 <= target_lvl_num <= len(ACTIVE_DESIGNER_CURVE):
        baseline_target = float(ACTIVE_DESIGNER_CURVE[target_lvl_num - 1])
    else:
        req_base = data.get("baseline_target", data.get("baseline_designer_target", None))
        baseline_target = float(req_base) if req_base is not None else float(target_fallback)

    adjustment = ACTIVE_SESSION_DDA.calculate_adjustment(
        baseline_target,
        {
            "won": session_update["won"],
            "lives_lost": 0 if session_update["won"] else 1,
            "completion_pct": session_update["completion_pct"] if session_update["completion_pct"] > 0 else (1.0 if session_update["won"] else 0.4),
            "time_taken": 30.0,
            "target_time": 40.0,
            "mario_mode": session_update["mario_mode"]
        },
        baseline_target=baseline_target
    )

    # STRICT CLAMP: Guarantee adjusted target difficulty never exceeds ±max_variance (±10% / ±0.10) relative to designer baseline
    max_var = getattr(ACTIVE_SESSION_DDA, "max_variance", 0.10)
    hard_min = max(0.0, baseline_target - max_var)
    hard_max = min(1.0, baseline_target + max_var)
    clamped_target = round(max(hard_min, min(hard_max, float(adjustment["adjusted_target"]))), 3)
    clamped_delta = round(clamped_target - baseline_target, 3)
    clamped_delta = max(-max_var, min(max_var, clamped_delta))

    adjustment["designer_target"] = baseline_target
    adjustment["adjusted_target"] = clamped_target
    adjustment["delta"] = clamped_delta
    adjustment["delta_pct"] = f"{clamped_delta * 100:+.1f}%"

    current_level_text = data.get("current_level_text", None)

    if not session_update["won"]:
        total_d = len(ACTIVE_DEATH_ZONES[current_lvl_num])
        adjustment["reason"] = f"Player struggling on Level {current_lvl_num} ({total_d} death(s)). Level {current_lvl_num} difficulty reduced by DDA micro-adjustment."

        if current_level_text and current_level_text.strip():
            modified_text, structural_changes = tweak_level_for_dda(current_level_text, adjustment["delta"], telemetry=session_update)
            next_level = {
                "level": current_lvl_num,
                "designer_target": baseline_target,
                "target_difficulty": adjustment["adjusted_target"],
                "estimated_difficulty": calculate_difficulty(modified_text),
                "level_text": modified_text,
                "structural_changes": structural_changes
            }
        else:
            single_pipe = generate_single_level_pipeline(adjustment["adjusted_target"])
            next_level = {
                "level": current_lvl_num,
                "designer_target": baseline_target,
                "target_difficulty": adjustment["adjusted_target"],
                "estimated_difficulty": single_pipe["estimated_difficulty"],
                "level_text": single_pipe["level_text"],
                "structural_changes": ["Generated adapted level layout for retry"]
            }
    else:
        single_pipe = generate_single_level_pipeline(adjustment["adjusted_target"])
        next_level = {
            "level": target_lvl_num,
            "designer_target": baseline_target,
            "target_difficulty": adjustment["adjusted_target"],
            "estimated_difficulty": single_pipe["estimated_difficulty"],
            "level_text": single_pipe["level_text"],
            "structural_changes": ["Generated pre-adjusted level layout for unlocked level"]
        }

    return jsonify({
        "status": "Success",
        "session_update": session_update,
        "dda_adjustment": adjustment,
        "next_level": next_level,
        "death_info": {
            "died": len(ACTIVE_DEATH_ZONES[current_lvl_num]) > 0,
            "total_deaths": len(ACTIVE_DEATH_ZONES[current_lvl_num]),
            "death_coordinates": ACTIVE_DEATH_ZONES[current_lvl_num]
        }
    })

# Explanation: Retrieves recorded player death coordinates for rendering death zone reticle overlays.
@app.route('/api/telemetry/death-zone/<int:level_id>', methods=['GET'])
@app.route('/api/telemetry/heatmap/<int:level_id>', methods=['GET'])
def get_telemetry_death_zone(level_id):
    """
    Returns ALL cumulative death coordinates [(x, y)] recorded across all playthroughs for level_id.
    Death markers persist across 3-life campaign resets and are only cleared when new level maps are generated.
    """
    deaths = ACTIVE_DEATH_ZONES.get(level_id, [])
    if isinstance(deaths, dict):
        deaths = [deaths] if deaths.get("died", False) else []
    has_died = len(deaths) > 0
    return jsonify({
        "status": "Success",
        "level_id": level_id,
        "died": has_died,
        "death_coordinates": deaths,
        "total_deaths": len(deaths),
        "message": f"Recorded {len(deaths)} total death location(s) for Level {level_id}."
    })

if __name__ == '__main__':
    os.makedirs('templates', exist_ok=True)
    os.makedirs(os.path.join(MARIO_DIR, 'levels'), exist_ok=True)
    print("============================================================")
    print(" MARIO PCG & DDA ADAPTIVE ENGINE SERVER IS READY")
    print(" Access Web UI at: http://127.0.0.1:5000")
    print("============================================================")
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False, threaded=True)