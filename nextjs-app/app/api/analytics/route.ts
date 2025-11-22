import { NextResponse } from 'next/server'

// API route for analytics data (aggregated from BigQuery/DataFlow processing)
export async function GET(request: Request) {
  try {
    // For development: query SQLite analytics database
    // In production, this would query BigQuery directly
    const Database = require('better-sqlite3')
    const path = require('path')
    
    const dbPath = path.join(process.cwd(), '..', 'databases', 'analytics.db')
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
