import './globals.css'

export const metadata = {
  title: 'CogniWatch Caregiver Dashboard',
  description: 'Caregiver console for CogniWatch',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  )
}
