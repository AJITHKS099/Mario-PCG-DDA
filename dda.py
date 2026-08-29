"""
Dynamic Difficulty Adjustment (DDA) Engine for Mario PCG.
Calculates real-time difficulty adjustments based on player performance metrics,
strictly enforcing a 10% (0.10) maximum variance bound relative to the designer's target curve.
"""

class DynamicDifficultyAdjuster:
    def __init__(self, max_variance=0.10, decay_factor=0.70):
        """
        :param max_variance: Maximum allowed delta from designer baseline (default 0.10 = 10%)
        :param decay_factor: Exponential decay weight for session history (default 0.70)
        """
        self.max_variance = max_variance
        self.decay_factor = decay_factor
        self.session_history = []

    def reset_session(self):
        """Resets cumulative session telemetry when a new campaign series is generated."""
        self.session_history = []

    def _calculate_raw_performance(self, player_performance):
        won = player_performance.get('won', True)
        lives_lost = player_performance.get('lives_lost', 0 if won else 1)
        completion_pct = player_performance.get('completion_pct', 1.0 if won else 0.5)
        time_taken = player_performance.get('time_taken', 30.0)
        target_time = player_performance.get('target_time', 45.0)
        mario_mode = player_performance.get('mario_mode', 0)

        if won:
            time_factor = (target_time - time_taken) / max(target_time, 1.0)
            time_factor = max(-0.5, min(0.5, time_factor))
            power_bonus = 0.2 if mario_mode > 0 else 0.0
            return 0.4 + (time_factor * 0.4) + power_bonus
        else:
            return -0.5 - (0.2 * lives_lost) + (completion_pct * 0.3)

    def calculate_adjustment(self, designer_target, player_performance=None, session_history=None):
        """
        Calculates the new target difficulty based on cumulative session performance across all played levels.
        """
        if player_performance is not None:
            self.session_history.append(player_performance)

        history = session_history if session_history is not None else self.session_history

        if not history:
            return {
                "designer_target": designer_target,
                "adjusted_target": designer_target,
                "delta": 0.0,
                "delta_pct": "+0.0%",
                "raw_performance": 0.0,
                "reason": "Initial level sequence. No player history recorded yet.",
                "dda_changes": ["Maintained target difficulty curve without structural shifts"]
            }

        # Calculate weighted cumulative performance score across all played levels in session
        total_weight = 0.0
        weighted_perf_sum = 0.0
        n = len(history)

        for i, perf in enumerate(history):
            raw_p = self._calculate_raw_performance(perf)
            # Exponential decay weight: recent levels have higher weight (0.7^(n-1-i))
            weight = self.decay_factor ** (n - 1 - i)
            weighted_perf_sum += raw_p * weight
            total_weight += weight

        cum_performance = weighted_perf_sum / max(total_weight, 1e-5)
        cum_performance = max(-1.0, min(1.0, cum_performance))

        delta = cum_performance * self.max_variance
        delta = max(-self.max_variance, min(self.max_variance, delta))

        min_allowed = max(0.0, designer_target - self.max_variance)
        max_allowed = min(1.0, designer_target + self.max_variance)

        adjusted_target = round(max(min_allowed, min(max_allowed, designer_target + delta)), 3)
        actual_delta = round(adjusted_target - designer_target, 3)

        if actual_delta > 0.01:
            reason = f"Cumulative session trend: strong performance across {n} level(s) (+{actual_delta*100:.1f}% difficulty shift)."
        elif actual_delta < -0.01:
            reason = f"Cumulative session trend: player struggling across {n} level(s) ({actual_delta*100:.1f}% difficulty shift)."
        else:
            reason = f"Cumulative session trend across {n} level(s) matched target expectations."

        dda_changes = []
        if actual_delta < -0.01:
            dda_changes.append(f"Reduced hazard density (Target difficulty lowered from {designer_target*100:.0f}% to {adjusted_target*100:.0f}%)")
            dda_changes.append("Narrowed maximum gap widths for safer platforming")
            dda_changes.append("Decreased enemy patrol frequency & Piranha Pipe spawns")
            dda_changes.append("Added +1 Mushroom Power-Up Question Block")
        elif actual_delta > 0.01:
            dda_changes.append(f"Increased challenge density (Target difficulty raised from {designer_target*100:.0f}% to {adjusted_target*100:.0f}%)")
            dda_changes.append("Increased Koopa & Piranha Flower Pipe frequency")
            dda_changes.append("Slightly widened platforming pit gaps")
        else:
            dda_changes.append("Maintained target difficulty curve without structural shifts")

        return {
            "designer_target": designer_target,
            "adjusted_target": adjusted_target,
            "delta": actual_delta,
            "delta_pct": f"{actual_delta * 100:+.1f}%",
            "raw_performance": round(cum_performance, 3),
            "session_levels_count": n,
            "reason": reason,
            "dda_changes": dda_changes
        }

if __name__ == "__main__":
    dda = DynamicDifficultyAdjuster(max_variance=0.10)
    print("Testing DDA Engine:")
    print("Flawless win at target 0.50:", dda.calculate_adjustment(0.50, {'won': True, 'time_taken': 20.0, 'mario_mode': 2}))
    print("Loss at target 0.50:", dda.calculate_adjustment(0.50, {'won': False, 'lives_lost': 1, 'completion_pct': 0.4}))
