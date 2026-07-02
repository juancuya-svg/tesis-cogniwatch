import { Shell } from '../../components/Shell'
import { getAlerts } from '../../lib/api'

export default async function AlertsPage() {
  const alerts = await getAlerts()
  return (
    <Shell>
      <div className="hero">
        <div>
          <span className="badge">Alertas</span>
          <h2>Cola de revisión</h2>
          <p className="muted">Cada alerta explica el cambio detectado y la acción sugerida.</p>
        </div>
      </div>
      <div className="card">
        <table className="table">
          <thead>
            <tr>
              <th>Título</th>
              <th>Explicación</th>
              <th>Severidad</th>
              <th>Recomendación</th>
            </tr>
          </thead>
          <tbody>
            {alerts.map((alert: any) => (
              <tr key={alert.id}>
                <td>{alert.title}</td>
                <td>{alert.explanation}</td>
                <td className={`status-${alert.severity}`}>{alert.severity}</td>
                <td>{alert.recommendation}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Shell>
  )
}
