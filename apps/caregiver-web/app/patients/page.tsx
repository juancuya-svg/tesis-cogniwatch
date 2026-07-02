import Link from 'next/link'
import { Shell } from '../../components/Shell'
import { getPatients } from '../../lib/api'

export default async function PatientsPage() {
  const patients = await getPatients()
  return (
    <Shell>
      <div className="hero">
        <div>
          <span className="badge">Pacientes</span>
          <h2>Personas asociadas</h2>
          <p className="muted">Acceso a perfiles, señales y alertas activas.</p>
        </div>
      </div>
      <div className="card">
        <table className="table">
          <thead>
            <tr>
              <th>Nombre</th>
              <th>Motivo</th>
              <th>Tier</th>
              <th>Autonomía</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {patients.map((patient: any) => (
              <tr key={patient.id}>
                <td>{patient.full_name}</td>
                <td>{patient.monitoring_reason}</td>
                <td>{patient.baseline_tier}</td>
                <td>{patient.autonomy_level}</td>
                <td><Link href={`/patients/${patient.id}`} className="badge">Ver detalle</Link></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Shell>
  )
}
