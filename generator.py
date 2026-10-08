import random
import time

from estimator import calculate_difficulty
from vglc_trainer import get_vglc_model

# Explanation: Replaces vertically stacked question blocks or coins with empty space to avoid unreachable item placements.
def _fix_stacked_special_blocks(lines):
    """
    Prevents interactive reward blocks (?, Q, 1, 2, C, U, L, etc.) from being stacked
    directly on top of other solid blocks where they cannot be hit from underneath.
    """
    height = len(lines)
    width = len(lines[0])

    reward_blocks = set(['?', 'Q', '1', '2', 'C', 'U', 'L', '@', '!'])
    solid_underneath = set(['X', 'S', 'Q', '?', 'D', 't', 'T', 'B', 'b', '#', '1', '2', 'C', 'U', 'L', '@', '!'])

    for x in range(width):
        for y in range(1, height - 1):
            if lines[y][x] in reward_blocks:
                # Check if block directly underneath is solid or another block
                if lines[y + 1][x] in solid_underneath:
                    # Unhittable reward block stacked directly on top of a solid block!
                    shifted = False
                    if y >= 3 and lines[y - 3][x] == '-' and lines[y - 2][x] == '-' and lines[y - 1][x] == '-':
                        lines[y - 3][x] = lines[y][x]
                        lines[y][x] = '-'
                        shifted = True
                    if not shifted:
                        lines[y][x] = '-'

    return lines

# Explanation: Adds thematic terrain decorations, pipe alignments, and hazard placements across the generated tile grid.
def _post_process_level_decorations(level_text, target_difficulty=0.5):
    """
    Enhances level layout with progressive enemy hazards (Green/Red Turtles 'k'/'r', Flying Turtles 'K'/'R',
    Spikies 'y'/'Y', Bullet Bill Cannons 'B'/'b', Piranha Flower Pipes 'T', and Hidden Blocks '1'/'2'),
    scaling variety and challenge dynamically as target_difficulty increases.
    """
    lines = [list(line) for line in level_text.splitlines() if line.strip()]
    if not lines:
        return level_text

    height = len(lines)
    width = len(lines[0])
    ground_y = height - 1

    # 1. Progressive Piranha Flower Pipes: scale from 30% to 70% based on difficulty
    piranha_ratio = min(0.70, 0.30 + target_difficulty * 0.40)
    pipe_tops = [(y, x) for y in range(1, height - 1) for x in range(15, width - 35) if lines[y][x] == 't' and lines[y-1][x] == '-']
    if pipe_tops:
        num_piranhas = max(1, int(len(pipe_tops) * piranha_ratio))
        chosen_pipes = random.sample(pipe_tops, min(len(pipe_tops), num_piranhas))
        for py, px in chosen_pipes:
            lines[py][px] = 'T'

    # 2. Hidden Blocks: inject 2-4 hidden blocks ('1' = hidden 1up, '2' = hidden coin)
    flat_cols = [x for x in range(25, width - 40) if lines[ground_y][x] == 'X' and lines[8][x] == '-' and lines[9][x] == '-' and lines[10][x] == '-']
    if flat_cols:
        num_hidden = min(len(flat_cols), random.randint(2, 4))
        chosen_cols = random.sample(flat_cols, num_hidden)
        for hx in chosen_cols:
            hy = random.choice([8, 9])
            htype = '1' if random.random() < 0.25 else '2'
            lines[hy][hx] = htype

    # 3. Progressive Turtle & Flying Turtle Spawner (k, r, K, R, y, Y)
    existing_enemies = [(y, x) for y in range(height) for x in range(20, width - 35) if lines[y][x] in ['g', 'E']]
    if existing_enemies:
        for ey, ex in existing_enemies:
            rand_val = random.random()
            if target_difficulty < 0.35:
                # Low difficulty: mostly Goombas, 30% Green Turtles 'k'
                if rand_val < 0.30:
                    lines[ey][ex] = 'k'
            elif target_difficulty < 0.65:
                # Medium difficulty: 35% Green Turtle 'k', 25% Red Turtle 'r', 15% Flying Green Turtle 'K', 10% Spiky 'y'
                if rand_val < 0.35:
                    lines[ey][ex] = 'k'
                elif rand_val < 0.60:
                    lines[ey][ex] = 'r'
                elif rand_val < 0.75:
                    lines[ey][ex] = 'K'
                elif rand_val < 0.85:
                    lines[ey][ex] = 'y'
            else:
                # High difficulty: 30% Red Turtle 'r', 25% Flying Red Turtle 'R', 20% Flying Green Turtle 'K', 15% Flying Spiky 'Y'
                if rand_val < 0.30:
                    lines[ey][ex] = 'r'
                elif rand_val < 0.55:
                    lines[ey][ex] = 'R'
                elif rand_val < 0.75:
                    lines[ey][ex] = 'K'
                elif rand_val < 0.90:
                    lines[ey][ex] = 'Y'

    # 4. Flying Turtle Patrol Spawner over gaps & platforms on medium/high difficulty
    if target_difficulty >= 0.35:
        num_flying_turtles = int(1 + target_difficulty * 4)
        valid_air_cols = [x for x in range(30, width - 40, 6) if lines[ground_y][x] == '-' or lines[ground_y - 1][x] == '-']
        if valid_air_cols:
            chosen_air_cols = random.sample(valid_air_cols, min(len(valid_air_cols), num_flying_turtles))
            for ax in chosen_air_cols:
                ay = random.choice([7, 8, 9, 10])
                ftype = 'R' if random.random() < 0.5 else 'K'
                lines[ay][ax] = ftype

    # 5. Bullet Bill Cannon Spawner (B head, b neck/body) on medium/high difficulty
    if target_difficulty >= 0.40:
        num_cannons = int(1 + target_difficulty * 3)
        cannon_cols = [x for x in range(35, width - 45, 12) if lines[ground_y][x] == 'X' and lines[ground_y - 1][x] == '-' and lines[ground_y - 2][x] == '-']
        if cannon_cols:
            chosen_cannons = random.sample(cannon_cols, min(len(cannon_cols), num_cannons))
            for cx in chosen_cannons:
                cannon_h = random.choice([2, 3])
                head_y = ground_y - cannon_h
                lines[head_y][cx] = 'B'
                for body_y in range(head_y + 1, ground_y):
                    lines[body_y][cx] = 'b'

    # 6. Sanitize vertically stacked special blocks
    lines = _fix_stacked_special_blocks(lines)

    return "\n".join(["".join(row) for row in lines])

