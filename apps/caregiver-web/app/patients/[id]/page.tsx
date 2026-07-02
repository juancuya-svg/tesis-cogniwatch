import { Shell } from '../../../components/Shell'
import { getPatientOverview } from '../../../lib/api'

export default async function PatientDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  const data = await getPatientOverview(id)

  return (
    <Shell>
      <div className="hero">
        <div>
          <span className="badge">Detalle del paciente</span>
          <h2>{data.patient.full_name}</h2>
          <p className="muted">Monitoreo orientado a seguimiento, cambios y alertas interpretables.</p>
        </div>
      </div>

      <section className="grid kpis">
        <div className="card"><div className="muted">Tier basal</div><div className="kpi-number">{data.patient.baseline_tier}</div></div>
        <div className="card"><div className="muted">Alertas abiertas</div><div className="kpi-number">{data.open_alerts}</div></div>
        <div className="card"><div className="muted">Último sueño</div><div className="kpi-number">{data.latest_signal?.sleep ?? '-'} min</div></div>
        <div className="card"><div className="muted">Últimos pasos</div><div className="kpi-number">{data.latest_signal?.steps ?? '-'}</div></div>
      </section>

      <section className="grid two-col" style={{ marginTop: 16 }}>
        <div className="card">
          <h3>Resumen clínico-funcional</h3>
          <p><strong>Motivo de seguimiento:</strong> {data.patient.monitoring_reason}</p>
          <p><strong>Wearable conectado:</strong> {data.patient.wearable_connected ? 'Sí' : 'No'}</p>
          <p><strong>Última FC en reposo:</strong> {data.latest_signal?.resting_hr ?? '-'} bpm</p>
          <p><strong>Adherencia wearable:</strong> {data.latest_signal?.adherence ?? '-'}</p>
        </div>
        <div className="card">
          <h3>Microevaluación cognitivo-motora</h3>
          <p className="muted">Probabilidad proxy basada en patrones de motricidad fina.</p>
          <div className="kpi-number">{data.latest_cognitive_motor_probability ?? '-'} </div>
        </div>
      </section>
    </Shell>
  )
}
