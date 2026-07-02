import Link from 'next/link'
import { Shell } from '../../components/Shell'
import { getAdminSummary, getAlerts, getPatients } from '../../lib/api'

export default async function DashboardPage() {
  const summary = await getAdminSummary()
  const patients = await getPatients()
  const alerts = await getAlerts()
  const bars = [45, 60, 48, 72, 66, 55, 38]

  return (
    <Shell>
      <div className="hero">
        <div>
          <span className="badge">Resumen operativo</span>
          <h2>Panel del cuidador</h2>
          <p className="muted">Seguimiento centrado en cambios frente a línea base, no en diagnóstico.</p>
        </div>
        <div className="card" style={{ minWidth: 260 }}>
          <div className="muted">Pacientes asociados</div>
          <div className="kpi-number">{patients.length}</div>
        </div>
      </div>

      <section className="grid kpis">
        <div className="card"><div className="muted">Pacientes</div><div className="kpi-number">{summary.patients}</div></div>
        <div className="card"><div className="muted">Cuidadores</div><div className="kpi-number">{summary.caregivers}</div></div>
        <div className="card"><div className="muted">Alertas</div><div className="kpi-number">{summary.alerts_total}</div></div>
        <div className="card"><div className="muted">Señales registradas</div><div className="kpi-number">{summary.signals_total}</div></div>
      </section>

      <section className="grid two-col" style={{ marginTop: 16 }}>
        <div className="card">
          <h3>Tendencia de estabilidad semanal</h3>
          <p className="muted">Visual rápido de variación agregada del estado funcional.</p>
          <div className="sparkline">
            {bars.map((h, idx) => <span key={idx} style={{ height: `${h}px` }} />)}
          </div>
        </div>
        <div className="card">
          <h3>Foco del día</h3>
          <p className="muted">Paciente con mayor necesidad de revisión manual.</p>
          <div className="kpi-number">Carlos Vega</div>
          <p className="status-medium">Watchlist · actividad reducida</p>
          <Link href="/patients/3" className="badge">Abrir detalle</Link>
        </div>
      </section>

      <h3 className="section-title">Alertas recientes</h3>
      <div className="card">
        <table className="table">
          <thead>
            <tr>
              <th>Paciente</th>
              <th>Alerta</th>
              <th>Severidad</th>
              <th>Estado</th>
            </tr>
          </thead>
          <tbody>
            {alerts.map((alert: any) => (
              <tr key={alert.id}>
                <td>Carlos Vega</td>
                <td>{alert.title}</td>
                <td className={`status-${alert.severity}`}>{alert.severity}</td>
                <td>{alert.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Shell>
  )
}
