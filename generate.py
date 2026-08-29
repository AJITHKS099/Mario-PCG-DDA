import os
import json
import random

def create_safe_start(height=14, width=15):
    """Generates 15 vertical columns of safe flat ground."""
    cols = []
    for _ in range(width):
        col = []
        for r in range(height):
            if r >= height - 2:
                col.append("X")
            else:
                col.append("-")
        cols.append("".join(col))
    return cols

def create_stair_ending(height=14):
    """Generates staircase + flagpole landing columns."""
    stair_cols = []
    # 8 columns of ascending stairs
    for step in range(1, 9):
        col = []
        for r in range(height):
            if r >= height - step:
                col.append("X")
            else:
                col.append("-")
        stair_cols.append("".join(col))
    
    # 10 flat ground ending columns
    for _ in range(10):
        col = []
        for r in range(height):
            if r >= height - 2:
                col.append("X")
            else:
                col.append("-")
        stair_cols.append("".join(col))
        
    return stair_cols

def fix_pipe_structures(grid):
    """Ensures pipe tops always sit seamlessly on pipe bodies down to ground."""
    height = len(grid)
    width = len(grid[0])

    for col in range(width):
        for row in range(height - 1):
            char = grid[row][col]
            if char == 'L':
                for sub_row in range(row + 1, height):
                    if grid[sub_row][col] in ['X', 'S', '?']:
                        break
                    grid[sub_row] = grid[sub_row][:col] + '[' + grid[sub_row][col+1:]
            elif char == 'J':
                for sub_row in range(row + 1, height):
                    if grid[sub_row][col] in ['X', 'S', '?']:
                        break
                    grid[sub_row] = grid[sub_row][:col] + ']' + grid[sub_row][col+1:]
    return grid

def generate_mario_level(model_file="mario_model.json", output_file="levels/generated_level.txt", target_length=200):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(model_file, "r") as f:
        model = json.load(f)

    context_size = model["context_size"]
    chunk_width = model["chunk_width"]
    transitions = model["transitions"]

    contexts = list(transitions.keys())
    current_context_str = random.choice(contexts)
    
    # Store initial chunks
    generated_chunks = current_context_str.split("||")

    # Generate middle level content using Chunk transitions
    num_chunks_needed = max(1, (target_length // chunk_width) - 10)
    for _ in range(num_chunks_needed):
        context_key = "||".join(generated_chunks[-context_size:])

        if context_key in transitions:
            choices = list(transitions[context_key].keys())
            weights = list(transitions[context_key].values())
            next_chunk = random.choices(choices, weights=weights)[0]
        else:
            fallback_key = random.choice(contexts)
            next_chunk = random.choice(list(transitions[fallback_key].keys()))

        generated_chunks.append(next_chunk)

    # Deconstruct chunks back into single vertical columns
    columns = []
    for chunk in generated_chunks:
        columns.extend(chunk.split("::"))

    target_height = len(columns[0])

    # Safe Start Zone (15 columns) & Staircase Ending (18 columns)
    start_cols = create_safe_start(height=target_height, width=15)
    end_cols = create_stair_ending(height=target_height)

    # Combine full column sequence
    full_columns = start_cols + columns + end_cols
    total_len = len(full_columns)

    # Convert vertical columns into horizontal rows
    raw_rows = ["".join([full_columns[col][row] for col in range(total_len)]) for row in range(target_height)]
    
    # Apply pipe repairs
    repaired_rows = fix_pipe_structures(raw_rows)

    with open(output_file, "w") as f:
        f.write("\n".join(repaired_rows))

    print(f"High-quality level generated successfully at '{output_file}'!")

if __name__ == "__main__":
    generate_mario_level()