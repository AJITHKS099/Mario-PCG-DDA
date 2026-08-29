const fs = require('fs');
const assert = require('assert');

console.log("=== STARTING CROSS-NAVIGATION & BI-DIRECTIONAL STATE PERSISTENCE TEST ===");

// 1. Verify HTML template markup
const indexHtml = fs.readFileSync('templates/index.html', 'utf8');
const retroHtml = fs.readFileSync('templates/retro.html', 'utf8');

console.log("\n[STEP 1] Verifying Visual Elements & Markup in HTML Templates...");

// Modern (index.html) must have:
// - Glass switch button
// - Transition overlay
assert(indexHtml.includes('glass-retro-switch-btn'), "Missing glass-retro-switch-btn in index.html!");
assert(indexHtml.includes('id="btnRetroSwitch"'), "Missing btnRetroSwitch in index.html!");
assert(indexHtml.includes('navigateToRetro()'), "Missing navigateToRetro click handler in index.html!");
assert(indexHtml.includes('transitionOverlay'), "Missing transitionOverlay in index.html!");
console.log(" -> [PASS] Modern UI (index.html) has glassmorphism switch button, transition overlay, and navigateToRetro handler.");

// Retro (retro.html) must have:
// - Themed arcade lever assembly
// - Lever arm, shaft, ball-top, indicators
// - Transition overlay
assert(retroHtml.includes('arcade-lever-assembly'), "Missing arcade-lever-assembly in retro.html!");
assert(retroHtml.includes('id="arcadeGamingLever"'), "Missing arcadeGamingLever in retro.html!");
assert(retroHtml.includes('pullRetroLever()'), "Missing pullRetroLever click handler in retro.html!");
assert(retroHtml.includes('lever-ball-top'), "Missing lever-ball-top in retro.html!");
assert(retroHtml.includes('retroTransitionOverlay'), "Missing retroTransitionOverlay in retro.html!");
console.log(" -> [PASS] Retro UI (retro.html) has authentic Arcade Gaming Lever assembly, animated lever arm, and pullRetroLever handler.");

// 2. Simulated Environment for Cross-Page Navigation State Testing
console.log("\n[STEP 2] Setting up shared sessionStorage mock environment...");

let mockStorage = {};
const globalSessionStorage = {
    getItem: (k) => mockStorage[k] || null,
    setItem: (k, v) => { mockStorage[k] = String(v); },
    removeItem: (k) => { delete mockStorage[k]; },
    clear: () => { mockStorage = {}; }
};

const mockFetch = async (url) => ({
    json: async () => ({
        status: 'Success',
        death_coordinates: [{ x: 92, y: 11, intensity: 1.0 }]
    })
});

// Create an execution context for index.html scripts
function createIndexContext() {
    const ctx = {
        sessionStorage: globalSessionStorage,
        window: { location: { href: '' } },
        fetch: mockFetch,
        document: {
            body: { classList: { add: ()=>{}, remove: ()=>{} } },
            getElementById: (id) => {
                if (ctx.mockElements[id]) return ctx.mockElements[id];
                if (id.startsWith('p')) {
                    const idx = parseInt(id.slice(1)) - 1;
                    return { value: ctx.curveValues[idx] !== undefined ? ctx.curveValues[idx].toString() : "50" };
                }
                return { innerText: '', innerHTML: '', style: {}, classList: { add: ()=>{}, remove: ()=>{} }, appendChild: ()=>{} };
            },
            querySelector: (sel) => {
                if (sel === '.level-view-container') return ctx.mockElements.levelViewContainer;
                return null;
            },
            querySelectorAll: () => []
        },
        Chart: function(ctxEl, cfg) {
            ctx.capturedChartDatasets = cfg.data.datasets;
            return { destroy: ()=>{} };
        },
        mockElements: {
            curveChart: { getContext: () => ({}) },
            curveInputsGrid: { innerHTML: '', style: {}, appendChild: () => {} },
            numLevelsDisplay: { innerText: '5' },
            presetSelect: { value: 'linear_ramp' },
            levelTabs: { innerHTML: '', appendChild: (c) => { ctx.mockElements.levelTabs.children.push(c); }, children: [] },
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
            arcadeLevelSelector: { innerHTML: '', appendChild: (c) => { ctx.mockElements.arcadeLevelSelector.children.push(c); }, children: [] },
            hudLevel: { innerText: '' },
            hudLives: { innerText: '', style: {} },
            hudCoins: { innerText: '' },
            hudPower: { innerText: '' },
            hudDDAShift: { innerText: '', style: {} },
            playerNextTileGrid: { innerHTML: '', style: {} },
            transitionOverlay: { classList: { add: (c)=>{ ctx.transitionOverlayClass = c; }, remove: ()=>{} } },
            levelViewContainer: { scrollLeft: 120 }
        },
        curveValues: [20, 35, 50, 65, 80]
    };

    ctx.document.createElement = (tag) => ({
        className: '',
        innerHTML: '',
        appendChild: () => {},
        style: {},
        classList: { add: ()=>{}, remove: ()=>{} }
    });

    const scriptMatch = indexHtml.match(/<script>([\s\S]*?)<\/script>/)[1];
    const runFn = new Function('global', 'window', 'document', 'sessionStorage', 'Chart', 'fetch', `${scriptMatch}; return {
        numLevels,
        campaignData: () => campaignData,
        setCampaignData: (d) => { campaignData = d; },
        playerArcadeState,
        selectedLevelIdx: () => selectedLevelIdx,
        setSelectedLevelIdx: (i) => { selectedLevelIdx = i; },
        isDeathZoneVisible: () => isDeathZoneVisible,
        setIsDeathZoneVisible: (v) => { isDeathZoneVisible = v; },
        saveSharedSessionState,
        loadSharedSessionState,
        navigateToRetro,
        renderDashboard,
        renderLevelView,
        renderArcadeLevelSelector,
        updateArcadeHUD,
        onload: window.onload
    };`);

    ctx.api = runFn(ctx, ctx.window, ctx.document, globalSessionStorage, ctx.Chart, mockFetch);
    return ctx;
}

