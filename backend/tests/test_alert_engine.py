from app.services.alert_engine import BaselineSnapshot, build_alerts


def test_build_alerts_detects_sleep_drop() -> None:
    alerts = build_alerts(
        {
            'total_sleep_minutes': 200,
            'steps': 3000,
            'resting_heart_rate': 80,
            'awakenings': 7,
            'wear_adherence': 0.3,
        },
        BaselineSnapshot(avg_sleep_minutes=420, avg_steps=6000, avg_resting_hr=66),
    )
    types = {a['alert_type'] for a in alerts}
    assert 'sleep_drop' in types
    assert 'activity_drop' in types
    assert 'frequent_awakenings' in types
