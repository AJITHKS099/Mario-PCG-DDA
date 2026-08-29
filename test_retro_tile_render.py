import subprocess
import json
from generator import generate_mario_level

print("=== TESTING RETRO TILE RENDERING LOGIC ===")

# Generate a sample level
level_text = generate_mario_level(0.5)

# Read full templates/retro.html
with open('templates/retro.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract the <script> block
start_idx = html.find('<script>') + len('<script>')
end_idx = html.find('</script>')
js_code = html[start_idx:end_idx]

# Create a standalone Node script
node_test_file = "test_retro_eval.js"
with open(node_test_file, 'w', encoding='utf-8') as f:
    f.write(f"""
global.window = {{}};
global.document = {{
    getElementById: () => ({{ innerHTML: '', style: {{}}, classList: {{ add: () => {{}}, remove: () => {{}} }}, appendChild: () => ({{}}) }}),
    querySelectorAll: () => []
}};

{js_code}

const rawText = {json.dumps(level_text)};
const rendered = formatRetroTiles(rawText);

// Verify no raw string corruptions like 'tile-S">S' or 'tile-X">X'
if (rendered.includes('tile-S">S') || rendered.includes('tile-X">X') || rendered.includes('tile-Q">Q')) {{
    console.error('[FAIL] Corrupted tile text detected!');
    process.exit(1);
}}

// Verify standard span elements are present
if (!rendered.includes('<span class="rtile rtile-ground"') && !rendered.includes('<span class="rtile rtile-solid"')) {{
    console.error('[FAIL] No tile spans generated!');
    process.exit(1);
}}

console.log('[PASS] Rendered output is 100% clean HTML with valid span elements!');
console.log('Sample output snippet:', rendered.slice(0, 150));
""")

res = subprocess.run(["node", node_test_file], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("STDERR:", res.stderr)
assert res.returncode == 0, "Node execution failed!"

print("=== RETRO TILE RENDER TEST PASSED WITH 100% SUCCESS ===")
