import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Insider Risk Management',
  description: 'Insider Risk Detection and Analytics Platform',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}