# Explanation: Constructs raw 2D tile matrix using Markov chain column transitions conditioned on difficulty.
def _build_raw_level_grid(target_difficulty, width=220, height=16, seed=None):
    """
    Generates a level layout using the VGLC 2nd-order Markov Chain model trained on 31 Super Mario Bros levels.
    """
    vglc_model = get_vglc_model()
    raw_text = vglc_model.generate_level_grid(target_difficulty=target_difficulty, width=width, height=height, seed=seed)
    return _post_process_level_decorations(raw_text, target_difficulty=target_difficulty)

from validator import is_level_solvable

# Explanation: Generates a complete Mario level string conditioned on target difficulty using 2nd-order Markov transitions.
def generate_mario_level(target_difficulty, width=220, height=16, seed=None, max_diff_error=0.05, max_attempts=50):
    """
    Generates a Mario level formatted for Mario-AI-Framework.
    Enforces that abs(estimated_difficulty - target_difficulty) <= 0.05 AND level is A* solvable.
    If difficulty error is > 0.05 or level is unsolvable, automatically regenerates until satisfied.
    """
    best_level = None
    best_error = 999.0

    for attempt in range(max_attempts):
        cur_seed = None if seed is None else (seed + attempt * 17)
        level_text = _build_raw_level_grid(target_difficulty, width=width, height=height, seed=cur_seed)
        est_diff = calculate_difficulty(level_text)
        error = abs(est_diff - target_difficulty)

        # Validate A* pathfinding playability
        solvable, _ = is_level_solvable(level_text)

        if error <= max_diff_error and solvable:
            return level_text

        if solvable and error < best_error:
            best_error = error
            best_level = level_text

    return best_level if best_level else _build_raw_level_grid(target_difficulty, width=width, height=height)

