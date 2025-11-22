import { NextResponse } from 'next/server'

// API route that queries SQLite and can integrate with BigQuery results
// Note: In production, this would query BigQuery instead of SQLite
export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url)
    const limit = parseInt(searchParams.get('limit') || '100')
    
    // For development: query SQLite
    // In production, this would call BigQuery or the Java backend
    const Database = require('better-sqlite3')
    const path = require('path')
    
    const dbPath = path.join(process.cwd(), '..', 'databases', 'insider_risk.db')
    const db = new Database(dbPath, { readonly: true })
    
    // Query events (this would typically come from BigQuery in production)
    const events = db.prepare(`
      SELECT * FROM risk_events 
      ORDER BY timestamp DESC 
      LIMIT ?
    `).all(limit)
    
    db.close()
    
    return NextResponse.json({
      success: true,
      data: events,
      count: events.length
    })
  } catch (error) {
    console.error('Error fetching events:', error)
    return NextResponse.json(
      { success: false, error: 'Failed to fetch events' },
      { status: 500 }
    )
  }
}
