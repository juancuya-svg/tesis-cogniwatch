from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class BaselineSnapshot:
    avg_sleep_minutes: float | None = None
    avg_steps: float | None = None
    avg_resting_hr: float | None = None


def build_alerts(today: dict[str, Any], baseline: BaselineSnapshot) -> list[dict[str, Any]]:
    alerts: list[dict[str, Any]] = []

    sleep = today.get("total_sleep_minutes")
    steps = today.get("steps")
    resting_hr = today.get("resting_heart_rate")
    awakenings = today.get("awakenings")
    adherence = today.get("wear_adherence")

    if baseline.avg_sleep_minutes and sleep is not None and sleep < baseline.avg_sleep_minutes * 0.7:
        severity = "high" if sleep < baseline.avg_sleep_minutes * 0.55 else "medium"
        alerts.append(
            {
                "alert_type": "sleep_drop",
                "severity": severity,
                "title": "Disminución relevante del sueño",
                "explanation": "El sueño nocturno cayó de forma importante frente a la línea base personal.",
                "recommendation": "Revisar rutina, eventos nocturnos y síntomas reportados en los últimos días.",
                "score": round((baseline.avg_sleep_minutes - sleep) / baseline.avg_sleep_minutes, 3),
            }
        )

    if baseline.avg_steps and steps is not None and steps < baseline.avg_steps * 0.6:
        alerts.append(
            {
                "alert_type": "activity_drop",
                "severity": "medium",
                "title": "Reducción de actividad diaria",
                "explanation": "La actividad del día está claramente por debajo del patrón basal del paciente.",
                "recommendation": "Confirmar si hubo reposo, malestar físico, problemas de movilidad o baja adherencia al uso.",
                "score": round((baseline.avg_steps - steps) / baseline.avg_steps, 3),
            }
        )

    if baseline.avg_resting_hr and resting_hr is not None and resting_hr > baseline.avg_resting_hr * 1.15:
        alerts.append(
            {
                "alert_type": "resting_hr_increase",
                "severity": "medium",
                "title": "Aumento de frecuencia cardiaca en reposo",
                "explanation": "La frecuencia cardiaca en reposo subió por encima del patrón basal del paciente.",
                "recommendation": "Verificar sueño, estrés, hidratación, enfermedad intercurrente o menor recuperación.",
                "score": round((resting_hr - baseline.avg_resting_hr) / baseline.avg_resting_hr, 3),
            }
        )

    if awakenings is not None and awakenings >= 6:
        alerts.append(
            {
                "alert_type": "frequent_awakenings",
                "severity": "medium",
                "title": "Despertares frecuentes",
                "explanation": "El patrón de sueño muestra múltiples despertares en la noche.",
                "recommendation": "Registrar cambios de ambiente, dolor, nocturia o inquietud conductual.",
                "score": float(awakenings),
            }
        )

    if adherence is not None and adherence < 0.4:
        alerts.append(
            {
                "alert_type": "low_adherence",
                "severity": "low",
                "title": "Baja adherencia al dispositivo",
                "explanation": "El tiempo de uso del wearable fue bajo, lo que reduce la confiabilidad del seguimiento.",
                "recommendation": "Confirmar carga, comodidad del reloj y acompañar la rutina de uso.",
                "score": round(adherence, 3),
            }
        )

    return alerts
