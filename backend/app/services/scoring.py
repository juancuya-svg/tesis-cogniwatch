from __future__ import annotations


def support_tier_label(tier: int) -> str:
    return {
        0: "low_monitoring",
        1: "watchlist",
        2: "high_support",
    }.get(tier, "watchlist")


def combine_scores(monitoring_tier: int, anomaly_score: float, cognitive_motor_probability: float | None = None) -> dict:
    base = {0: 0.25, 1: 0.55, 2: 0.8}.get(monitoring_tier, 0.55)
    cm = 0.0 if cognitive_motor_probability is None else 0.2 * cognitive_motor_probability
    final_score = min(1.0, 0.65 * base + 0.35 * anomaly_score + cm)
    if final_score < 0.35:
        severity = "low"
    elif final_score < 0.7:
        severity = "medium"
    else:
        severity = "high"
    return {
        "monitoring_tier": support_tier_label(monitoring_tier),
        "risk_score": round(final_score, 3),
        "severity": severity,
    }
