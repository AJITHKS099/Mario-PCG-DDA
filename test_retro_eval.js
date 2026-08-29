
global.window = {};
global.document = {
    getElementById: () => ({ innerHTML: '', style: {}, classList: { add: () => {}, remove: () => {} }, appendChild: () => ({}) }),
    querySelectorAll: () => []
};


        // RETRO ARCADE GLOBAL STATE
        let numLevels = 5;
        let retroCurve = [20, 35, 50, 65, 80]; // 0-100% scale
        let campaignData = null;
        let selectedLevelIdx = 0;
        let showDeathZone = false;
        let browserGameLoopId = null;

        let playerArcadeState = {
            activeLevelIdx: 1,
            maxUnlockedLevel: 1,
            lives: 3,
            coins: 0,
            marioMode: 0,
            levelTargets: [0.20, 0.35, 0.50, 0.65, 0.80],
            levelTexts: {},
            lastDdaDelta: {},
            isRetryMap: {}
        };

        const PRESETS = {
            "linear_ramp": [20, 35, 50, 65, 80],
            "mid_spike": [25, 45, 85, 35, 70],
            "wave_pacing": [30, 60, 40, 75, 50, 85],
            "boss_rush": [30, 40, 55, 70, 95]
        };

        // RENDER 8-BIT EQUALIZER BARS
        function renderEqualizer() {
            const container = document.getElementById('equalizerBars');
            if (!container) return;
            container.innerHTML = '';

            for (let i = 0; i < numLevels; i++) {
                const val = retroCurve[i] || 50;
                const col = document.createElement('div');
                col.className = 'eq-column';

                const btnUp = document.createElement('button');
                btnUp.className = 'eq-btn';
                btnUp.innerText = '+';
                btnUp.onclick = () => adjustEqVal(i, 5);

                const meter = document.createElement('div');
                meter.className = 'eq-meter';

                // 10 LED segments (10% each)
                const activeSegments = Math.round(val / 10);
                for (let s = 1; s <= 10; s++) {
                    const seg = document.createElement('div');
                    seg.className = 'eq-segment';
                    if (s <= activeSegments) {
                        seg.classList.add('active');
                        if (s <= 4) seg.classList.add('tier-low');
                        else if (s <= 7) seg.classList.add('tier-mid');
                        else seg.classList.add('tier-high');
                    }
                    meter.appendChild(seg);
                }

                const btnDown = document.createElement('button');
                btnDown.className = 'eq-btn';
                btnDown.innerText = '-';
                btnDown.onclick = () => adjustEqVal(i, -5);

                const label = document.createElement('div');
                label.className = 'eq-label';
                label.innerText = `L${i + 1}`;

                const valDisplay = document.createElement('div');
                valDisplay.className = 'eq-val';
                valDisplay.innerText = `${val}%`;

                col.appendChild(btnUp);
                col.appendChild(meter);
                col.appendChild(btnDown);
                col.appendChild(label);
                col.appendChild(valDisplay);

                container.appendChild(col);
            }
        }

        function adjustEqVal(idx, delta) {
            retroCurve[idx] = Math.max(5, Math.min(95, (retroCurve[idx] || 50) + delta));
            renderEqualizer();
            saveRetroSharedSessionState();
        }

        function applyRetroPreset() {
            const presetKey = document.getElementById('retroPresetSelect').value;
            const presetArr = PRESETS[presetKey];
            if (presetArr) {
                numLevels = presetArr.length;
                document.getElementById('retroNumLevels').value = numLevels.toString();
                retroCurve = [...presetArr];
                renderEqualizer();
                saveRetroSharedSessionState();
            }
        }

        function changeRetroNumLevels() {
            numLevels = parseInt(document.getElementById('retroNumLevels').value) || 5;
            while (retroCurve.length < numLevels) {
                const prev = retroCurve[retroCurve.length - 1] || 50;
                retroCurve.push(Math.min(95, prev + 10));
            }
            if (retroCurve.length > numLevels) {
                retroCurve = retroCurve.slice(0, numLevels);
            }
            renderEqualizer();
            saveRetroSharedSessionState();
        }

        // NES COLORIZED ASCII PIXEL TILE FORMATTER
        function formatRetroTiles(rawText) {
            if (!rawText) return "";
            let formatted = "";
            for (let i = 0; i < rawText.length; i++) {
                const ch = rawText[i];
                if (ch === 'X') {
                    formatted += '<span class="rtile rtile-ground" title="Ground (X)">X</span>';
                } else if (ch === 'S' || ch === 'D' || ch === '#' || ch === '%') {
                    formatted += '<span class="rtile rtile-solid" title="Solid Block">' + ch + '</span>';
                } else if (ch === '?' || ch === 'Q') {
                    formatted += '<span class="rtile rtile-question" title="Question Block">' + ch + '</span>';
                } else if (ch === '1' || ch === '2') {
                    formatted += '<span class="rtile rtile-hidden" title="Hidden Block (' + (ch === '1' ? '1-Up' : 'Coin') + ')">' + ch + '</span>';
                } else if (ch === 'o') {
                    formatted += '<span class="rtile rtile-coin" title="Coin">●</span>';
                } else if (ch === 'g' || ch === 'E') {
                    formatted += '<span class="rtile rtile-goomba" title="Goomba">g</span>';
                } else if (ch === 'k' || ch === 'r') {
                    formatted += '<span class="rtile rtile-koopa" title="Koopa">' + ch + '</span>';
                } else if (ch === 'K' || ch === 'R') {
                    formatted += '<span class="rtile rtile-flying-koopa" title="Flying Koopa">' + ch + '</span>';
                } else if (ch === 'y' || ch === 'Y') {
                    formatted += '<span class="rtile rtile-spiky" title="Spiky">' + ch + '</span>';
                } else if (ch === 't' || ch === 'L' || ch === 'J' || ch === '[' || ch === ']' || ch === '<' || ch === '>') {
                    formatted += '<span class="rtile rtile-pipe" title="Pipe">' + ch + '</span>';
                } else if (ch === 'T') {
                    formatted += '<span class="rtile rtile-piranha" title="Piranha Pipe">T</span>';
                } else if (ch === 'B' || ch === 'b') {
                    formatted += '<span class="rtile rtile-cannon" title="Bullet Cannon">' + ch + '</span>';
                } else if (ch === '|' || ch === 'F') {
                    formatted += '<span class="rtile rtile-flag" title="Flagpole">' + ch + '</span>';
                } else if (ch === '-') {
                    formatted += '<span class="rtile rtile-sky">-</span>';
                } else {
                    formatted += ch;
                }
            }
            return formatted;
        }

        // LOG TO RETRO TERMINAL
        function logRetro(msg, cls = '') {
            const term = document.getElementById('retroTerminalLog');
            if (!term) return;
            const time = new Date().toTimeString().split(' ')[0];
            const p = document.createElement('div');
            if (cls) p.className = cls;
            p.innerHTML = `&gt; [${time}] ${msg}`;
            term.appendChild(p);
            term.scrollTop = term.scrollHeight;
        }

        // GENERATE CAMPAIGN VIA SSE STREAM
        async function generateRetroCampaign() {
            const overlay = document.getElementById('retroModalOverlay');
            const pBar = document.getElementById('retroProgressBar');
            const pTxt = document.getElementById('retroProgressText');
            if (overlay) overlay.style.display = 'flex';
            if (pBar) pBar.style.width = '0%';
            if (pTxt) pTxt.innerText = "INITIALIZING 2ND-ORDER MARKOV SAMPLER...";

            logRetro("Starting PCG campaign generation pipeline...", "cyan");

            // Reset Arcade state
            playerArcadeState.lastDdaDelta = {};
            playerArcadeState.levelTargets = retroCurve.map(v => v / 100.0);
            playerArcadeState.levelTexts = {};
            playerArcadeState.activeLevelIdx = 1;
            playerArcadeState.maxUnlockedLevel = 1;
            playerArcadeState.isRetryMap = {};
            document.getElementById('hudDDAShift').innerText = "+0.0%";

            const skill = document.getElementById('retroSkillSelect').value;

            try {
                const resp = await fetch('/api/generate-sequence-stream', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ curve: retroCurve, player_skill: skill, max_variance: 0.10 })
                });

                const reader = resp.body.getReader();
                const decoder = new TextDecoder();
                let buffer = '';

                while (true) {
                    const { done, value } = await reader.read();
                    if (done) break;

                    buffer += decoder.decode(value, { stream: true });
                    const lines = buffer.split('\n\n');
                    buffer = lines.pop();

                    for (const line of lines) {
                        if (line.startsWith('data: ')) {
                            try {
                                const evt = JSON.parse(line.slice(6));
                                if (evt.type === 'progress') {
                                    if (pTxt) pTxt.innerText = evt.message.toUpperCase();
                                } else if (evt.type === 'level_complete') {
                                    if (pTxt) pTxt.innerText = evt.message.toUpperCase();
                                    const pct = Math.round((evt.level / (evt.total || numLevels)) * 100);
                                    if (pBar) pBar.style.width = pct + '%';
                                    logRetro(`Stage ${evt.level} Validated (Est. Diff: ${(evt.step.estimated_difficulty * 100).toFixed(0)}%)`);
                                    if (evt.step && evt.step.level_text) {
                                        playerArcadeState.levelTexts[evt.level] = evt.step.level_text;
                                    }
                                } else if (evt.type === 'complete') {
                                    campaignData = evt.result.data;
                                    if (campaignData && campaignData.history) {
                                        campaignData.history.forEach(h => {
                                            playerArcadeState.levelTexts[h.level] = h.level_text;
                                            playerArcadeState.levelTargets[h.level - 1] = h.target_difficulty;
                                        });
                                    }
                                    logRetro("★ CAMPAIGN GENERATION COMPLETE & VERIFIED ★", "cyan");
                                    setTimeout(() => {
                                        if (overlay) overlay.style.display = 'none';
                                        renderRetroDashboard();
                                        saveRetroSharedSessionState();
                                    }, 400);
                                }
                            } catch (e) {
                                console.error("Parse error on chunk:", e);
                            }
                        }
                    }
                }
            } catch (err) {
                if (overlay) overlay.style.display = 'none';
                logRetro("ERROR GENERATING CAMPAIGN: " + err, "err");
            }
        }

        // RENDER DASHBOARD & TABS
        function renderRetroDashboard() {
            if (!campaignData || !campaignData.history || campaignData.history.length === 0) return;

            document.getElementById('monitorStatusBadge').innerText = 'ACTIVE';
            document.getElementById('monitorStatusBadge').style.background = 'var(--neon-green)';
            document.getElementById('btnDeathToggle').disabled = false;
            document.getElementById('btnAiWatch').disabled = false;
            document.getElementById('btnPlayStart').disabled = playerArcadeState.lives <= 0;

            const tabsContainer = document.getElementById('retroLevelTabs');
            tabsContainer.innerHTML = '';

            campaignData.history.forEach((step, idx) => {
                const btn = document.createElement('button');
                const lvlNum = step.level;
                const isUnlocked = lvlNum <= playerArcadeState.maxUnlockedLevel;
                const isCleared = lvlNum < playerArcadeState.maxUnlockedLevel;
                const isActive = idx === selectedLevelIdx;

                btn.className = `retro-tab-btn ${isActive ? 'active' : ''} ${!isUnlocked ? 'locked' : ''}`;
                btn.innerText = `[STAGE ${lvlNum}] ${isCleared ? '✔' : (isUnlocked ? '🎮' : '🔒')}`;
                btn.disabled = !isUnlocked;

                btn.onclick = () => {
                    selectedLevelIdx = idx;
                    playerArcadeState.activeLevelIdx = lvlNum;
                    renderRetroLevelView();
                    updateRetroHUD();
                    document.querySelectorAll('.retro-tab-btn').forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    saveRetroSharedSessionState();
                };

                tabsContainer.appendChild(btn);
            });

            renderRetroLevelView();
            updateRetroHUD();
        }

        function renderRetroLevelView() {
            if (!campaignData || !campaignData.history || !campaignData.history[selectedLevelIdx]) return;
            const step = campaignData.history[selectedLevelIdx];
            const tileGrid = document.getElementById('tileGrid');
            if (tileGrid && step.level_text) {
                tileGrid.innerHTML = formatRetroTiles(step.level_text);
            }

            if (showDeathZone) {
                fetchRetroDeathZoneTelemetry();
            } else {
                const canvas = document.getElementById('heatmapCanvas');
                if (canvas) {
                    const ctx = canvas.getContext('2d');
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                }
            }
        }

        function updateRetroHUD() {
            const idx = playerArcadeState.activeLevelIdx;
            document.getElementById('hudLevel').innerText = `1-${idx}`;
            
            // Hearts
            let hearts = "";
            for (let i = 0; i < Math.max(0, playerArcadeState.lives); i++) hearts += "❤️";
            if (playerArcadeState.lives <= 0) hearts = "💀 0 LIVES";
            document.getElementById('hudLives').innerText = hearts;

            document.getElementById('hudCoins').innerText = `🪙 ${playerArcadeState.coins.toString().padStart(2, '0')}`;
            
            const powerNames = {0: "SMALL", 1: "SUPER", 2: "FIRE"};
            document.getElementById('hudPower').innerText = powerNames[playerArcadeState.marioMode] || "SMALL";

            const delta = playerArcadeState.lastDdaDelta[idx] || "+0.0%";
            document.getElementById('hudDDAShift').innerText = delta;

            const btnPlay = document.getElementById('btnPlayStart');
            if (btnPlay) {
                btnPlay.innerText = `▶ PRESS START: PLAY WORLD 1-${idx}`;
                btnPlay.disabled = playerArcadeState.lives <= 0;
            }
        }

        // DEATH ZONE OVERLAY
        function toggleRetroDeathZone() {
            showDeathZone = !showDeathZone;
            const btn = document.getElementById('btnDeathToggle');
            if (showDeathZone) {
                btn.style.background = '#fff';
                btn.style.color = '#000';
                fetchRetroDeathZoneTelemetry();
            } else {
                btn.style.background = 'var(--neon-magenta)';
                btn.style.color = '#fff';
                const canvas = document.getElementById('heatmapCanvas');
                if (canvas) {
                    const ctx = canvas.getContext('2d');
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                }
            }
            saveRetroSharedSessionState();
        }

        async function fetchRetroDeathZoneTelemetry() {
            if (!campaignData || !campaignData.history || !campaignData.history[selectedLevelIdx]) return;
            const currentLevelId = campaignData.history[selectedLevelIdx].level;

            try {
                const resp = await fetch(`/api/telemetry/death-zone/${currentLevelId}`);
                const res = await resp.json();
                if (res.status === 'Success') {
                    renderRetroDeathCanvas(res.death_coordinates || []);
                }
            } catch (err) {
                console.error("Failed to fetch death zone telemetry:", err);
            }
        }

        function renderRetroDeathCanvas(points) {
            const canvas = document.getElementById('heatmapCanvas');
            const tileGrid = document.getElementById('tileGrid');
            if (!canvas || !tileGrid) return;

            if (!campaignData || !campaignData.history || !campaignData.history[selectedLevelIdx]) return;
            const step = campaignData.history[selectedLevelIdx];

            const gridW = tileGrid.scrollWidth || tileGrid.offsetWidth || 800;
            const gridH = tileGrid.scrollHeight || tileGrid.offsetHeight || 250;

            canvas.width = gridW;
            canvas.height = gridH;
            canvas.style.width = gridW + 'px';
            canvas.style.height = gridH + 'px';

            const ctx = canvas.getContext('2d');
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            if (!points || points.length === 0) return;

            const lines = (step.level_text || "").trim().split('\n');
            const firstLine = lines[0] ? lines[0].replace('\r', '') : "";
            const numCols = firstLine.length || 220;
            const numRows = lines.length || 16;

            const charW = gridW / numCols;
            const charH = gridH / numRows;

            points.forEach(pt => {
                const px = (pt.x + 0.5) * charW;
                const py = (pt.y + 0.5) * charH;

                // 8-bit Neon Red Target Reticle
                ctx.strokeStyle = '#ff3131';
                ctx.lineWidth = 3;
                ctx.beginPath();
                ctx.arc(px, py, 16, 0, Math.PI * 2);
                ctx.stroke();

                ctx.fillStyle = '#ffffff';
                ctx.font = 'bold 12px monospace';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText('💀', px, py);
            });
        }

        // WATCH AI PLAY
        async function watchRetroAiPlay() {
            if (!campaignData || !campaignData.history || !campaignData.history[selectedLevelIdx]) return;
            const step = campaignData.history[selectedLevelIdx];
            logRetro(`Launching Robin Baumgarten A* visualizer for Stage ${step.level}...`, "cyan");

            try {
                const resp = await fetch('/api/watch-ai-play', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        level_index: step.level,
                        target_difficulty: step.target_difficulty,
                        level_text: step.level_text
                    })
                });
                const res = await resp.json();
                if (res.status === 'Success') {
                    logRetro(`AI window active for Stage ${step.level}. Watch solving trajectory live!`);
                } else {
                    logRetro(`AI Playback Error: ${res.message}`, "err");
                }
            } catch (err) {
                logRetro(`Failed to launch AI playback: ${err}`, "err");
            }
        }

        // LAUNCH HUMAN PLAY
        async function launchRetroHumanPlay() {
            if (!campaignData || !campaignData.history || campaignData.history.length === 0) {
                alert("CANNOT PLAY: Please insert coin and generate campaign stages first!");
                return;
            }

            if (playerArcadeState.lives <= 0) {
                alert("GAME OVER: 0 Lives remaining! Click 'RESET ARCADE PROGRESSION' to restore credits.");
                return;
            }

            const currentIdx = playerArcadeState.activeLevelIdx;
            const targetDiff = playerArcadeState.levelTargets[currentIdx - 1] || 0.5;
            const nextDesignerTarget = playerArcadeState.levelTargets[currentIdx] || targetDiff;
            const isRetry = playerArcadeState.isRetryMap[currentIdx] || false;
            const prevText = playerArcadeState.levelTexts[currentIdx] || (campaignData.history[currentIdx - 1] ? campaignData.history[currentIdx - 1].level_text : null);

            logRetro(`Launching interactive Java window for Stage 1-${currentIdx} (Lives: ${playerArcadeState.lives})...`, "cyan");

            try {
                const resp = await fetch('/api/play-human-level', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        level_index: currentIdx,
                        target_difficulty: targetDiff,
                        lives: playerArcadeState.lives,
                        coins: playerArcadeState.coins,
                        mario_mode: playerArcadeState.marioMode,
                        is_retry: isRetry,
                        prev_level_text: prevText,
                        level_text: prevText
                    })
                });

                const res = await resp.json();
                if (res.status === 'Success') {
                    logRetro(`Playing Stage 1-${currentIdx} in Java Window... Complete level or lose life to trigger DDA!`);
                    pollRetroSessionResult(currentIdx, nextDesignerTarget);
                } else {
                    logRetro(`Error launching stage: ${res.message}`, "err");
                }
            } catch (err) {
                logRetro(`Launch error: ${err}`, "err");
            }
        }

        function pollRetroSessionResult(currentIdx, nextDesignerTarget) {
            if (browserGameLoopId) clearInterval(browserGameLoopId);

            let pollAttempts = 0;
            browserGameLoopId = setInterval(async () => {
                pollAttempts++;
                if (pollAttempts > 300) {
                    clearInterval(browserGameLoopId);
                    logRetro("Session polling timed out.", "warn");
                    return;
                }

                try {
                    const currentDesignerTarget = playerArcadeState.levelTargets[currentIdx - 1] || 0.5;
                    const prevText = playerArcadeState.levelTexts[currentIdx] || (campaignData && campaignData.history && campaignData.history[currentIdx - 1] ? campaignData.history[currentIdx - 1].level_text : null);
                    const resp = await fetch('/api/check-session-result', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            level_index: currentIdx,
                            next_designer_target: nextDesignerTarget,
                            current_designer_target: currentDesignerTarget,
                            current_level_text: prevText
                        })
                    });

                    const res = await resp.json();

                    if (res.status === 'Success') {
                        clearInterval(browserGameLoopId);

                        const sess = res.session_update;
                        const dda = res.dda_adjustment;

                        const finalLives = Math.max(0, sess.lives);
                        playerArcadeState.lives = finalLives;
                        playerArcadeState.coins = sess.coins;
                        playerArcadeState.marioMode = sess.mario_mode;

                        const maxLevels = numLevels || 5;

                        if (sess.won) {
                            playerArcadeState.isRetryMap[currentIdx] = false;
                            logRetro(`★ STAGE 1-${currentIdx} CLEARED! ★ (Kills: ${sess.kills}/${sess.total_enemies})`, "cyan");

                            if (currentIdx < maxLevels) {
                                const nextLvlNum = currentIdx + 1;
                                const nextZeroIdx = currentIdx;

                                playerArcadeState.maxUnlockedLevel = Math.max(playerArcadeState.maxUnlockedLevel, nextLvlNum);
                                playerArcadeState.activeLevelIdx = nextLvlNum;
                                selectedLevelIdx = nextZeroIdx;

                                if (dda && dda.adjusted_target !== undefined) {
                                    playerArcadeState.levelTargets[nextZeroIdx] = dda.adjusted_target;
                                    playerArcadeState.lastDdaDelta[nextLvlNum] = dda.delta_pct;
                                }
                                if (res.next_level && res.next_level.level_text) {
                                    playerArcadeState.levelTexts[nextLvlNum] = res.next_level.level_text;
                                }

                                if (campaignData && campaignData.history && campaignData.history[nextZeroIdx]) {
                                    const nextStep = campaignData.history[nextZeroIdx];
                                    if (dda && dda.adjusted_target !== undefined) {
                                        nextStep.target_difficulty = dda.adjusted_target;
                                        nextStep.dda_result = dda;
                                    }
                                    if (res.next_level) {
                                        nextStep.estimated_difficulty = res.next_level.estimated_difficulty;
                                        nextStep.level_text = res.next_level.level_text;
                                    }
                                }
                                logRetro(`STAGE 1-${nextLvlNum} UNLOCKED! Pre-adjusted Target: ${(dda.adjusted_target * 100).toFixed(0)}% [${dda.delta_pct} DDA Shift]`, "cyan");
                            } else {
                                logRetro(`🏆 CAMPAIGN COMPLETE! YOU CONQUERED ALL STAGES!`, "cyan");
                            }
                        } else {
                            playerArcadeState.isRetryMap[currentIdx] = true;
                            playerArcadeState.activeLevelIdx = currentIdx;
                            selectedLevelIdx = currentIdx - 1;

                            playerArcadeState.levelTargets[currentIdx - 1] = dda.adjusted_target;
                            playerArcadeState.lastDdaDelta[currentIdx] = dda.delta_pct;
                            if (res.next_level && res.next_level.level_text) {
                                playerArcadeState.levelTexts[currentIdx] = res.next_level.level_text;
                            }

                            if (campaignData && campaignData.history && campaignData.history[currentIdx - 1]) {
                                const step = campaignData.history[currentIdx - 1];
                                step.target_difficulty = dda.adjusted_target;
                                step.dda_result = dda;
                                if (res.next_level && res.next_level.level_text) {
                                    step.level_text = res.next_level.level_text;
                                    step.estimated_difficulty = res.next_level.estimated_difficulty;
                                }
                            }

                            if (finalLives <= 0) {
                                logRetro(`💀 GAME OVER! 0 Lives Remaining. Session halted. Reset credits to play again.`, "err");
                            } else {
                                logRetro(`☠ MARIO DIED (${finalLives} Lives Left). Stage 1-${currentIdx} difficulty adapted by DDA (${dda.delta_pct}) for retry.`, "warn");
                            }
                        }

                        renderRetroDashboard();
                        updateRetroHUD();
                        saveRetroSharedSessionState();
                    }
                } catch (err) {
                    console.error("Polling error:", err);
                }
            }, 1000);
        }

        function resetRetroArcade() {
            playerArcadeState.lives = 3;
            playerArcadeState.coins = 0;
            playerArcadeState.marioMode = 0;
            playerArcadeState.activeLevelIdx = 1;
            playerArcadeState.maxUnlockedLevel = 1;
            playerArcadeState.isRetryMap = {};
            selectedLevelIdx = 0;

            renderRetroDashboard();
            updateRetroHUD();
            saveRetroSharedSessionState();
            logRetro("Arcade credits reset! 3 lives restored. Unlocked stage maps preserved.", "cyan");
            alert("Arcade Credits Reset! 3 Lives restored.");
        }

        // --- SHARED SESSION STATE PERSISTENCE ---
        function getFullRetroSessionState() {
            const viewCont = document.querySelector('.retro-level-view-container');

            return {
                numLevels: numLevels,
                curve: [...retroCurve],
                campaignData: campaignData,
                playerArcadeState: playerArcadeState,
                selectedLevelIdx: selectedLevelIdx,
                isDeathZoneVisible: showDeathZone,
                scrollLeft: viewCont ? viewCont.scrollLeft : 0,
                retroTerminalHTML: document.getElementById('retroTerminalLog') ? document.getElementById('retroTerminalLog').innerHTML : '',
                timestamp: Date.now()
            };
        }

        function saveRetroSharedSessionState() {
            try {
                if (typeof sessionStorage === 'undefined') return;
                const state = getFullRetroSessionState();
                sessionStorage.setItem('mario_pcg_shared_state', JSON.stringify(state));
            } catch (e) {
                console.warn("Could not save shared state in Retro UI:", e);
            }
        }

        function loadRetroSharedSessionState() {
            try {
                if (typeof sessionStorage === 'undefined') return false;
                const raw = sessionStorage.getItem('mario_pcg_shared_state');
                if (!raw) return false;
                const state = JSON.parse(raw);
                if (!state) return false;

                if (typeof state.numLevels === 'number' && state.numLevels >= 3 && state.numLevels <= 10) {
                    numLevels = state.numLevels;
                    const sel = document.getElementById('retroNumLevels');
                    if (sel) sel.value = numLevels.toString();
                }

                if (Array.isArray(state.curve) && state.curve.length > 0) {
                    retroCurve = state.curve.map(v => Math.round(v > 1 ? v : v * 100)).slice(0, numLevels);
                    while (retroCurve.length < numLevels) {
                        const prev = retroCurve[retroCurve.length - 1] || 50;
                        retroCurve.push(Math.min(95, prev + 10));
                    }
                    renderEqualizer();
                }

                if (state.playerArcadeState) {
                    playerArcadeState = Object.assign(playerArcadeState, state.playerArcadeState);
                }

                if (state.campaignData && state.campaignData.history && state.campaignData.history.length > 0) {
                    campaignData = state.campaignData;
                    selectedLevelIdx = (typeof state.selectedLevelIdx === 'number' && state.selectedLevelIdx < campaignData.history.length)
                        ? state.selectedLevelIdx
                        : Math.max(0, playerArcadeState.activeLevelIdx - 1);

                    renderRetroDashboard();
                    logRetro("★ RESTORED CAMPAIGN SEQUENCE & DDA TELEMETRY ★", "cyan");
                } else {
                    renderEqualizer();
                    updateRetroHUD();
                }

                if (state.isDeathZoneVisible) {
                    showDeathZone = true;
                    const btn = document.getElementById('btnDeathToggle');
                    if (btn) {
                        btn.style.background = '#fff';
                        btn.style.color = '#000';
                    }
                    fetchRetroDeathZoneTelemetry();
                }

                if (state.retroTerminalHTML && document.getElementById('retroTerminalLog')) {
                    document.getElementById('retroTerminalLog').innerHTML = state.retroTerminalHTML;
                }

                if (typeof state.scrollLeft === 'number' && document.querySelector('.retro-level-view-container')) {
                    setTimeout(() => {
                        const cont = document.querySelector('.retro-level-view-container');
                        if (cont) cont.scrollLeft = state.scrollLeft;
                    }, 50);
                }

                return true;
            } catch (e) {
                console.error("Failed to load shared session state in Retro UI:", e);
                return false;
            }
        }

        function pullRetroLever() {
            const lever = document.getElementById('arcadeGamingLever');
            if (lever) lever.classList.add('pulled');

            const indRetro = document.getElementById('indRetro');
            const indModern = document.getElementById('indModern');
            if (indRetro) indRetro.classList.remove('active');
            if (indModern) indModern.classList.add('active');

            logRetro("LEVER PULLED: ENGAGING MODERN GLASS INTERFACE...", "cyan");
            saveRetroSharedSessionState();
            if (typeof sessionStorage !== 'undefined') {
                sessionStorage.setItem('mario_nav_transitioning', 'modern');
            }

            const overlay = document.getElementById('retroTransitionOverlay');
            if (overlay) {
                overlay.classList.add('active');
                overlay.classList.add('crt-collapse');
            }

            setTimeout(() => {
                window.location.href = '/';
            }, 350);
        }

        window.onload = function() {
            if (typeof sessionStorage !== 'undefined' && sessionStorage.getItem('mario_nav_transitioning')) {
                document.body.classList.add('retro-fade-in');
                sessionStorage.removeItem('mario_nav_transitioning');
            }

            const restored = loadRetroSharedSessionState();
            if (!restored) {
                renderEqualizer();
                updateRetroHUD();
            }
        };
    

