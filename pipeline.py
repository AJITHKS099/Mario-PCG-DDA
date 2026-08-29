"""
Pipeline coordinator for Mario PCG sequence generation, DDA processing, and level validation.
"""
from generator import generate_mario_level
from estimator import calculate_difficulty
from dda import DynamicDifficultyAdjuster
from game_session import MarioCampaignSession

def run_pipeline_sequence(curve, dda_variance=0.10, player_skill="average"):
    """
    Executes a complete PCG + DDA pipeline run for a given difficulty curve.
    """
    session = MarioCampaignSession(dda_max_variance=dda_variance)
    history = session.run_campaign_simulation(curve, player_skill=player_skill)
    
    return {
        "curve": curve,
        "history": history,
        "summary": {
            "total_levels": len(curve),
            "player_skill": player_skill,
            "max_variance": dda_variance,
            "designer_curve": curve,
            "dda_adjusted_curve": [h["target_difficulty"] for h in history],
            "actual_estimated_curve": [h["estimated_difficulty"] for h in history]
        }
    }

def generate_single_level_pipeline(target_difficulty):
    """Generates a single level and estimates its difficulty."""
    level_text = generate_mario_level(target_difficulty)
    est_diff = calculate_difficulty(level_text)
    return {
        "target_difficulty": target_difficulty,
        "estimated_difficulty": est_diff,
        "level_text": level_text
    }

if __name__ == "__main__":
    res = run_pipeline_sequence([0.3, 0.5, 0.7, 0.4])
    print("Pipeline Test Summary:", res["summary"])