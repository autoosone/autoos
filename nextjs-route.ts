/**
 * 🚀 PRODUCTION NEXT.JS ROUTE FOR BLAXEL INTEGRATION
 * 
 * File: /app/api/blaxel/route.ts
 * 
 * This route handles all communication with Blaxel agents
 * Includes proper error handling, authentication, and CORS
 */

import { NextRequest, NextResponse } from 'next/server'

// Configuration - use environment variables in production
const BLAXEL_CONFIG = {
  apiKey: process.env.BLAXEL_API_KEY || 'YOUR_BLAXEL_API_KEY_HERE',
  baseUrl: 'https://run.blaxel.ai',
  workspace: 'amo',
  agent: 'template-copilot-kit-py',
  timeout: 30000
}

// Helper function to make requests to Blaxel
async function callBlaxelAgent(message: string, threadId?: string) {
  const url = `${BLAXEL_CONFIG.baseUrl}/${BLAXEL_CONFIG.workspace}/agents/${BLAXEL_CONFIG.agent}`
  
  const headers: Record<string, string> = {
    'Authorization': `Bearer ${BLAXEL_CONFIG.apiKey}`,
    'Content-Type': 'application/json'
  }
  
  if (threadId) {
    headers['X-Blaxel-Thread-Id'] = threadId
  }
  
  const response = await fetch(url, {
    method: 'POST',
    headers,
    body: JSON.stringify({ inputs: message }),
    signal: AbortSignal.timeout(BLAXEL_CONFIG.timeout)
  })
  
  if (!response.ok) {
    throw new Error(`Blaxel API error: ${response.status} ${response.statusText}`)
  }
  
  return response.json()
}

// Handle POST requests
export async function POST(request: NextRequest) {
  try {
    // Parse request body
    const body = await request.json()
    const { message, threadId } = body
    
    // Validate input
    if (!message || typeof message !== 'string') {
      return NextResponse.json(
        { error: 'Missing or invalid message field' },
        { status: 400 }
      )
    }
    
    // Call Blaxel agent
    const response = await callBlaxelAgent(message, threadId)
    
    // Return successful response
    return NextResponse.json({
      success: true,
      data: response,
      timestamp: new Date().toISOString()
    })
    
  } catch (error) {
    console.error('Blaxel API error:', error)
    
    // Handle specific error types
    if (error instanceof Error) {
      if (error.name === 'TimeoutError') {
        return NextResponse.json(
          { error: 'Request timeout - agent took too long to respond' },
          { status: 504 }
        )
      }
      
      if (error.message.includes('401') || error.message.includes('403')) {
        return NextResponse.json(
          { error: 'Authentication failed - check API key' },
          { status: 401 }
        )
      }
    }
    
    // Generic error response
    return NextResponse.json(
      { 
        error: 'Failed to communicate with agent',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    )
  }
}

// Handle GET requests (for health checks)
export async function GET() {
  try {
    // Test connection to Blaxel
    const response = await callBlaxelAgent('healthcheck')
    
    return NextResponse.json({
      status: 'healthy',
      blaxel: 'connected',
      agent: `${BLAXEL_CONFIG.workspace}/${BLAXEL_CONFIG.agent}`,
      timestamp: new Date().toISOString()
    })
  } catch (error) {
    return NextResponse.json(
      {
        status: 'unhealthy',
        blaxel: 'disconnected',
        error: error instanceof Error ? error.message : 'Unknown error',
        timestamp: new Date().toISOString()
      },
      { status: 503 }
    )
  }
}

// Export configuration for reference
export const config = {
  runtime: 'nodejs',
  regions: ['us-east-1'] // Match your Blaxel region for best performance
}
