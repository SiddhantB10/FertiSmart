'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Navbar } from '@/components/Layout/Navbar';
import { Footer } from '@/components/Layout/Footer';

// Use environment variable for API URL with fallback
const API_URL = process.env.NEXT_PUBLIC_API_URL || 
  (process.env.NODE_ENV === 'production' ? 'https://fertismart-backend.onrender.com' : 'http://localhost:5001');

// Feature name mapping for professional display
const FEATURE_NAMES: Record<string, string> = {
  'N': 'Nitrogen',
  'P': 'Phosphorus',
  'K': 'Potassium',
  'temperature': 'Temperature',
  'humidity': 'Humidity',
  'ph': 'Soil pH',
  'rainfall': 'Rainfall'
};

const FEATURE_DESCRIPTIONS: Record<string, string> = {
  'N': 'Nitrogen content in soil (kg/ha)',
  'P': 'Phosphorus content in soil (kg/ha)',
  'K': 'Potassium content in soil (kg/ha)',
  'temperature': 'Average temperature (°C)',
  'humidity': 'Relative humidity (%)',
  'ph': 'Soil pH level',
  'rainfall': 'Annual rainfall (mm)'
};

interface ModelInfo {
  accuracy?: number;
  n_crops?: number;
  crops?: string[];
}

interface Recommendation {
  crop: string;
  confidence: number;
  suitable: boolean;
}

interface PredictionResult {
  recommended_crop: string;
  confidence: number;
  top_recommendations: Recommendation[];
  explanation: {
    crop_info: string;
    conditions_analysis: string[];
    confidence_level: string;
    recommendation: string;
  };
  feature_importance: Record<string, number>;
  most_important_factor: {
    feature: string;
    importance: number;
  };
}