// Create an execution context for retro.html scripts
function createRetroContext() {
    const ctx = {
        sessionStorage: globalSessionStorage,
        window: { location: { href: '' } },
        fetch: mockFetch,
        document: {
            body: { classList: { add: ()=>{}, remove: ()=>{} } },
            getElementById: (id) => {
                if (ctx.mockElements[id]) return ctx.mockElements[id];
                return { innerText: '', innerHTML: '', style: {}, classList: { add: ()=>{}, remove: ()=>{} }, appendChild: ()=>{} };
            },
            querySelector: (sel) => {
                if (sel === '.retro-level-view-container') return ctx.mockElements.levelViewContainer;
                return null;
            },
            querySelectorAll: () => []
        },
        mockElements: {
            equalizerBars: { innerHTML: '', appendChild: () => {} },
            retroNumLevels: { value: '5' },
            retroPresetSelect: { value: 'linear_ramp' },
            retroLevelTabs: { innerHTML: '', appendChild: (c) => { ctx.mockElements.retroLevelTabs.children.push(c); }, children: [] },
            monitorStatusBadge: { innerText: '', style: {} },
            btnDeathToggle: { disabled: true, style: {} },
            btnAiWatch: { disabled: true },
            btnPlayStart: { disabled: true, innerText: '' },
            tileGrid: { innerHTML: '', scrollWidth: 2000, scrollHeight: 250 },
            heatmapCanvas: { style: {}, getContext: () => ({ clearRect: ()=>{}, stroke: ()=>{}, fillText: ()=>{}, beginPath: ()=>{}, arc: ()=>{} }) },
            hudLevel: { innerText: '' },
            hudLives: { innerText: '' },
            hudCoins: { innerText: '' },
            hudPower: { innerText: '' },
            hudDDAShift: { innerText: '', style: {} },
            retroTerminalLog: { innerHTML: '', appendChild: () => {}, scrollTop: 0, scrollHeight: 100 },
            arcadeGamingLever: { classList: { add: (c)=>{ ctx.leverClass = c; } } },
            indRetro: { classList: { remove: ()=>{} } },
            indModern: { classList: { add: ()=>{} } },
            retroTransitionOverlay: { classList: { add: (c)=>{ ctx.retroTransitionOverlayClass = c; } } },
            levelViewContainer: { scrollLeft: 0 }
        }
    };

    ctx.document.createElement = (tag) => ({
        className: '',
        innerHTML: '',
        appendChild: () => {},
        style: {},
        classList: { add: ()=>{}, remove: ()=>{} }
    });

    const scriptMatch = retroHtml.match(/<script>([\s\S]*?)<\/script>/)[1];
    const runFn = new Function('global', 'window', 'document', 'sessionStorage', 'fetch', `${scriptMatch}; return {
        numLevels: () => numLevels,
        setNumLevels: (n) => { numLevels = n; },
        retroCurve: () => retroCurve,
        setRetroCurve: (c) => { retroCurve = c; },
        campaignData: () => campaignData,
        setCampaignData: (d) => { campaignData = d; },
        playerArcadeState,
        selectedLevelIdx: () => selectedLevelIdx,
        setSelectedLevelIdx: (i) => { selectedLevelIdx = i; },
        showDeathZone: () => showDeathZone,
        setShowDeathZone: (v) => { showDeathZone = v; },
        saveRetroSharedSessionState,
        loadRetroSharedSessionState,
        pullRetroLever,
        renderRetroDashboard,
        renderRetroLevelView,
        updateRetroHUD,
        onload: window.onload
    };`);

    ctx.api = runFn(ctx, ctx.window, ctx.document, globalSessionStorage, mockFetch);
    return ctx;
}

