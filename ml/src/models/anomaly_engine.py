from __future__ import annotations


def personalized_anomaly_score(today: dict, baseline: dict) -> float:
    def pct_delta(key: str, direction: str = 'both') -> float:
        current = today.get(key)
        reference = baseline.get(key)
        if current is None or reference in (None, 0):
            return 0.0
        value = (current - reference) / reference
        if direction == 'up':
            return max(0.0, value)
        if direction == 'down':
            return max(0.0, -value)
        return abs(value)

    score = (
        0.3 * pct_delta('total_sleep_minutes', 'down') +
        0.25 * pct_delta('steps', 'down') +
        0.2 * pct_delta('resting_heart_rate', 'up') +
        0.1 * pct_delta('awakenings', 'up') +
        0.15 * pct_delta('wear_adherence', 'down')
    )
    return round(min(1.0, score), 3)
