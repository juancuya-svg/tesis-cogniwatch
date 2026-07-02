from fastapi import APIRouter

router = APIRouter()


@router.get('/supported-types')
def supported_types() -> dict:
    return {
        'health_connect': [
            'sleep_session',
            'heart_rate',
            'resting_heart_rate',
            'steps',
            'exercise_session',
            'oxygen_saturation',
            'respiratory_rate',
        ],
        'app_fallbacks': ['daily_check_in', 'manual_symptom_report', 'cognitive_motor_microtask'],
    }
