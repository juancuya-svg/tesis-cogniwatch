import { ReactNode } from 'react'
import { Sidebar } from './Sidebar'

export function Shell({ children }: { children: ReactNode }) {
  return (
    <div className="shell">
      <Sidebar />
      <main className="main">{children}</main>
    </div>
  )
}
