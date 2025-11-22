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
    const fs = require('fs')
    
    // Use environment variable if set, otherwise use relative path
    // In Docker, DATABASE_PATH is set to /app/databases/insider_risk.db
    const dbPath = process.env.DATABASE_PATH || 
      path.resolve(process.cwd(), '..', 'databases', 'insider_risk.db')
    
    // Check if database file exists (directory is mounted via Docker volume)
    if (!fs.existsSync(dbPath)) {
      console.error(`Database file not found at: ${dbPath}`)
      console.error(`Directory exists: ${fs.existsSync(path.dirname(dbPath))}`)
      return NextResponse.json(
        { success: false, error: `Database file not found at: ${dbPath}` },
        { status: 500 }
      )
    }
    
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
  } catch (error: any) {
    console.error('Error fetching events:', error)
    console.error('Database path attempted:', process.env.DATABASE_PATH || 'not set')
    console.error('Current working directory:', process.cwd())
    return NextResponse.json(
      { 
        success: false, 
        error: 'Failed to fetch events',
        details: error?.message || String(error)
      },
      { status: 500 }
    )
  }
}
