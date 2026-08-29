const fs = require('fs');
const html = fs.readFileSync('templates/index.html', 'utf8');

global.window = global;
global.alert = function(msg) {
    console.log("   [ALERT INTERCEPTED]:", msg);
};

const mockElements = {
    curveChart: { getContext: () => ({}) },
    curveInputsGrid: { innerHTML: '', style: {}, appendChild: () => {} },
    numLevelsDisplay: { innerText: '' },
    presetSelect: { value: 'linear_ramp' },
    levelTabs: { innerHTML: '', appendChild: (c) => { mockElements.levelTabs.children.push(c); }, children: [] },
    btnDeathZone: { disabled: true, style: {}, classList: { add: ()=>{}, remove: ()=>{} } },
    btnWatchAI: { disabled: true, style: {}, classList: { add: ()=>{}, remove: ()=>{} } },
    btnLaunchPlay: { disabled: true, style: {} },
    playerSessionLog: { innerHTML: '', innerText: '' },
    statDesigner: { innerText: '' },
    statDDATarget: { innerText: '' },
    statEstimated: { innerText: '' },
    statResult: { innerText: '', style: {} },
    tileGrid: { innerHTML: '', style: {}, scrollWidth: 2000, scrollHeight: 250 },
    heatmapCanvas: { style: {}, getContext: () => ({ clearRect: ()=>{}, createRadialGradient: ()=>({ addColorStop: ()=>{} }), fillStyle: '', font: '', textAlign: '', textBaseline: '', fillText: ()=>{}, beginPath: ()=>{}, arc: ()=>{}, fill: ()=>{} }) },
    telemetryList: { innerHTML: '', appendChild: () => {} },
    arcadeLevelSelector: { innerHTML: '', appendChild: (c) => { mockElements.arcadeLevelSelector.children.push(c); }, children: [] },
    hudLevel: { innerText: '' },
    hudLives: { innerText: '', style: {} },
    hudCoins: { innerText: '' },
    hudPower: { innerText: '' },
    hudDDAShift: { innerText: '', style: {} },
    playerNextTileGrid: { innerHTML: '', style: {} }
};

global.document = {
    getElementById: function(id) {
        if (mockElements[id]) return mockElements[id];
        if (id.startsWith('p')) {
            const num = parseInt(id.slice(1));
            return { value: (num * 15).toString() };
        }
        return { innerText: '', innerHTML: '', style: {}, appendChild: () => {}, classList: { add: ()=>{}, remove: ()=>{} } };
    },
    querySelectorAll: function() { return []; },
    createElement: function(tag) {
        return { className: '', innerHTML: '', appendChild: () => {}, style: {}, classList: { add: ()=>{}, remove: ()=>{} } };
    }
};

let capturedDatasets = [];
global.Chart = function(ctx, config) {
    capturedDatasets = config.data.datasets;
    return { destroy: () => {} };
};

const scriptCode = html.match(/<script>([\s\S]*?)<\/script>/)[1];

