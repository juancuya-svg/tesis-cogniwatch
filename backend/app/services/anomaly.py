from __future__ import annotations

from typing import Iterable


def relative_deviation(current: float | None, baseline: float | None, direction: str = "both") -> float:
    if current is None or baseline in (None, 0):
        return 0.0
    delta = (current - baseline) / baseline
    if direction == "down":
        return max(0.0, -delta)
    if direction == "up":
        return max(0.0, delta)
    return abs(delta)


def anomaly_score(today: dict, baseline: dict) -> float:
    score = 0.0
    score += 0.30 * relative_deviation(today.get("total_sleep_minutes"), baseline.get("total_sleep_minutes"), "down")
    score += 0.25 * relative_deviation(today.get("steps"), baseline.get("steps"), "down")
    score += 0.20 * relative_deviation(today.get("resting_heart_rate"), baseline.get("resting_heart_rate"), "up")
    score += 0.10 * relative_deviation(today.get("awakenings"), baseline.get("awakenings"), "up")
    adherence = today.get("wear_adherence")
    if adherence is not None and adherence < 0.4:
        score += 0.15 * (1 - adherence)
    return round(min(1.0, score), 3)
