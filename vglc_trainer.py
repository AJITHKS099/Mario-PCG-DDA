import os
import random

VGLC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "TheVGLC", "Super Mario Bros", "Processed"))

# Explanation: Converts Video Game Level Corpus (VGLC) tile characters into Mario-AI framework compatible glyphs.
def map_vglc_symbol_to_mario_ai(symbol):
    """
    Maps VGLC text symbols to Mario-AI-Framework format:
    - '-' : Air
    - 'X' : Solid Ground / Brick Block
    - 'S' : Destructible Brick
    - '?' : Rare Powerup Question Block
    - 'Q' : Coin Question Block
    - 'E' : Enemy (Goomba)
    - '<', '>' : Pipe Top
    - '[', ']' : Pipe Trunk
    - 'o' : Coin
    """
    if symbol == '<' or symbol == '>':
        return 't'  # Pipe top tile
    elif symbol == '[' or symbol == ']':
        return 't'  # Pipe trunk tile
    elif symbol == 'E':
        return 'g'  # Default enemy to Goomba
    return symbol

# Explanation: Loads and parses all Super Mario Bros ASCII level files from the VGLC corpus directory.
def load_vglc_levels(vglc_folder=VGLC_DIR, target_height=16):
    """
    Loads and normalizes all VGLC Super Mario Bros level files.
    Returns a list of 2D grid levels (list of lists of characters).
    """
    levels = []
    if not os.path.exists(vglc_folder):
        return levels

    for fname in sorted(os.listdir(vglc_folder)):
        if fname.endswith(".txt"):
            fpath = os.path.join(vglc_folder, fname)
            with open(fpath, 'r') as f:
                lines = [line.rstrip('\r\n') for line in f.readlines() if line.strip()]
            
            if not lines:
                continue

            h = len(lines)
            w = max(len(l) for l in lines)
            
            # Normalize to fixed target_height (16)
            grid = []
            pad_top = max(0, target_height - h)
            for _ in range(pad_top):
                grid.append(['-' for _ in range(w)])
            
            for line in lines[:target_height]:
                row = []
                for c in range(w):
                    ch = line[c] if c < len(line) else '-'
                    row.append(map_vglc_symbol_to_mario_ai(ch))
                grid.append(row)
            
            levels.append(grid)

    return levels

# Explanation: Calculates hazard density score of a level slice based on pits, enemies, and obstacles.
def compute_column_hazard_score(col):
    """
    Calculates difficulty/hazard score of a single column slice.
    """
    score = 0.0
    for tile in col:
        if tile in ['g', 'k', 'r', 'E']:
            score += 1.0
        elif tile in ['T', 't']:
            score += 0.4
        elif tile in ['?', '@']:
            score -= 0.2
    
    # Pit gap hazard
    if col[-1] == '-' and col[-2] == '-':
        score += 1.5
    
    return max(0.0, score)