export default function CropPredictionPage() {
  const [modelInfo, setModelInfo] = useState<ModelInfo>({});
  const [loading, setLoading] = useState(false);
  const [warming, setWarming] = useState(false);
  const [predictionResult, setPredictionResult] = useState<PredictionResult | null>(null);
  const [error, setError] = useState('');
  
  const [formData, setFormData] = useState({
    N: '',
    P: '',
    K: '',
    temperature: '',
    humidity: '',
    ph: '',
    rainfall: ''
  });

  useEffect(() => {
    fetchModelInfo();
    // Warm up the backend when page loads
    warmUpBackend();
  }, []);

  const warmUpBackend = async () => {
    try {
      setWarming(true);
      // Ping the health endpoint to wake up Render
      await fetch(`${API_URL}/api/health`, { 
        method: 'GET',
        signal: AbortSignal.timeout(15000) // 15 second timeout
      });
    } catch (err) {
      console.warn('Backend warm-up failed:', err);
    } finally {
      setTimeout(() => setWarming(false), 1000);
    }
  };

  const fetchModelInfo = async () => {
    try {
      console.log('Fetching model info from:', `${API_URL}/api/model/info`);
      const response = await fetch(`${API_URL}/api/model/info`, {
        signal: AbortSignal.timeout(15000)
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('Model info received:', data);
      setModelInfo(data);
    } catch (err) {
      console.error('Failed to fetch model info:', err);
      setError(`Failed to connect to backend: ${err instanceof Error ? err.message : 'Unknown error'}`);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handlePredict = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setPredictionResult(null);

    try {
      // Validate form data
      const requiredFields = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall'];
      for (const field of requiredFields) {
        if (!formData[field as keyof typeof formData] || isNaN(parseFloat(formData[field as keyof typeof formData]))) {
          setError(`Please enter a valid value for ${FEATURE_NAMES[field]}`);
          setLoading(false);
          return;
        }
      }

      const payload = {
        N: parseFloat(formData.N),
        P: parseFloat(formData.P),
        K: parseFloat(formData.K),
        temperature: parseFloat(formData.temperature),
        humidity: parseFloat(formData.humidity),
        ph: parseFloat(formData.ph),
        rainfall: parseFloat(formData.rainfall)
      };

      console.log('Sending prediction request:', payload);
      console.log('API URL:', `${API_URL}/api/predict`);

      const response = await fetch(`${API_URL}/api/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
        signal: AbortSignal.timeout(30000) // 30 second timeout for first request
      });

      console.log('Response status:', response.status);
      console.log('Response headers:', response.headers);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log('Prediction response:', data);

      if (data.success) {
        setPredictionResult(data);
      } else {
        setError(data.error || 'Prediction failed');
      }
    } catch (err) {
      console.error('Prediction error:', err);
      setError(`Failed to get prediction: ${err instanceof Error ? err.message : 'Unknown error'}`);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFormData({
      N: '',
      P: '',
      K: '',
      temperature: '',
      humidity: '',
      ph: '',
      rainfall: ''
    });
    setPredictionResult(null);
    setError('');
  };

  const loadSampleData = () => {
    // Generate random values within realistic ranges for crop cultivation
    const randomInRange = (min: number, max: number, decimals: number = 0) => {
      const value = Math.random() * (max - min) + min;
      return decimals > 0 ? value.toFixed(decimals) : Math.round(value).toString();
    };

    const sampleData = {
      N: randomInRange(0, 140),           // Nitrogen: 0-140 kg/ha
      P: randomInRange(5, 145),           // Phosphorus: 5-145 kg/ha
      K: randomInRange(5, 205),           // Potassium: 5-205 kg/ha
      temperature: randomInRange(8, 44, 1),  // Temperature: 8-44°C
      humidity: randomInRange(14, 100),   // Humidity: 14-100%
      ph: randomInRange(3.5, 9.9, 1),     // pH: 3.5-9.9
      rainfall: randomInRange(20, 300, 1) // Rainfall: 20-300mm
    };

    console.log('Loading sample data:', sampleData);
    setFormData(sampleData);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-green-50 dark:from-gray-900 dark:via-gray-800 dark:to-emerald-900 transition-colors">
      <Navbar />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Title Section */}
        <div className="text-center mb-8 animate-fade-in">
          <div className="inline-block px-4 py-2 bg-gradient-to-r from-emerald-100 to-teal-100 dark:from-emerald-900/30 dark:to-teal-900/30 rounded-full mb-4 shadow-sm hover:shadow-md transition-all duration-300 transform hover:scale-105">
            <span className="text-sm font-semibold gradient-text">Random Forest ML Algorithm</span>
          </div>
          <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-3 animate-slide-up">
            Intelligent <span className="gradient-text">Crop Recommendation</span> System
          </h2>
          <p className="text-lg text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            Enter your soil and climate parameters to receive data-driven crop recommendations
          </p>
        </div>

        {/* Error Display */}
        {error && (
          <Alert className="mb-8 border-red-200 dark:border-red-800 bg-red-50 dark:bg-red-900/20">
            <AlertDescription className="text-red-700 dark:text-red-300 font-medium">
              ⚠️ {error}
            </AlertDescription>
          </Alert>
        )}

        {/* Backend Warming Indicator */}
        {warming && (
          <Alert className="mb-8 border-blue-200 dark:border-blue-800 bg-blue-50 dark:bg-blue-900/20">
            <AlertDescription className="text-blue-700 dark:text-blue-300 font-medium flex items-center gap-2">
              <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              🚀 Waking up backend server... This may take a few seconds on first load.
            </AlertDescription>
          </Alert>
        )}

        {/* Model Info */}
        {modelInfo.accuracy && (
          <div className="bg-white/90 dark:bg-gray-800/90 backdrop-blur-sm rounded-2xl shadow-2xl dark:shadow-emerald-500/20 p-6 mb-8 border border-emerald-200 dark:border-emerald-700 animate-slide-in-left hover:scale-105 transition-all duration-300">
            <div className="flex items-center justify-between flex-wrap gap-6">
              <div className="flex items-center gap-4">
                <div className="w-16 h-16 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-2xl flex items-center justify-center shadow-lg animate-bounce-gentle">
                  <span className="text-3xl">🤖</span>
                </div>
                <div>
                  <h3 className="text-xl font-bold text-emerald-600 dark:text-emerald-400">Model Performance</h3>
                  <p className="text-sm text-gray-600 dark:text-gray-300">Trained on 55,500+ crop samples</p>
                </div>
              </div>
              <div className="flex gap-6">
                <div className="text-center group bg-gradient-to-br from-emerald-500 to-emerald-600 dark:from-emerald-400 dark:to-emerald-500 rounded-2xl p-6 hover:from-emerald-400 hover:to-emerald-500 dark:hover:from-emerald-300 dark:hover:to-emerald-400 transition-all duration-300 shadow-lg dark:shadow-emerald-400/20 min-w-[120px]">
                  <div className="text-4xl font-bold text-white dark:text-gray-900 transform group-hover:scale-110 transition-transform duration-300">
                    {modelInfo.accuracy || '97.32'}%
                  </div>
                  <div className="text-sm text-emerald-100 dark:text-gray-800 font-medium mt-1">Model Accuracy</div>
                </div>
                <div className="w-px bg-gradient-to-b from-transparent via-emerald-400 dark:via-emerald-300 to-transparent"></div>
                <div className="text-center group bg-gradient-to-br from-teal-500 to-teal-600 dark:from-teal-400 dark:to-teal-500 rounded-2xl p-6 hover:from-teal-400 hover:to-teal-500 dark:hover:from-teal-300 dark:hover:to-teal-400 transition-all duration-300 shadow-lg dark:shadow-teal-400/20 min-w-[120px]">
                  <div className="text-4xl font-bold text-white dark:text-gray-900 transform group-hover:scale-110 transition-transform duration-300">
                    {modelInfo.n_crops || '37'}
                  </div>
                  <div className="text-sm text-teal-100 dark:text-gray-800 font-medium mt-1">Crops Supported</div>
                </div>
                <div className="w-px bg-gradient-to-b from-transparent via-emerald-400 dark:via-emerald-300 to-transparent"></div>
                <div className="text-center group bg-gradient-to-br from-cyan-500 to-cyan-600 dark:from-cyan-400 dark:to-cyan-500 rounded-2xl p-6 hover:from-cyan-400 hover:to-cyan-500 dark:hover:from-cyan-300 dark:hover:to-cyan-400 transition-all duration-300 shadow-lg dark:shadow-cyan-400/20 min-w-[120px]">
                  <div className="text-4xl font-bold text-white dark:text-gray-900 transform group-hover:scale-110 transition-transform duration-300">
                    7
                  </div>
                  <div className="text-sm text-cyan-100 dark:text-gray-800 font-medium mt-1">Input Parameters</div>
                </div>
              </div>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Input Form */}
          <Card className="shadow-2xl dark:shadow-emerald-500/20 border-t-4 border-emerald-500 dark:border-emerald-400 animate-slide-in-left hover:shadow-3xl transition-all duration-300">
            <CardHeader className="bg-gradient-to-r from-emerald-600 via-teal-600 to-blue-600 text-white">
              <CardTitle className="text-2xl flex items-center gap-2">
                <span className="animate-bounce-gentle">📝</span> Input Parameters
              </CardTitle>
              <p className="text-sm text-emerald-100 mt-2">
                Enter your field&apos;s soil and climate data for accurate prediction
              </p>
            </CardHeader>
            <CardContent className="pt-6">
              <form onSubmit={handlePredict} className="space-y-6">
                {/* Soil Nutrients */}
                <div className="bg-white/70 dark:bg-gray-700/50 backdrop-blur-sm rounded-xl p-6 border-2 border-emerald-200 dark:border-emerald-700 hover:border-emerald-400 dark:hover:border-emerald-500 transition-all duration-300 hover:shadow-lg dark:hover:shadow-emerald-500/20">
                  <h3 className="text-lg font-bold gradient-text mb-4 flex items-center gap-2">
                    🧪 Soil Nutrients <span className="text-sm font-normal text-gray-500 dark:text-gray-400">(kg/ha)</span>
                  </h3>
                  <div className="grid grid-cols-3 gap-4">
                    <div>
                      <Label htmlFor="N" className="text-sm font-semibold">Nitrogen</Label>
                      <Input
                        id="N"
                        name="N"
                        type="number"
                        step="0.01"
                        value={formData.N}
                        onChange={handleInputChange}
                        placeholder="0-140"
                        required
                        className="mt-2"
                      />
                    </div>
                    <div>
                      <Label htmlFor="P" className="text-sm font-semibold">Phosphorus</Label>
                      <Input
                        id="P"
                        name="P"
                        type="number"
                        step="0.01"
                        value={formData.P}
                        onChange={handleInputChange}
                        placeholder="5-145"
                        required
                        className="mt-2"
                      />
                    </div>
                    <div>
                      <Label htmlFor="K" className="text-sm font-semibold">Potassium</Label>
                      <Input
                        id="K"
                        name="K"
                        type="number"
                        step="0.01"
                        value={formData.K}
                        onChange={handleInputChange}
                        placeholder="5-205"
                        required
                        className="mt-2"
                      />
                    </div>
                  </div>
                </div>

                {/* Climate Conditions */}
                <div className="bg-white/70 dark:bg-gray-700/50 backdrop-blur-sm rounded-xl p-6 border-2 border-teal-200 dark:border-teal-700 hover:border-teal-400 dark:hover:border-teal-500 transition-all duration-300 hover:shadow-lg dark:hover:shadow-teal-500/20">
                  <h3 className="text-lg font-bold gradient-text mb-4 flex items-center gap-2">
                    🌤️ Climate Conditions
                  </h3>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="temperature" className="text-sm font-semibold">Temperature (°C)</Label>
                      <Input
                        id="temperature"
                        name="temperature"
                        type="number"
                        step="0.1"
                        value={formData.temperature}
                        onChange={handleInputChange}
                        placeholder="8-44"
                        required
                        className="mt-2"
                      />
                    </div>
                    <div>
                      <Label htmlFor="humidity" className="text-sm font-semibold">Humidity (%)</Label>
                      <Input
                        id="humidity"
                        name="humidity"
                        type="number"
                        step="0.1"
                        value={formData.humidity}
                        onChange={handleInputChange}
                        placeholder="14-100"
                        required
                        className="mt-2"
                      />
                    </div>
                  </div>
                </div>

                {/* Soil pH & Rainfall */}
                <div className="bg-white/70 dark:bg-gray-700/50 backdrop-blur-sm rounded-xl p-6 border-2 border-blue-200 dark:border-blue-700 hover:border-blue-400 dark:hover:border-blue-500 transition-all duration-300 hover:shadow-lg dark:hover:shadow-blue-500/20">
                  <h3 className="text-lg font-bold gradient-text mb-4 flex items-center gap-2">
                    🌧️ Soil pH & Rainfall
                  </h3>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="ph" className="text-sm font-semibold">Soil pH</Label>
                      <Input
                        id="ph"
                        name="ph"
                        type="number"
                        step="0.01"
                        value={formData.ph}
                        onChange={handleInputChange}
                        placeholder="3.5-9.9"
                        required
                        className="mt-2"
                      />
                    </div>
                    <div>
                      <Label htmlFor="rainfall" className="text-sm font-semibold">Rainfall (mm)</Label>
                      <Input
                        id="rainfall"
                        name="rainfall"
                        type="number"
                        step="0.1"
                        value={formData.rainfall}
                        onChange={handleInputChange}
                        placeholder="20-300"
                        required
                        className="mt-2"
                      />
                    </div>
                  </div>
                </div>

                {/* Buttons */}
                <Button
                  type="submit"
                  disabled={loading}
                  className="w-full bg-gradient-to-r from-emerald-600 via-teal-600 to-blue-600 hover:from-emerald-700 hover:via-teal-700 hover:to-blue-700 text-white font-bold py-4 text-lg shadow-lg hover:shadow-2xl dark:shadow-emerald-500/20 transform hover:scale-105 transition-all duration-300"
                >
                  {loading ? (
                    <span className="flex items-center justify-center gap-2">
                      <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      <span>Analyzing soil conditions...</span>
                    </span>
                  ) : (
                    <span className="flex items-center justify-center gap-2">
                      🚀 Get Crop Recommendation
                    </span>
                  )}
                </Button>
                
                <div className="grid grid-cols-2 gap-3">
                  <Button 
                    type="button" 
                    variant="outline" 
                    onClick={loadSampleData}
                    className="border-2 border-emerald-400 dark:border-emerald-500 text-emerald-600 dark:text-emerald-400 hover:bg-emerald-50 dark:hover:bg-emerald-900/20 transform hover:scale-105 transition-all duration-300"
                  >
                    <span className="flex items-center justify-center gap-2">
                      📋 Load Sample
                    </span>
                  </Button>
                  <Button 
                    type="button" 
                    variant="outline" 
                    onClick={handleReset}
                    className="border-2 border-gray-400 dark:border-gray-500 text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800 transform hover:scale-105 transition-all duration-300"
                  >
                    <span className="flex items-center justify-center gap-2">
                      🔄 Reset
                    </span>
                  </Button>
                </div>
              </form>

              {error && (
                <Alert className="mt-6 bg-red-50 dark:bg-red-900/20 border-2 border-red-300 dark:border-red-800 animate-slide-in-left">
                  <AlertDescription className="text-red-800 dark:text-red-300 font-medium">{error}</AlertDescription>
                </Alert>
              )}
            </CardContent>
          </Card>

          {/* Results */}
          <div className="space-y-6">
            {predictionResult ? (
              <>
                {/* Main Recommendation */}
                <Card className="shadow-2xl dark:shadow-emerald-500/20 border-t-4 border-emerald-500 dark:border-emerald-400 animate-bounce-in">
                  <CardHeader className="bg-gradient-to-r from-emerald-500 to-emerald-600 text-white">
                    <CardTitle className="text-2xl flex items-center gap-2">
                      🎯 Recommended Crop
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="pt-6">
                    <div className="text-center mb-6">
                      <div className="text-6xl font-bold gradient-text mb-2 animate-scale-in">
                        {predictionResult.recommended_crop.toUpperCase()}
                      </div>
                      <div className="text-2xl text-gray-600 dark:text-gray-300 mb-4 animate-fade-in">
                        {predictionResult.confidence}% Confidence
                      </div>
                      <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3 mb-4 overflow-hidden">
                        <div 
                          className="bg-gradient-to-r from-emerald-500 via-teal-500 to-blue-500 h-3 rounded-full animate-slide-in-left" 
                          style={{ width: `${predictionResult.confidence}%` }}
                        ></div>
                      </div>
                    </div>
                    <div className="bg-white/70 dark:bg-gray-700/50 backdrop-blur-sm rounded-lg p-4 mb-4 border border-emerald-200 dark:border-emerald-700 hover:shadow-lg dark:hover:shadow-emerald-500/20 transition-all duration-300">
                      <p className="text-gray-800 dark:text-gray-200">{predictionResult.explanation.crop_info}</p>
                    </div>
                  </CardContent>
                </Card>

                {/* Top 3 Recommendations */}
                <Card className="shadow-2xl dark:shadow-teal-500/20 animate-slide-in-right">
                  <CardHeader className="bg-gradient-to-r from-teal-500 to-blue-600 text-white">
                    <CardTitle className="flex items-center gap-2">📊 Top 3 Recommendations</CardTitle>
                  </CardHeader>
                  <CardContent className="pt-6">
                    <div className="space-y-3">
                      {predictionResult.top_recommendations.map((rec, index) => (
                        <div 
                          key={index} 
                          className={`p-4 rounded-lg border-2 transform hover:scale-105 transition-all duration-300 ${
                            index === 0 ? 'bg-white/70 dark:bg-gray-700/50 backdrop-blur-sm border-emerald-400 dark:border-emerald-500 shadow-lg dark:shadow-emerald-500/20' : 
                            'bg-white/70 dark:bg-gray-700/50 backdrop-blur-sm border-gray-300 dark:border-gray-600'
                          }`}
                        >
                          <div className="flex justify-between items-center mb-2">
                            <span className="text-lg font-semibold flex items-center gap-2 text-gray-800 dark:text-gray-200">
                              {index === 0 && '🥇'}
                              {index === 1 && '🥈'}
                              {index === 2 && '🥉'}
                              {rec.crop}
                            </span>
                            <span className="text-xl font-bold gradient-text">{rec.confidence}%</span>
                          </div>
                          <div className="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-2.5 overflow-hidden">
                            <div 
                              className="bg-gradient-to-r from-teal-500 to-emerald-500 h-2.5 rounded-full transition-all duration-1000" 
                              style={{ width: `${rec.confidence}%` }}
                            ></div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>

                {/* Feature Importance - WITH FULL NAMES */}
                <Card className="shadow-2xl dark:shadow-orange-500/20 border-t-4 border-orange-500 dark:border-orange-400 animate-slide-up">
                  <CardHeader className="bg-gradient-to-r from-orange-500 to-red-600 text-white">
                    <CardTitle className="flex items-center gap-2">📈 Feature Importance Analysis</CardTitle>
                    <p className="text-sm text-orange-100 mt-2">Which factors influenced this recommendation</p>
                  </CardHeader>
                  <CardContent className="pt-6">
                    <div className="mb-6 p-4 bg-white/70 dark:bg-gray-700/50 backdrop-blur-sm rounded-xl border-2 border-orange-300 dark:border-orange-700 hover:shadow-lg dark:hover:shadow-orange-500/20 transition-all duration-300">
                      <p className="text-xs text-gray-500 uppercase mb-1">Most Important Factor</p>
                      <p className="text-2xl font-bold gradient-text">
                        {FEATURE_NAMES[predictionResult.most_important_factor.feature] || predictionResult.most_important_factor.feature}
                      </p>
                      <p className="text-sm text-orange-600 font-semibold">
                        {(predictionResult.most_important_factor.importance * 100).toFixed(1)}% Importance
                      </p>
                    </div>
                    <div className="space-y-4">
                      {Object.entries(predictionResult.feature_importance)
                        .sort(([, a], [, b]) => b - a)
                        .map(([feature, importance], index) => (
                          <div key={feature} className="transform hover:scale-105 transition-all duration-300">
                            <div className="flex justify-between items-center mb-2">
                              <div>
                                <div className="flex items-center gap-2">
                                  <span className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold transform hover:rotate-12 transition-transform duration-300 ${
                                    index === 0 ? 'bg-gradient-to-br from-orange-500 to-red-500 text-white shadow-lg' :
                                    index === 1 ? 'bg-gradient-to-br from-orange-400 to-red-400 text-white shadow-md' :
                                    index === 2 ? 'bg-gradient-to-br from-orange-300 to-red-300 text-white shadow-sm' :
                                    'bg-gray-200 text-gray-600'
                                  }`}>
                                    {index + 1}
                                  </span>
                                  <div>
                                    <span className="font-bold text-gray-900">
                                      {FEATURE_NAMES[feature] || feature}
                                    </span>
                                    <p className="text-xs text-gray-500">{FEATURE_DESCRIPTIONS[feature]}</p>
                                  </div>
                                </div>
                              </div>
                              <span className="text-lg font-bold text-orange-600">
                                {(importance * 100).toFixed(1)}%
                              </span>
                            </div>
                            <div className="w-full bg-gray-200 rounded-full h-3">
                              <div
                                className={`h-3 rounded-full ${
                                  index === 0 ? 'bg-gradient-to-r from-orange-500 to-red-500' :
                                  index === 1 ? 'bg-gradient-to-r from-orange-400 to-red-400' :
                                  'bg-gradient-to-r from-gray-400 to-gray-500'
                                }`}
                                style={{ width: `${importance * 100}%` }}
                              ></div>
                            </div>
                          </div>
                        ))}
                    </div>
                  </CardContent>
                </Card>

                {/* Conditions Analysis */}
                {predictionResult.explanation.conditions_analysis.length > 0 && (
                  <Card className="shadow-xl">
                    <CardHeader className="bg-gradient-to-r from-purple-500 to-pink-600 text-white">
                      <CardTitle>🔍 Conditions Analysis</CardTitle>
                    </CardHeader>
                    <CardContent className="pt-6">
                      <ul className="space-y-2">
                        {predictionResult.explanation.conditions_analysis.map((analysis, index) => (
                          <li key={index} className="flex items-start gap-2">
                            <span className="text-green-500 mt-1">✓</span>
                            <span className="text-gray-700">{analysis}</span>
                          </li>
                        ))}
                      </ul>
                    </CardContent>
                  </Card>
                )}
              </>
            ) : (
              <Card className="shadow-xl">
                <CardContent className="pt-12 pb-12 text-center">
                  <div className="text-6xl mb-4">🌱</div>
                  <h3 className="text-2xl font-semibold text-gray-700 mb-2">Ready to Get Started?</h3>
                  <p className="text-gray-500">Enter your soil and climate conditions to receive crop recommendations</p>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
      
      <Footer />
    </div>
  );
}
