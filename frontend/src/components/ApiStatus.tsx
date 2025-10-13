'use client'

import { useState, useEffect } from 'react'
import { ApiService } from '../services/api'

export function ApiStatus() {
  const [status, setStatus] = useState<'checking' | 'connected' | 'error'>('checking')
  const [apiInfo, setApiInfo] = useState<{ status?: string; message?: string; timestamp?: string; version?: string } | null>(null)

  useEffect(() => {
    checkApiConnection()
  }, [])

  const checkApiConnection = async () => {
    try {
      setStatus('checking')
      const response = await ApiService.healthCheck()
      setApiInfo(response)
      setStatus('connected')
    } catch (error) {
      console.error('API connection failed:', error)
      setStatus('error')
    }
  }

  const getStatusColor = () => {
    switch (status) {
      case 'checking': return 'bg-yellow-100 text-yellow-800 border-yellow-200'
      case 'connected': return 'bg-green-100 text-green-800 border-green-200'
      case 'error': return 'bg-red-100 text-red-800 border-red-200'
      default: return 'bg-gray-100 text-gray-800 border-gray-200'
    }
  }

  const getStatusIcon = () => {
    switch (status) {
      case 'checking':
        return (
          <div className="animate-spin rounded-full h-4 w-4 border-2 border-yellow-600 border-t-transparent"></div>
        )
      case 'connected':
        return (
          <svg className="w-4 h-4 text-green-600" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
          </svg>
        )
      case 'error':
        return (
          <svg className="w-4 h-4 text-red-600" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
          </svg>
        )
    }
  }

  const getStatusText = () => {
    switch (status) {
      case 'checking': return 'Checking API...'
      case 'connected': return `API Connected (${apiInfo?.version || 'v1.0.0'})`
      case 'error': return 'API Disconnected'
      default: return 'Unknown Status'
    }
  }

  return (
    <div className={`inline-flex items-center space-x-2 px-3 py-1 rounded-full text-sm border ${getStatusColor()}`}>
      {getStatusIcon()}
      <span className="font-medium">{getStatusText()}</span>
      {status === 'error' && (
        <button
          onClick={checkApiConnection}
          className="ml-2 text-xs underline hover:no-underline"
        >
          Retry
        </button>
      )}
    </div>
  )
}