class VGLCMarkovModel:
    # Explanation: Executes the init routine.
    def __init__(self, vglc_folder=VGLC_DIR):
        self.levels = load_vglc_levels(vglc_folder)
        self.transitions = {}      # (col_prev2, col_prev1) -> list of next_col
        self.start_columns = []    # Safe ground starting column pairs
        self.column_hazards = {}   # col_tuple -> hazard_score
        self._train()

    # Explanation: Trains 2nd-order Markov transition probabilities from sequence of 16-high level column slices.
    def _train(self):
        for lvl in self.levels:
            if not lvl or len(lvl) < 16:
                continue
            h = len(lvl)
            w = len(lvl[0])

            # Extract column slices
            columns = []
            for c in range(w):
                col = tuple(lvl[r][c] for r in range(16))
                columns.append(col)
                if col not in self.column_hazards:
                    self.column_hazards[col] = compute_column_hazard_score(col)

            # Build 2nd-order transitions
            for i in range(len(columns) - 2):
                c1 = columns[i]
                c2 = columns[i + 1]
                c3 = columns[i + 2]
                key = (c1, c2)
                if key not in self.transitions:
                    self.transitions[key] = []
                self.transitions[key].append(c3)

                # Store starting flat ground columns
                if i < 15 and c1[-1] == 'X' and c2[-1] == 'X':
                    self.start_columns.append(key)

    # Explanation: Probabilistically samples next column slice given previous two columns and target difficulty constraint.
    def sample_next_column(self, col_prev2, col_prev1, target_difficulty=0.5):
        """
        Samples the next column slice based on 2nd-order Markov context and target difficulty.
        """
        key = (col_prev2, col_prev1)
        candidates = self.transitions.get(key, [])

        if not candidates:
            # Fallback: search 1st-order transitions or random safe column
            candidates = [c for (k1, k2), cols in self.transitions.items() if k2 == col_prev1 for c in cols]

        if not candidates:
            # Absolute fallback: standard flat ground column
            flat_col = list('-' * 12 + 'XXXX')
            return tuple(flat_col)

        # Weight candidates by target difficulty preference
        weights = []
        target_hazard = target_difficulty * 0.85
        for cand in candidates:
            hazard = self.column_hazards.get(cand, 0.0)
            diff_diff = abs(hazard - target_hazard)
            w = 1.0 / (0.05 + (diff_diff ** 2.0))
            weights.append(w)

        total_w = sum(weights)
        if total_w <= 0:
            return random.choice(candidates)
        
        norm_weights = [w / total_w for w in weights]
        return random.choices(candidates, weights=norm_weights)[0]

    # Explanation: Synthesizes full 2D level column matrix by sampling from trained Markov transition distribution.
    def generate_level_grid(self, target_difficulty=0.5, width=220, height=16, seed=None):
        """
        Generates a 2D level grid string using the trained VGLC Markov model.
        """
        if seed is not None:
            random.seed(seed)

        grid_cols = []
        
        # 1. Start with safe ground columns
        start_key = random.choice(self.start_columns) if self.start_columns else None
        if start_key:
            grid_cols.append(start_key[0])
            grid_cols.append(start_key[1])
        else:
            flat_col = tuple(list('-' * 12 + 'XXXX'))
            grid_cols.append(flat_col)
            grid_cols.append(flat_col)

        # 2. Markov Chain generation
        while len(grid_cols) < width - 25:
            c1 = grid_cols[-2]
            c2 = grid_cols[-1]
            next_col = self.sample_next_column(c1, c2, target_difficulty=target_difficulty)
            grid_cols.append(next_col)

        # 3. Add Classic Super Mario Bros End Structure (Staircase -> Jump Gap -> Flagpole -> Walkway -> Castle with Door)
        end_ground_y = 12

        # A. Ascending 8-step Pyramid Staircase
        for step in range(1, 9):
            col_list = list('-' * height)
            for y in range(end_ground_y - step, height):
                col_list[y] = 'X'
            grid_cols.append(tuple(col_list))

        # B. 3-Tile Jump Gap between Staircase Top and Flagpole (Flat ground with air above)
        for _ in range(3):
            col_list = list('-' * height)
            for y in range(end_ground_y, height):
                col_list[y] = 'X'
            grid_cols.append(tuple(col_list))

        # C. Flagpole Column (F on ground)
        flag_col = list('-' * height)
        flag_col[end_ground_y - 1] = 'F'
        for y in range(end_ground_y, height):
            flag_col[y] = 'X'
        grid_cols.append(tuple(flag_col))

        # D. Walkway to Castle (5 tiles)
        for _ in range(5):
            walk_col = list('-' * height)
            for y in range(end_ground_y, height):
                walk_col[y] = 'X'
            grid_cols.append(tuple(walk_col))

        # E. Castle Structure with Door Cutout (5 tiles wide, 5 tiles high)
        for cx in range(5):
            castle_col = list('-' * height)
            for y in range(end_ground_y - 4, height):
                if cx == 2 and y in [end_ground_y - 1, end_ground_y - 2]:
                    castle_col[y] = '-'  # Open Castle Door Entrance
                else:
                    castle_col[y] = 'X'
            grid_cols.append(tuple(castle_col))

        # Pad remaining columns to match width
        while len(grid_cols) < width:
            walk_col = list('-' * height)
            for y in range(end_ground_y, height):
                walk_col[y] = 'X'
            grid_cols.append(tuple(walk_col))

        # Reconstruct row-major level string
        rows = []
        for r in range(height):
            row_str = "".join([grid_cols[c][r] for c in range(width)])
            rows.append(row_str)

        return "\n".join(rows)

# Singleton Instance
_vglc_model = None

# Explanation: Factory function that retrieves or trains the default 2nd-order Markov transition model on VGLC levels.
def get_vglc_model():
    global _vglc_model
    if _vglc_model is None:
        _vglc_model = VGLCMarkovModel()
    return _vglc_model

if __name__ == "__main__":
    model = get_vglc_model()
    print(f"Loaded {len(model.levels)} VGLC levels.")
    print(f"Trained {len(model.transitions)} unique 2nd-order column transitions.")
    sample_lvl = model.generate_level_grid(0.5)
    print("Sample Level Generated successfully! Lines:", len(sample_lvl.splitlines()), "Width:", len(sample_lvl.splitlines()[0]))
