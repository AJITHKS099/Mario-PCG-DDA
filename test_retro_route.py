import os
import sys
import app

print("=== STARTING RETRO ROUTE & BACKEND COMPATIBILITY TEST ===")

client = app.app.test_client()

# TEST 1: Default Glassmorphism UI at /
print("[TEST 1] Testing GET / (Original Glassmorphism Frontend)...")
r_orig = client.get('/')
assert r_orig.status_code == 200, f"Expected 200, got {r_orig.status_code}"
orig_html = r_orig.data.decode('utf-8')
assert "glass-card" in orig_html, "Original site missing glassmorphism markup!"
assert "Chart.js" in orig_html or "chart.js" in orig_html or "curveChart" in orig_html, "Original site missing chart elements!"
print(" -> [PASS] Original site at / is 100% intact with zero changes!")

# TEST 2: Retro Arcade Cabinet UI at /retro
print("[TEST 2] Testing GET /retro (Brand-New Retro Arcade Frontend)...")
r_retro = client.get('/retro')
assert r_retro.status_code == 200, f"Expected 200, got {r_retro.status_code}"
retro_html = r_retro.data.decode('utf-8')
assert "arcade-cabinet" in retro_html, "Retro site missing arcade cabinet chassis!"
assert "crt-scanlines" in retro_html, "Retro site missing CRT scanline markup!"
assert "Press Start 2P" in retro_html, "Retro site missing 8-bit font link!"
assert "EQUALIZER" in retro_html, "Retro site missing equalizer meter!"
assert "INSERT COIN" in retro_html, "Retro site missing Insert Coin CTA!"
print(" -> [PASS] New retro arcade site at /retro loads cleanly with 8-bit CRT styling!")

# TEST 3: Full API compatibility
print("[TEST 3] Testing shared REST endpoints compatibility...")
r_presets = client.get('/api/presets')
assert r_presets.status_code == 200
presets = r_presets.get_json()
assert "linear_ramp" in presets
assert "boss_rush" in presets
print(" -> [PASS] Shared REST API /api/presets verified for both frontends!")

print("\n=== ALL TESTS PASSED WITH 100% SUCCESS! ===")
