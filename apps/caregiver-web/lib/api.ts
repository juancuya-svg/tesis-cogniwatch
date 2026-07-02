const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'

async function safeJson(url: string) {
  try {
    const response = await fetch(url, { cache: 'no-store' })
    if (!response.ok) throw new Error('Bad response')
    return await response.json()
  } catch {
    return null
  }
}

export async function getAdminSummary() {
  return (await safeJson(`${API_BASE}/api/v1/admin/summary`)) ?? {
    patients: 1,
    caregivers: 1,
    alerts_total: 1,
    signals_total: 14,
  }
}

export async function getPatients() {
  return (await safeJson(`${API_BASE}/api/v1/patients`)) ?? [
    {
      id: 3,
      full_name: 'Carlos Vega',
      email: 'patient@cogniwatch.local',
      baseline_tier: 'watchlist',
      monitoring_reason: 'memory_follow_up',
      autonomy_level: 'partial_support',
    },
  ]
}

export async function getPatientOverview(id: string) {
  return (await safeJson(`${API_BASE}/api/v1/patients/${id}/overview`)) ?? {
    patient: {
      id: Number(id),
      full_name: 'Carlos Vega',
      baseline_tier: 'watchlist',
      monitoring_reason: 'memory_follow_up',
      wearable_connected: true,
    },
    latest_signal: {
      summary_date: '2026-04-02',
      sleep: 382,
      steps: 4180,
      resting_hr: 72,
      adherence: 0.77,
    },
    latest_cognitive_motor_probability: 0.41,
    open_alerts: 1,
  }
}

export async function getAlerts() {
  return (await safeJson(`${API_BASE}/api/v1/alerts`)) ?? [
    {
      id: 1,
      patient_user_id: 3,
      alert_type: 'activity_drop',
      severity: 'medium',
      status: 'new',
      title: 'Actividad reducida frente a línea base',
      explanation: 'Los pasos diarios bajaron frente al patrón personal.',
      recommendation: 'Confirmar descanso, fatiga y uso del reloj.',
      score: 0.34,
      created_at: '2026-04-02T09:00:00',
    },
  ]
}
