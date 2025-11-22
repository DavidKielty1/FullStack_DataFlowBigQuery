import { NextResponse } from 'next/server'

// API route for analytics data (aggregated from BigQuery/DataFlow processing)
export async function GET(request: Request) {
  try {
    // For development: query SQLite analytics database
    // In production, this would query BigQuery directly
    const Database = require('better-sqlite3')
    const path = require('path')
    
    // Use environment variable if set, otherwise use relative path
    const fs = require('fs')
    let dbPath = process.env.ANALYTICS_DATABASE_PATH || 
      path.join(process.cwd(), '..', 'databases', 'analytics.db')
    
    // Only resolve if it's a relative path (not starting with /)
    if (!dbPath.startsWith('/')) {
      dbPath = path.resolve(dbPath)
    }
    
    // Check if database file exists (directory is mounted via Docker volume)
    if (!fs.existsSync(dbPath)) {
      console.error(`Analytics database file not found at: ${dbPath}`)
      return NextResponse.json(
        { success: false, error: `Database file not found at: ${dbPath}` },
        { status: 500 }
      )
    }
    
    const db = new Database(dbPath, { readonly: true })
    
    // Get aggregated analytics
    const analytics = db.prepare(`
      SELECT 
        date,
        risk_level,
        COUNT(*) as count,
        AVG(avg_risk_score) as avg_risk_score
      FROM analytics_summary
      GROUP BY date, risk_level
      ORDER BY date DESC
      LIMIT 30
    `).all()
    
    db.close()
    
    return NextResponse.json({
      success: true,
      data: analytics
    })
  } catch (error) {
    console.error('Error fetching analytics:', error)
    return NextResponse.json(
      { success: false, error: 'Failed to fetch analytics' },
      { status: 500 }
    )
  }
}
