from sqlalchemy import Boolean, Column, Date, DateTime, Float, ForeignKey, Integer, JSON, String, Text, func
from sqlalchemy.orm import relationship

from app.core.db import Base


class PatientProfile(Base):
    __tablename__ = "patient_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    date_of_birth = Column(Date, nullable=True)
    sex_at_birth = Column(String(20), nullable=True)
    monitoring_reason = Column(String(120), nullable=True)
    autonomy_level = Column(String(40), nullable=True)
    baseline_tier = Column(String(40), nullable=True)
    consent_signed = Column(Boolean, nullable=False, default=False)
    wearable_connected = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CaregiverLink(Base):
    __tablename__ = "caregiver_links"

    id = Column(Integer, primary_key=True)
    caregiver_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    patient_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    relationship_label = Column(String(60), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class BaselineAssessment(Base):
    __tablename__ = "baseline_assessments"

    id = Column(Integer, primary_key=True)
    patient_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    perceived_memory = Column(Integer, nullable=True)
    perceived_attention = Column(Integer, nullable=True)
    sleep_hours = Column(Float, nullable=True)
    activity_days = Column(Integer, nullable=True)
    autonomy_score = Column(Integer, nullable=True)
    self_report_score = Column(Float, nullable=True)
    suggested_tier = Column(String(40), nullable=True)
    assessment_payload = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class WearableDailySummary(Base):
    __tablename__ = "wearable_daily_summaries"

    id = Column(Integer, primary_key=True)
    patient_user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    summary_date = Column(Date, nullable=False, index=True)
    total_sleep_minutes = Column(Float, nullable=True)
    sleep_efficiency = Column(Float, nullable=True)
    awakenings = Column(Integer, nullable=True)
    steps = Column(Integer, nullable=True)
    sedentary_minutes = Column(Integer, nullable=True)
    active_minutes = Column(Integer, nullable=True)
    avg_heart_rate = Column(Float, nullable=True)
    resting_heart_rate = Column(Float, nullable=True)
    hrv = Column(Float, nullable=True)
    spo2 = Column(Float, nullable=True)
    respiratory_rate = Column(Float, nullable=True)
    wear_adherence = Column(Float, nullable=True)
    data_source = Column(String(40), nullable=False, default="health_connect")
    raw_payload = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CognitiveMotorSession(Base):
    __tablename__ = "cognitive_motor_sessions"

    id = Column(Integer, primary_key=True)
    patient_user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    session_type = Column(String(50), nullable=False, default="finger_trace")
    total_time_ms = Column(Integer, nullable=True)
    mean_speed = Column(Float, nullable=True)
    mean_jerk = Column(Float, nullable=True)
    air_time_ratio = Column(Float, nullable=True)
    pressure_mean = Column(Float, nullable=True)
    predicted_flag_probability = Column(Float, nullable=True)
    feature_payload = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True)
    patient_user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    alert_type = Column(String(80), nullable=False)
    severity = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False, default="new")
    title = Column(String(180), nullable=False)
    explanation = Column(Text, nullable=False)
    recommendation = Column(Text, nullable=True)
    score = Column(Float, nullable=True)
    alert_payload = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    closed_at = Column(DateTime(timezone=True), nullable=True)


class CareNote(Base):
    __tablename__ = "care_notes"

    id = Column(Integer, primary_key=True)
    patient_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    author_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    note = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
