import subprocess
import os
from generate import generate_mario_level

def compile_java(mario_dir):
    bin_dir = os.path.join(mario_dir, "bin")
    os.makedirs(bin_dir, exist_ok=True)
    compile_cmd = ["javac", "-cp", "bin;bin/*;src", "-d", "bin", "src/PlayLevel.java"]
    compile_res = subprocess.run(compile_cmd, cwd=mario_dir, capture_output=True, text=True)
    if compile_res.returncode != 0:
        print("[ERROR] Java compilation failed:")
        print(compile_res.stderr)
        return False
    return True

def validate_level(mario_dir, rel_level_path):
    """Runs PlayLevel in background 'validate' mode using Robin Baumgarten AI agent."""
    val_cmd = ["java", "-cp", "bin;bin/*", "PlayLevel", rel_level_path, "validate"]
    result = subprocess.run(val_cmd, cwd=mario_dir, capture_output=True, text=True)
    return "RESULT:WIN" in result.stdout.strip()

def watch_ai_play(mario_dir, rel_level_path):
    """Runs PlayLevel in 'validate' mode with visuals enabled so you can watch the AI."""
    print("\n[AI DEMO] Watching Robin Baumgarten AI solve the level...")
    # Temporarily run in validate mode while rendering
    demo_cmd = ["java", "-cp", "bin;bin/*", "PlayLevel", rel_level_path, "validate"]
    subprocess.run(demo_cmd, cwd=mario_dir)

def main():
    mario_dir = os.path.join(os.getcwd(), "Mario-AI-Framework")
    
    print("Ensuring Java framework is compiled...")
    if not compile_java(mario_dir):
        return

    level_file = "levels/generated_level.txt"
    rel_level_path = os.path.join("..", "levels", "generated_level.txt")

    attempt = 1
    max_attempts = 10

    # 1. Validation loop
    while attempt <= max_attempts:
        print(f"\n[Attempt {attempt}/{max_attempts}] Generating level...")
        generate_mario_level(output_file=level_file)

        print("Validating playability with Robin Baumgarten A* Agent...")
        if validate_level(mario_dir, rel_level_path):
            print("✔ Playability Passed! Level is 100% beatable.")
            break
        else:
            print("✘ Playability Failed! Retrying...")
            attempt += 1

    if attempt > max_attempts:
        print("\n[Warning] Could not generate a playable level within max attempts.")
        return

    # 2. Ask if you want to watch the AI or play yourself
    print("\n" + "="*40)
    choice = input("Enter '1' to watch the AI play, or '2' to play yourself: ").strip()
    print("="*40)

    if choice == '1':
        # Re-run validation with visual playback in PlayLevel
        watch_ai_cmd = ["java", "-cp", "bin;bin/*", "PlayLevel", rel_level_path, "validate_vis"]
        subprocess.run(watch_ai_cmd, cwd=mario_dir)
    else:
        print("\nLaunching level for human player...")
        play_cmd = ["java", "-cp", "bin;bin/*", "PlayLevel", rel_level_path, "play"]
        subprocess.run(play_cmd, cwd=mario_dir)

if __name__ == "__main__":
    main()