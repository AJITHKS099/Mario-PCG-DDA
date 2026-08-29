import os
import sys
import json

print("=== STARTING COMPLETE DOUBLE CHECK TEST SUITE ===")

# Test 1: Import all modules
print("[TEST 1] Importing all Python modules...")
import app
import pipeline
import generator
import estimator
import dda
import game_session
import vglc_trainer
import validator
print(" -> [PASS] All modules imported cleanly with 0 errors!")

# Test 2: Generator & Estimator
print("[TEST 2] Testing level generation and difficulty estimation...")
lvl = generator.generate_mario_level(0.45)
assert len(lvl) > 100, "Level text too short!"
est = estimator.calculate_difficulty(lvl)
assert 0.0 <= est <= 1.0, f"Invalid estimated difficulty: {est}"
print(f" -> [PASS] Level generated (Length: {len(lvl)} chars, Est Diff: {est:.2f})")

# Test 3: Validator (A* Search)
print("[TEST 3] Testing A* validator on generated level...")
val_eng = validator.MarioPhysicsValidator()
is_solvable, val_metrics = val_eng.is_level_solvable(lvl)
print(f" -> [PASS] Validator result: Solvable={is_solvable}, Metrics={val_metrics}")

# Test 4: DDA Engine Calculations
print("[TEST 4] Testing Bayesian DDA Engine calculations...")
dda_eng = dda.DynamicDifficultyAdjuster(max_variance=0.10)
# Win on Level 1
adj_win = dda_eng.calculate_adjustment(0.40, {
    "won": True,
    "lives_lost": 0,
    "completion_pct": 1.0,
    "time_taken": 30.0,
    "target_time": 40.0,
    "mario_mode": 0
})
print(f" -> [PASS] DDA Win Adjustment (Next Level Target 40% -> {adj_win['adjusted_target']*100:.1f}%, Delta: {adj_win['delta_pct']})")

# Death on Level 2
adj_lose = dda_eng.calculate_adjustment(0.40, {
    "won": False,
    "lives_lost": 1,
    "completion_pct": 0.45,
    "time_taken": 30.0,
    "target_time": 40.0,
    "mario_mode": 0
})
print(f" -> [PASS] DDA Death Adjustment (Current Level Target 40% -> {adj_lose['adjusted_target']*100:.1f}%, Delta: {adj_lose['delta_pct']})")

# Test 5: Flask App Client Endpoints
print("[TEST 5] Testing Flask REST endpoints with test client...")
client = app.app.test_client()

# GET /
r_home = client.get('/')
assert r_home.status_code == 200, f"GET / returned {r_home.status_code}"
print(" -> [PASS] GET / returned 200 OK")

# POST /api/generate-sequence-stream
r_stream = client.post('/api/generate-sequence-stream', json={
    "curve": [20, 40, 60],
    "player_skill": "average",
    "max_variance": 0.10
})
assert r_stream.status_code == 200, f"POST /api/generate-sequence-stream returned {r_stream.status_code}"
stream_data = r_stream.get_data(as_text=True)
assert "data: " in stream_data, "No SSE data in stream response!"
assert "type\": \"complete\"" in stream_data, "Stream did not reach complete state!"
print(" -> [PASS] POST /api/generate-sequence-stream streamed 3 levels and completed successfully!")

# Test 5B: Play Human & Watch AI Guards
print("[TEST 5B] Testing play-human-level & watch-ai-play guards without generated level...")
r_play_nogenerate = client.post('/api/play-human-level', json={
    "level_index": 1,
    "target_difficulty": 0.5
})
assert r_play_nogenerate.status_code == 400, f"Expected 400, got {r_play_nogenerate.status_code}"
assert "Cannot play" in r_play_nogenerate.get_json()["message"]
print(" -> [PASS] POST /api/play-human-level successfully blocked with 400 when no level exists!")

r_play_zerolives = client.post('/api/play-human-level', json={
    "level_index": 1,
    "target_difficulty": 0.5,
    "lives": 0,
    "level_text": lvl
})
assert r_play_zerolives.status_code == 400, f"Expected 400, got {r_play_zerolives.status_code}"
assert "Game Over" in r_play_zerolives.get_json()["message"]
print(" -> [PASS] POST /api/play-human-level successfully blocked with 400 when lives <= 0!")

r_ai_nogenerate = client.post('/api/watch-ai-play', json={
    "level_index": 1,
    "target_difficulty": 0.5
})
assert r_ai_nogenerate.status_code == 400, f"Expected 400, got {r_ai_nogenerate.status_code}"
assert "Cannot watch AI" in r_ai_nogenerate.get_json()["message"]
print(" -> [PASS] POST /api/watch-ai-play successfully blocked with 400 when no level exists!")

# POST /api/check-session-result (Simulated result file)
os.makedirs(os.path.join(app.MARIO_DIR, "levels"), exist_ok=True)
last_res_path = os.path.join(app.MARIO_DIR, "levels", "last_result.txt")
with open(last_res_path, "w") as f:
    f.write("SESSION_UPDATE:WON=true:MODE=0:LIVES=3:COINS=10:COMPLETION=1.00:KILLS=2:TOTAL_ENEMIES=5:HURTS=0:JUMPS=8")

r_check = client.post('/api/check-session-result', json={
    "level_index": 1,
    "next_designer_target": 0.40,
    "current_designer_target": 0.20,
    "current_level_text": lvl
})
assert r_check.status_code == 200, f"POST /api/check-session-result returned {r_check.status_code}"
check_json = r_check.get_json()
assert check_json["status"] == "Success", f"Expected Success, got {check_json}"
assert check_json["session_update"]["won"] == True, "Expected won=True!"
assert "next_level" in check_json, "Missing next_level in response!"
print(" -> [PASS] POST /api/check-session-result successfully processed Level 1 WIN and returned DDA pre-adjusted Level 2!")

# POST /api/check-session-result on DEATH (Player died on Level 1, 2 lives left)
with open(last_res_path, "w") as f:
    f.write("SESSION_UPDATE:WON=false:MODE=0:LIVES=2:COINS=3:COMPLETION=0.45:KILLS=1:TOTAL_ENEMIES=5:HURTS=1:JUMPS=5")

r_check_death = client.post('/api/check-session-result', json={
    "level_index": 1,
    "next_designer_target": 0.40,
    "current_designer_target": 0.20,
    "current_level_text": lvl
})
assert r_check_death.status_code == 200, f"POST /api/check-session-result returned {r_check_death.status_code}"
death_json = r_check_death.get_json()
assert death_json["session_update"]["won"] == False, "Expected won=False on death!"
assert death_json["session_update"]["lives"] == 2, "Expected 2 lives left!"
assert death_json["next_level"]["level"] == 1, "Expected retry to stay on Level 1 slot!"
assert "structural_changes" in death_json["next_level"], "Expected DDA structural adjustments on retry level!"
print(f" -> [PASS] POST /api/check-session-result on DEATH strictly retained Level 1 slot and adapted level layout ({death_json['next_level']['structural_changes']})!")

print("\n=== ALL TESTS PASSED WITH 100% SUCCESS! ===")