const testRunnerCode = `
${scriptCode}

console.log("=== TEST 1: Page Load (Initial State) ===");
window.onload();
if (capturedDatasets.length === 1 && capturedDatasets[0].label === "Designer Target Curve (0-100)") {
    console.log("[PASS] Test 1A: ONLY designer curve rendered on initial load!");
} else {
    console.error("[FAIL] Test 1A failed! Datasets:", capturedDatasets.length);
    process.exit(1);
}

if (mockElements.tileGrid.innerHTML.includes("Level Map Visualizer Inactive") &&
    mockElements.btnDeathZone.disabled === true &&
    mockElements.btnWatchAI.disabled === true &&
    mockElements.btnLaunchPlay.disabled === true &&
    mockElements.levelTabs.innerHTML.includes("No levels generated yet")) {
    console.log("[PASS] Test 1B: Visualizer & Play button are INACTIVE / DISABLED on fresh page load!");
} else {
    console.error("[FAIL] Test 1B: Inactive guards failed on load!", mockElements);
    process.exit(1);
}

console.log("\\n=== TEST 2: Attempting to Click Play Before Generation ===");
let playTriggered = false;
global.fetch = async function(url) {
    if (url === '/api/play-human-level') {
        playTriggered = true;
    }
    return { json: async () => ({ status: 'Success' }) };
};

launchHumanPlay();
if (!playTriggered && mockElements.playerSessionLog.innerHTML.includes("Cannot Play")) {
    console.log("[PASS] Test 2: Play action blocked before generation with clear guidance message!\\n");
} else {
    console.error("[FAIL] Test 2: Play action was NOT blocked!");
    process.exit(1);
}

console.log("=== TEST 3: Campaign Generation Pipeline Completes ===");
campaignData = {
    history: [
        { level: 1, designer_target: 0.25, target_difficulty: 0.25, estimated_difficulty: 0.27, level_text: "----------------\\n---XXXX---------", player_performance: { played: false } },
        { level: 2, designer_target: 0.45, target_difficulty: 0.45, estimated_difficulty: 0.46, level_text: "----------------\\n---XXXX---------", player_performance: { played: false } },
        { level: 3, designer_target: 0.70, target_difficulty: 0.70, estimated_difficulty: 0.69, level_text: "----------------\\n---XXXX---------", player_performance: { played: false } }
    ]
};
mockElements.levelTabs.children = [];
mockElements.arcadeLevelSelector.children = [];
renderDashboard();

if (capturedDatasets.length === 3 &&
    mockElements.btnDeathZone.disabled === false &&
    mockElements.btnWatchAI.disabled === false &&
    mockElements.btnLaunchPlay.disabled === false &&
    mockElements.tileGrid.innerHTML.includes("tile-X") &&
    mockElements.arcadeLevelSelector.children.length === 3) {
    console.log("[PASS] Test 3A: Visualizer & Play button are ACTIVE with level maps after generation!");
} else {
    console.error("[FAIL] Test 3A failed! Post-generation state invalid.");
    process.exit(1);
}

console.log("\\n=== TEST 4: Death Zone Overlay Scaling Across Full Scrollable Width ===");
renderDeathZoneOverlay([{ x: 10, y: 5 }, { x: 180, y: 12 }]);
if (mockElements.heatmapCanvas.style.width === '2000px' && mockElements.heatmapCanvas.width === 2000) {
    console.log("[PASS] Test 4: Canvas overlay correctly matches full 2000px scrollable width!\\n");
} else {
    console.error("[FAIL] Test 4 failed! Canvas width not matching scrollWidth:", mockElements.heatmapCanvas);
    process.exit(1);
}

console.log("=== TEST 5: 3rd Death Reached (0 Lives Remaining - Game Over Guard) ===");
playerArcadeState.lives = 0;
renderArcadeLevelSelector();
updateArcadeHUD();

if (mockElements.btnLaunchPlay.disabled === true && mockElements.hudLives.innerText === "❤️ 0") {
    console.log("[PASS] Test 5A: Play button disabled and HUD shows 0 lives on Game Over!");
} else {
    console.error("[FAIL] Test 5A failed! Play button not disabled when lives = 0.");
    process.exit(1);
}

let gameOverPlayTriggered = false;
global.fetch = async function(url) {
    if (url === '/api/play-human-level') {
        gameOverPlayTriggered = true;
    }
    return { json: async () => ({ status: 'Success' }) };
};
launchHumanPlay();

if (!gameOverPlayTriggered && mockElements.playerSessionLog.innerHTML.includes("GAME OVER")) {
    console.log("[PASS] Test 5B: launchHumanPlay correctly blocked when lives <= 0!");
} else {
    console.error("[FAIL] Test 5B failed! launchHumanPlay allowed when lives <= 0.");
    process.exit(1);
}

resetCampaign();
if (playerArcadeState.lives === 3 && mockElements.btnLaunchPlay.disabled === false && mockElements.hudLives.innerText === "❤️ 3") {
    console.log("[PASS] Test 5C: resetCampaign restores 3 lives and re-enables Play button!\\n");
} else {
    console.error("[FAIL] Test 5C failed! resetCampaign did not restore lives properly.");
    process.exit(1);
}

console.log("=== ALL TESTS PASSED WITH 100% SUCCESS! ===");
`;

eval(testRunnerCode);