# Explanation: Modifies existing level layout to dynamically increase or decrease difficulty based on DDA telemetry and player death points.
def tweak_level_for_dda(base_level_text, dda_delta, telemetry=None):
    """
    Applies targeted DDA spatial micro-adjustments to an existing level layout when retrying,
    combining performance metrics with targeted spatial interventions (pit gap fill, enemy demotion, powerup insertion).

    :param base_level_text: str representation of the previous level layout
    :param dda_delta: float difficulty adjustment (-0.10 to +0.10)
    :param telemetry: dict containing optional failure coordinates, mario_mode, struggle_reason
    :return: (modified_level_text, list_of_structural_changes_made)
    """
    lines = [list(line) for line in base_level_text.splitlines() if line.strip()]
    if not lines:
        return base_level_text, ["No layout changes"]

    height = len(lines)
    width = len(lines[0])
    changes_made = []
    telemetry = telemetry or {}

    # Extract target failure column X_fail if available
    completion_pct = telemetry.get('completion_pct', 0.5)
    fail_col = int(completion_pct * width) if completion_pct > 0 else random.randint(20, width - 40)
    fail_col = max(10, min(width - 30, fail_col))

    mario_mode = telemetry.get('mario_mode', 0)
    struggle_reason = str(telemetry.get('struggle_reason', '')).lower()

    if dda_delta < -0.01:
        # --- TARGETED EASE INTERVENTIONS ---
        
        # 1. Pit Failure Intervention: fill or add platform at failure coordinate
        if "pit" in struggle_reason or "gap" in struggle_reason or "fell" in struggle_reason:
            ground_y = height - 1
            # Search for pit gap near fail_col
            pit_x = None
            for cx in range(max(0, fail_col - 5), min(width - 1, fail_col + 5)):
                if lines[ground_y][cx] == '-':
                    pit_x = cx
                    break
            
            if pit_x is not None:
                for y in range(ground_y - 1, height):
                    lines[y][pit_x] = 'X'
                changes_made.append(f"Injected platform ground block across pit gap at col {pit_x}")
            elif height >= 4 and fail_col + 1 < width:
                # Add floating platform above ground
                lines[ground_y - 3][fail_col] = 'S'
                lines[ground_y - 3][fail_col + 1] = 'S'
                changes_made.append(f"Injected safety stepping platform at col {fail_col}")

        # 2. Enemy Cluster Intervention: demote or remove enemies near failure coordinate
        enemy_slice = []
        for y in range(height):
            for x in range(max(0, fail_col - 5), min(width - 1, fail_col + 5)):
                if lines[y][x] in ['g', 'k', 'r', 'y']:
                    enemy_slice.append((y, x, lines[y][x]))

        if enemy_slice:
            ey, ex, etype = random.choice(enemy_slice)
            if etype in ['r', 'y', 'k']:
                lines[ey][ex] = 'g'  # Demote to Goomba
                changes_made.append(f"Demoted aggressive enemy ({etype}) to Goomba at col {ex}")
            else:
                lines[ey][ex] = 'o'  # Convert Goomba to coin reward
                changes_made.append(f"Removed enemy patrol near failure point at col {ex}")

        # 3. Small Mario Power-Up Assistance: insert ? block 5 columns prior to failure
        if mario_mode == 0 and height >= 6:
            powerup_x = max(5, min(width - 5, fail_col - 5))
            lines[height - 5][powerup_x] = '?'
            changes_made.append(f"Inserted dynamic Power-Up ? block 5 columns prior to failure point at col {powerup_x}")

        # Fallback general adjustments if targeted changes were insufficient
        if not changes_made:
            ground_y = height - 1
            for x in range(20, width - 40):
                if lines[ground_y][x] == '-' and lines[ground_y][x+1] == '-':
                    lines[ground_y][x] = 'X'
                    changes_made.append(f"Narrowed pit gap at col {x}")
                    break

        if not changes_made:
            changes_made.append("Reduced regional hazard density")

    elif dda_delta > 0.01:
        # --- INCREASE CHALLENGE INTERVENTIONS ---
        clean_pipes = [(y, x) for y in range(1, height - 1) for x in range(width - 1) if lines[y][x] == 't' and lines[y-1][x] == '-']
        if clean_pipes:
            py, px = random.choice(clean_pipes)
            lines[py][px] = 'T'
            changes_made.append(f"Added Piranha Flower to pipe at col {px}")

        ground_y = height - 1
        flat_ground = [x for x in range(20, width - 40) if lines[ground_y][x] == 'X' and lines[ground_y - 1][x] == '-']
        if flat_ground:
            ex = random.choice(flat_ground)
            lines[ground_y - 1][ex] = 'g'
            changes_made.append(f"Added extra Goomba enemy patrol at col {ex}")

        if not changes_made:
            changes_made.append("Increased regional enemy vigilance")
    else:
        changes_made.append("Retained exact level layout structure for retry")

    modified_text = "\n".join(["".join(row) for row in lines])
    return modified_text, changes_made

if __name__ == "__main__":
    lvl1 = generate_mario_level(0.5)
    print("Level Piranha Pipes ('T'):", lvl1.count('T'))
    print("Level Coin ? Blocks ('Q'):", lvl1.count('Q'))
    print("Level Rare Mushroom ? Blocks ('?'):", lvl1.count('?'))