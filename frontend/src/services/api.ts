// API service for connecting to FertiSmart backend
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5001'

// Type definitions for API responses
export interface HealthCheckResponse {
  status: string;
  message: string;
  timestamp: string;
  version: string;
}

export interface DashboardData {
  totalSamples: number;
  avgPhLevel: number;
  totalRecommendations: number;
  systemHealth: 'healthy' | 'warning' | 'error';
  recentActivity: Array<{
    id: string;
    type: string;
    message: string;
    timestamp: string;
  }>;
}

export class ApiService {
  static async request(endpoint: string, options: RequestInit = {}) {
    const url = `${API_BASE_URL}${endpoint}`
    
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    }

    try {
      const response = await fetch(url, config)
      const data = await response.json()
      
      if (!response.ok) {
        throw new Error(data.message || `HTTP error! status: ${response.status}`)
      }
      
      return data
    } catch (error) {
      console.error(`API request failed for ${endpoint}:`, error)
      throw error
    }
  }

  // Health check
  static async healthCheck() {
    return this.request('/api/health')
  }

  // Analytics endpoints
  static async getDashboardData() {
    return this.request('/api/analytics/dashboard')
  }

  static async getTrends() {
    return this.request('/api/analytics/trends')
  }

  // Clustering endpoints
  static async getClusterResults() {
    return this.request('/api/clustering/results')
  }

  static async analyzeCluster(data: any) {
    return this.request('/api/clustering/analyze', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  // Recommendation endpoints
  static async getRecommendations() {
    return this.request('/api/recommendations/history')
  }

  static async generateRecommendations(filters: any) {
    return this.request('/api/recommendations/generate', {
      method: 'POST',
      body: JSON.stringify({ filters }),
    })
  }

  // Classification endpoints
  static async trainModel(data: any) {
    return this.request('/api/classification/train', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  static async makePrediction(features: any) {
    return this.request('/api/classification/predict', {
      method: 'POST',
      body: JSON.stringify({ features }),
    })
  }

  // Visualization endpoints
  static async getChartData() {
    return this.request('/api/visualization/charts')
  }

  // Schema endpoints
  static async getStarSchema() {
    return this.request('/api/schema/star')
  }

  static async getSnowflakeSchema() {
    return this.request('/api/schema/snowflake')
  }

  // Preprocessing endpoints
  static async uploadSoilData(data: any) {
    return this.request('/api/preprocessing/upload', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  static async getQualityReport() {
    return this.request('/api/preprocessing/quality-report')
  }
}