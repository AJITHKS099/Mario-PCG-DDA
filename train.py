import os
import json
from collections import defaultdict, Counter

def train_mario_model(dataset_folder, context_size=3, chunk_width=3):
    transitions = defaultdict(Counter)
    
    level_files = [f for f in os.listdir(dataset_folder) if f.endswith('.txt')]
    print(f"Found {len(level_files)} level files for training...")

    chunks_database = []

    for file_name in level_files:
        file_path = os.path.join(dataset_folder, file_name)
        with open(file_path, 'r') as f:
            lines = [line.rstrip('\n') for line in f.readlines() if line.strip()]

        if not lines:
            continue

        height = len(lines)
        width = min(len(line) for line in lines)

        # Slice into vertical columns
        columns = ["".join([lines[row][col] for row in range(height)]) for col in range(width)]

        # Group columns into Macro-Chunks of width `chunk_width`
        chunks = []
        for c in range(0, len(columns) - chunk_width + 1, chunk_width):
            chunk_str = "::".join(columns[c : c + chunk_width])
            chunks.append(chunk_str)
            chunks_database.append(chunk_str)

        # Learn transition probabilities between Macro-Chunks
        for i in range(len(chunks) - context_size):
            context = "||".join(chunks[i : i + context_size])
            next_chunk = chunks[i + context_size]
            transitions[context][next_chunk] += 1

    serialized_model = {
        "context_size": context_size,
        "chunk_width": chunk_width,
        "chunks": chunks_database,
        "transitions": {k: dict(v) for k, v in transitions.items()}
    }

    with open("mario_model.json", "w") as f:
        json.dump(serialized_model, f, indent=2)

    print("High-quality Chunk-based Model successfully saved to 'mario_model.json'!")

if __name__ == "__main__":
    DATASET_PATH = "./TheVGLC/Super Mario Bros/Processed"
    train_mario_model(DATASET_PATH, context_size=3, chunk_width=3)