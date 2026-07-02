import Link from 'next/link'

export function Sidebar() {
  return (
    <aside className="sidebar">
      <h1>CogniWatch Care</h1>
      <p>Seguimiento funcional y cognitivo para cuidadores y personal observador.</p>
      <nav className="nav">
        <Link href="/dashboard">Resumen</Link>
        <Link href="/patients">Pacientes</Link>
        <Link href="/alerts">Alertas</Link>
        <Link href="/login">Salir</Link>
      </nav>
    </aside>
  )
}
