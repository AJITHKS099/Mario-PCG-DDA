import os

def calculate_difficulty(level_source):
    """
    Analyzes a text-based Mario level (file path or string) and scores its difficulty
    on a normalized continuous scale between 0.00 and 1.00.
    """
    if isinstance(level_source, str) and os.path.exists(level_source):
        with open(level_source, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
    elif isinstance(level_source, str):
        lines = [line.strip() for line in level_source.strip().splitlines() if line.strip()]
    else:
        return 0.0

    if not lines:
        return 0.0

    total_columns = max(len(lines[0]), 1)
    height = len(lines)

    enemy_weighted_score = 0.0
    gap_columns = 0
    max_gap_width = 0
    current_gap_width = 0
    powerup_count = 0

    enemy_weights = {
        'g': 1.0,  # Goomba
        'k': 1.3,  # Green Koopa
        'r': 1.6,  # Red Koopa
        'T': 1.8,  # Piranha Flower Pipe
        'y': 1.5,  # Spiky
        'G': 1.2,
        'K': 1.5
    }

    # 1. Inspect Grid Tiles
    for r, row in enumerate(lines):
        for char in row:
            if char in enemy_weights:
                enemy_weighted_score += enemy_weights[char]
            elif char in ['?', '@']:
                powerup_count += 1

    # 2. Inspect Ground Row (Pit Gaps)
    ground_row = lines[-1]
    for char in ground_row:
        if char == '-':
            gap_columns += 1
            current_gap_width += 1
            max_gap_width = max(max_gap_width, current_gap_width)
        else:
            current_gap_width = 0

    # 3. Calculate Density & Complexity Metrics
    enemy_density = enemy_weighted_score / total_columns
    gap_density = gap_columns / total_columns
    
    # 4. Formulate Heuristic Score
    base_enemy_score = enemy_density * 2.8
    base_gap_score = (gap_density * 2.6) + (max_gap_width * 0.04)
    powerup_relief = min(0.15, (powerup_count / total_columns) * 1.5)

    raw_difficulty = base_enemy_score + base_gap_score - powerup_relief

    # Cap & normalize difficulty strictly between 0.00 and 1.00
    final_score = round(min(max(raw_difficulty, 0.05), 0.98), 2)
    return final_score

if __name__ == "__main__":
    from generator import generate_mario_level
    easy_lvl = generate_mario_level(0.2)
    hard_lvl = generate_mario_level(0.8)
    print("Easy Level Estimated Diff:", calculate_difficulty(easy_lvl))
    print("Hard Level Estimated Diff:", calculate_difficulty(hard_lvl))