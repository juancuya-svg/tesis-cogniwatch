export default function LoginPage() {
  return (
    <div className="container login-wrap">
      <div className="card">
        <span className="badge">Acceso cuidador</span>
        <h2>Bienvenido a CogniWatch</h2>
        <p className="muted">Panel para cuidadores, staff y seguimiento longitudinal.</p>
        <input className="input" placeholder="Correo" defaultValue="caregiver@cogniwatch.local" />
        <div style={{ height: 12 }} />
        <input className="input" placeholder="Contraseña" defaultValue="ChangeMe123!" type="password" />
        <button className="button">Ingresar</button>
      </div>
    </div>
  )
}