const rawText = "----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n-------------------------------------------------------------------------------------------------------------------------------------------------------XXX------------------------------------------------------------------\n---------------------------------------------------------------------------------------------------------------------------------------------SSSSSSSSS-----SSSSSSSSSSSSSSS--------------------------------X-----------------\n-----------------------------------------------------------------------------------------XX----------------------------------------------------------------SSSSSSSSSSSSS---------------------------------XX-----------------\n-----------------ooo---------------------------------------------------------------------XX----------------------------------------------------------------SSSSSSSSSSSSS--------------------------------XXX-----------------\n-----------------XXX----------------R-------------------------XX-----SSSS----------------XX-------------------------SSS------------------------------------SSSSSSSSSSSSS-------------------------------XXXX-----------------\n-------------------------------------------------------------XXX-------------------------XX----------------------------------------------------------------S----------1-------------------------------XXXXX---------XXXXX---\n------------------------------------------------------------XXXX-------------------------XX---------2----XX---------------1-------------2-------------K----S----------------oo-----------------------XXXXXX---------XXXXX---\n----------------------------?-------------------Koo--------XXXXX----------------------o--XX-------------XXX------------------o-------------------------------ooooooo---------------oo---------------XXXXXXX---------XX-XX---\n----------------------------------------------------------XXXXXX-----SSSS----------------XX-------------XXX-------XX----------------------------------------??SSSSSS----XXX------------------------XXXXXXXX---F-----XX-XX---\n-------------XXX?------------------------------B---------XXXXXXX-------------------------XX-----------XXXXX---k--XXX---------------------------------XX----------------XXXX------------------------XXXXXXXXXXXXXXXXXXXXXXXXX\n-----------------------------------------------b-----tT-XXXXXXXX-------------------B-----XX----------XXXXXX-----XXXXX-------------------------------XXXXXX------------XXXXX------------------------XXXXXXXXXXXXXXXXXXXXXXXXX\n----X------------------------------------------b-----ttXXXXXXXXX-------------------b-----XX-------------XXX----XXXXXX-----------------------------XXXXX---------kk---XXXXXX------------XX----------XXXXXXXXXXXXXXXXXXXXXXXXX\nXXXXXXXXXXXX----XXXX-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX--XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX-----XXXXXXXXXXXXXXX---XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX";
const rendered = formatRetroTiles(rawText);

// Verify no raw string corruptions like 'tile-S">S' or 'tile-X">X'
if (rendered.includes('tile-S">S') || rendered.includes('tile-X">X') || rendered.includes('tile-Q">Q')) {
    console.error('[FAIL] Corrupted tile text detected!');
    process.exit(1);
}

// Verify standard span elements are present
if (!rendered.includes('<span class="rtile rtile-ground"') && !rendered.includes('<span class="rtile rtile-solid"')) {
    console.error('[FAIL] No tile spans generated!');
    process.exit(1);
}

console.log('[PASS] Rendered output is 100% clean HTML with valid span elements!');
console.log('Sample output snippet:', rendered.slice(0, 150));
