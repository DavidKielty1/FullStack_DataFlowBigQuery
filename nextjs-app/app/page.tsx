export default function Home() {
  return (
    <main style={{ padding: '2rem' }}>
      <h1>Insider Risk Management Platform</h1>
      <p>Welcome to the Insider Risk Detection and Analytics Dashboard</p>
      <div style={{ marginTop: '2rem' }}>
        <h2>API Endpoints</h2>
        <ul>
          <li><a href="/api/events">/api/events</a> - Get risk events</li>
          <li><a href="/api/analytics">/api/analytics</a> - Get analytics data</li>
          <li><a href="/api/health">/api/health</a> - Health check</li>
        </ul>
      </div>
    </main>
  )
}

