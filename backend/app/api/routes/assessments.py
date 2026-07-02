from fastapi import APIRouter

router = APIRouter()


@router.get('/onboarding-template')
def onboarding_template() -> dict:
    return {
        'consent': True,
        'sections': [
            'basic_profile',
            'caregiver_link',
            'monitoring_reason',
            'autonomy_level',
            'sleep_habits',
            'activity_habits',
            'memory_attention_perception',
            'functional_checklist',
            'alert_preferences',
            'wearable_pairing',
        ],
        'note': 'This assessment is a support-oriented intake, not a medical diagnosis.',
    }
