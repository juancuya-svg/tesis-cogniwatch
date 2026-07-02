from datetime import date, datetime
from pydantic import BaseModel, Field


class PatientCreate(BaseModel):
    full_name: str
    email: str
    password: str
    date_of_birth: date | None = None
    sex_at_birth: str | None = None
    monitoring_reason: str | None = None
    autonomy_level: str | None = None


class BaselineAssessmentIn(BaseModel):
    perceived_memory: int | None = Field(default=None, ge=0, le=4)
    perceived_attention: int | None = Field(default=None, ge=0, le=4)
    sleep_hours: float | None = Field(default=None, ge=0, le=24)
    activity_days: int | None = Field(default=None, ge=0, le=7)
    autonomy_score: int | None = Field(default=None, ge=0, le=10)
    self_report_score: float | None = None
    assessment_payload: dict = Field(default_factory=dict)


class WearableDailySummaryIn(BaseModel):
    summary_date: date
    total_sleep_minutes: float | None = None
    sleep_efficiency: float | None = None
    awakenings: int | None = None
    steps: int | None = None
    sedentary_minutes: int | None = None
    active_minutes: int | None = None
    avg_heart_rate: float | None = None
    resting_heart_rate: float | None = None
    hrv: float | None = None
    spo2: float | None = None
    respiratory_rate: float | None = None
    wear_adherence: float | None = None
    data_source: str = "health_connect"
    raw_payload: dict | None = None


class CognitiveMotorSessionIn(BaseModel):
    session_type: str = "finger_trace"
    total_time_ms: int | None = None
    mean_speed: float | None = None
    mean_jerk: float | None = None
    air_time_ratio: float | None = None
    pressure_mean: float | None = None
    feature_payload: dict = Field(default_factory=dict)


class AlertOut(BaseModel):
    id: int
    alert_type: str
    severity: str
    status: str
    title: str
    explanation: str
    recommendation: str | None
    score: float | None
    created_at: datetime

    class Config:
        from_attributes = True