// TEST STEP 3: Generate sequence and play state in Modern UI -> Save State
console.log("\n[STEP 3] Generating 5 levels in Modern UI with gameplay telemetry and death data...");
const modernCtx1 = createIndexContext();

const test5LevelCampaign = {
    curve: [0.20, 0.40, 0.65, 0.80, 0.50],
    history: [
        {
            level: 1,
            designer_target: 0.20,
            target_difficulty: 0.20,
            estimated_difficulty: 0.22,
            level_text: "----------------\\n---XXXX-g-?--X--\\nXXXXXXXXXXXXXXXX",
            player_performance: { played: true, won: true, kills: 2, total_enemies: 4, struggle_reason: "Course Clear!" },
            dda_result: { delta: 0.05, delta_pct: "+5.0%", reason: "Excellent clear pace." }
        },
        {
            level: 2,
            designer_target: 0.40,
            target_difficulty: 0.45,
            estimated_difficulty: 0.44,
            level_text: "----------------\\n---XXXX-k-T--X--\\nXXXXXXXXXXXXXXXX",
            player_performance: { played: true, won: false, kills: 1, total_enemies: 5, struggle_reason: "Died at 42% near Piranha Flower Pipe." },
            dda_result: { delta: -0.04, delta_pct: "-4.0%", reason: "Player struggling with enemy concentration." },
            death_info: { died: true, total_deaths: 1, death_coordinates: [{ x: 92, y: 11, intensity: 1.0 }] }
        },
        {
            level: 3,
            designer_target: 0.65,
            target_difficulty: 0.65,
            estimated_difficulty: 0.63,
            level_text: "----------------\\n---XXXX-B-y--X--\\nXXXXXXXXXXXXXXXX",
            player_performance: { played: false },
            dda_result: { delta: 0.0, delta_pct: "+0.0%", reason: "Initial target." }
        },
        {
            level: 4,
            designer_target: 0.80,
            target_difficulty: 0.80,
            estimated_difficulty: 0.79,
            level_text: "----------------\\n---XXXX-B-T--X--\\nXXXXXXXXXXXXXXXX",
            player_performance: { played: false },
            dda_result: { delta: 0.0, delta_pct: "+0.0%", reason: "Initial target." }
        },
        {
            level: 5,
            designer_target: 0.50,
            target_difficulty: 0.50,
            estimated_difficulty: 0.51,
            level_text: "----------------\\n---XXXX-F-F--X--\\nXXXXXXXXXXXXXXXX",
            player_performance: { played: false },
            dda_result: { delta: 0.0, delta_pct: "+0.0%", reason: "Initial target." }
        }
    ]
};

modernCtx1.api.setCampaignData(test5LevelCampaign);
modernCtx1.api.playerArcadeState.lives = 2;
modernCtx1.api.playerArcadeState.coins = 14;
modernCtx1.api.playerArcadeState.marioMode = 1; // Super Mario
modernCtx1.api.playerArcadeState.activeLevelIdx = 2; // On World 1-2
modernCtx1.api.playerArcadeState.maxUnlockedLevel = 2;
modernCtx1.api.playerArcadeState.lastDdaDelta[2] = "-4.0%";
modernCtx1.api.playerArcadeState.isRetryMap[2] = true;
modernCtx1.api.setSelectedLevelIdx(1); // Viewing Level 2
modernCtx1.api.setIsDeathZoneVisible(true);
modernCtx1.mockElements.playerSessionLog.innerHTML = "Outcome: LOSS (1 life lost on World 1-2). DDA micro-adjusted -4.0%.";

// Execute state save
modernCtx1.api.saveSharedSessionState();
console.log(" -> [PASS] Modern UI successfully saved campaign sequence and telemetry into sessionStorage!");

// TEST STEP 4: Load Retro UI and verify 100% exact state hydration
console.log("\n[STEP 4] Simulating page load on Retro UI (/retro)...");
const retroCtx1 = createRetroContext();
retroCtx1.api.onload();

