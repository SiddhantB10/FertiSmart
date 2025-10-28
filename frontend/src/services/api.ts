// API service for connecting to FertiSmart backend
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 
  (process.env.NODE_ENV === 'production' ? 'https://fertismart-backend.onrender.com' : 'http://localhost:5001')

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
  // Cache for the wake-up status
  private static isWakingUp = false;
  private static lastPingTime = 0;
  private static PING_INTERVAL = 5 * 60 * 1000; // 5 minutes

  // Wake up the backend if it's sleeping (Render free tier)
  static async wakeUpBackend(): Promise<boolean> {
    const now = Date.now();
    
    // If we recently pinged, skip
    if (now - this.lastPingTime < this.PING_INTERVAL) {
      return true;
    }

    try {
      this.isWakingUp = true;
      const response = await fetch(`${API_BASE_URL}/api/health`, {
        method: 'GET',
        signal: AbortSignal.timeout(30000), // 30 second timeout
      });
      this.lastPingTime = now;
      this.isWakingUp = false;
      return response.ok;
    } catch (error) {
      this.isWakingUp = false;
      console.warn('Backend wake-up failed:', error);
      return false;
    }
  }

  static async request(endpoint: string, options: RequestInit = {}) {
    const url = `${API_BASE_URL}${endpoint}`
    
    // For critical endpoints, wake up backend first
    if (endpoint.includes('/predict') || endpoint.includes('/recommend')) {
      await this.wakeUpBackend();
    }
    
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
        throw new Error(data.message || data.error || `HTTP error! status: ${response.status}`)
      }
      
      return data
    } catch (error) {
      // Only log in development mode
      if (process.env.NODE_ENV === 'development') {
        console.error(`API request failed for ${endpoint}:`, error)
      }
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

  static async analyzeCluster(data: Record<string, unknown>) {
    return this.request('/api/clustering/analyze', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  // Recommendation endpoints
  static async getRecommendations() {
    return this.request('/api/recommendations/history')
  }

  static async generateRecommendations(filters: Record<string, unknown>) {
    return this.request('/api/recommendations/generate', {
      method: 'POST',
      body: JSON.stringify({ filters }),
    })
  }

  // Classification endpoints
  static async trainModel(data: Record<string, unknown>) {
    return this.request('/api/classification/train', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  static async makePrediction(features: Record<string, unknown>) {
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
  static async uploadSoilData(data: Record<string, unknown>) {
    return this.request('/api/preprocessing/upload', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  static async getQualityReport() {
    return this.request('/api/preprocessing/quality-report')
  }

  // Crop Recommendation endpoints
  static async trainCropModel() {
    return this.request('/api/crop-recommendation/train', {
      method: 'POST',
    })
  }

  static async predictCrop(soilClimateData: {
    N: number;
    P: number;
    K: number;
    temperature: number;
    humidity: number;
    ph: number;
    rainfall: number;
  }) {
    return this.request('/api/crop-recommendation/predict', {
      method: 'POST',
      body: JSON.stringify(soilClimateData),
    })
  }
}

// Default export
export default ApiService