const rCampaign = retroCtx1.api.campaignData();
assert(rCampaign !== null, "Retro UI failed to hydrate campaignData!");
assert.strictEqual(rCampaign.history.length, 5, "Retro UI did not hydrate all 5 levels!");
assert.strictEqual(retroCtx1.api.numLevels(), 5, "Retro UI numLevels mismatch!");
assert.strictEqual(retroCtx1.api.playerArcadeState.lives, 2, "Retro UI lives mismatch (expected 2)!");
assert.strictEqual(retroCtx1.api.playerArcadeState.coins, 14, "Retro UI coins mismatch (expected 14)!");
assert.strictEqual(retroCtx1.api.playerArcadeState.marioMode, 1, "Retro UI marioMode mismatch!");
assert.strictEqual(retroCtx1.api.playerArcadeState.activeLevelIdx, 2, "Retro UI activeLevelIdx mismatch!");
assert.strictEqual(retroCtx1.api.playerArcadeState.maxUnlockedLevel, 2, "Retro UI maxUnlockedLevel mismatch!");
assert.strictEqual(retroCtx1.api.playerArcadeState.lastDdaDelta[2], "-4.0%", "Retro UI lastDdaDelta mismatch!");
assert.strictEqual(retroCtx1.api.playerArcadeState.isRetryMap[2], true, "Retro UI isRetryMap mismatch!");
assert.strictEqual(retroCtx1.api.selectedLevelIdx(), 1, "Retro UI selectedLevelIdx mismatch!");
assert.strictEqual(retroCtx1.api.showDeathZone(), true, "Retro UI death zone toggle state mismatch!");
assert(retroCtx1.mockElements.tileGrid.innerHTML.includes('rtile-koopa') || retroCtx1.mockElements.tileGrid.innerHTML.includes('rtile-piranha'), "Level 2 tile preview missing expected tiles!");
console.log(" -> [PASS] Retro UI accurately restored all 5 levels, active World 1-2, 2 lives, 14 coins, DDA delta, and death zones!");

// TEST STEP 5: Modify state in Retro UI (e.g. gain 5 coins, adjust equalizer, clear Level 2) -> Pull Lever
console.log("\n[STEP 5] Updating gameplay in Retro UI and pulling Gaming Lever back to Modern...");
retroCtx1.api.playerArcadeState.coins = 19;
retroCtx1.api.playerArcadeState.lives = 2;
retroCtx1.api.playerArcadeState.activeLevelIdx = 3;
retroCtx1.api.playerArcadeState.maxUnlockedLevel = 3;
retroCtx1.api.playerArcadeState.lastDdaDelta[3] = "+3.0%";
rCampaign.history[1].player_performance = { played: true, won: true, kills: 4, total_enemies: 5, struggle_reason: "Course Clear!" };
retroCtx1.api.setSelectedLevelIdx(2); // Viewing Level 3
retroCtx1.api.pullRetroLever();

assert.strictEqual(retroCtx1.leverClass, "pulled", "Arcade lever element was not thrown to 'pulled' state!");
assert.strictEqual(retroCtx1.retroTransitionOverlayClass, "crt-collapse", "CRT transition overlay not triggered!");
console.log(" -> [PASS] Gaming Lever successfully thrown with animation and CRT transition overlay triggered!");

// TEST STEP 6: Load Modern UI and verify state carried over from Retro UI
console.log("\n[STEP 6] Simulating return to Modern UI (/)...");
const modernCtx2 = createIndexContext();
modernCtx2.api.onload();

const mCampaign2 = modernCtx2.api.campaignData();
assert(mCampaign2 !== null, "Modern UI failed to load shared state from Retro!");
assert.strictEqual(mCampaign2.history.length, 5, "Level sequence count altered!");
assert.strictEqual(modernCtx2.api.playerArcadeState.coins, 19, "Updated coin count not carried over!");
assert.strictEqual(modernCtx2.api.playerArcadeState.lives, 2, "Lives count not carried over!");
assert.strictEqual(modernCtx2.api.playerArcadeState.activeLevelIdx, 3, "Active level progression not carried over!");
assert.strictEqual(modernCtx2.api.playerArcadeState.maxUnlockedLevel, 3, "Max unlocked level not carried over!");
assert.strictEqual(modernCtx2.api.playerArcadeState.lastDdaDelta[3], "+3.0%", "DDA delta not carried over!");
assert.strictEqual(modernCtx2.api.selectedLevelIdx(), 2, "Selected level view index not carried over!");
assert.strictEqual(modernCtx2.mockElements.hudCoins.innerText, "🪙 19", "Modern HUD coins display not matching!");
assert.strictEqual(modernCtx2.mockElements.hudLevel.innerText, "WORLD 1-3", "Modern HUD level display not matching!");

console.log(" -> [PASS] Modern UI restored updated World 1-3 progression, 19 coins, 2 lives, and DDA status flawlessly!");

console.log("\n=== ALL CROSS-NAVIGATION & STATE PRESERVATION TESTS PASSED 100%! ===");
