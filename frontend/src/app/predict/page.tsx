'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Alert, AlertDescription } from '@/components/ui/alert';

const API_URL = 'http://localhost:5001';

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
  }, []);

  const fetchModelInfo = async () => {
    try {
      const response = await fetch(`${API_URL}/api/model/info`);
      const data = await response.json();
      setModelInfo(data);
    } catch (err) {
      console.error('Failed to fetch model info:', err);
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
      const payload = {
        N: parseFloat(formData.N),
        P: parseFloat(formData.P),
        K: parseFloat(formData.K),
        temperature: parseFloat(formData.temperature),
        humidity: parseFloat(formData.humidity),
        ph: parseFloat(formData.ph),
        rainfall: parseFloat(formData.rainfall)
      };

      const response = await fetch(`${API_URL}/api/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
      });

      const data = await response.json();

      if (data.success) {
        setPredictionResult(data);
      } else {
        setError(data.error || 'Prediction failed');
      }
    } catch {
      setError('Failed to connect to the server. Please ensure the backend is running.');
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

    setFormData({
      N: randomInRange(0, 140),           // Nitrogen: 0-140 kg/ha
      P: randomInRange(5, 145),           // Phosphorus: 5-145 kg/ha
      K: randomInRange(5, 205),           // Potassium: 5-205 kg/ha
      temperature: randomInRange(8, 44, 1),  // Temperature: 8-44°C
      humidity: randomInRange(14, 100),   // Humidity: 14-100%
      ph: randomInRange(3.5, 9.9, 1),     // pH: 3.5-9.9
      rainfall: randomInRange(20, 300, 1) // Rainfall: 20-300mm
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-green-50">
      {/* Professional Header */}
      <div className="bg-white border-b border-gray-200 shadow-sm sticky top-0 z-50 backdrop-blur-sm bg-white/95 animate-slide-up">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3 group">
              <div className="w-12 h-12 bg-gradient-to-br from-green-500 to-blue-600 rounded-xl flex items-center justify-center shadow-lg transform group-hover:scale-110 group-hover:rotate-12 transition-all duration-300">
                <span className="text-2xl">🌾</span>
              </div>
              <div>
                <h1 className="text-2xl font-bold gradient-text">FertiSmart</h1>
                <p className="text-sm text-gray-500">AI-Powered Crop Recommendation</p>
              </div>
            </div>
            <a href="/" className="text-sm text-gray-600 hover:text-green-600 transition-all duration-300 transform hover:scale-105 px-4 py-2 rounded-lg hover:bg-green-50">
              ← Back to Home
            </a>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Title Section */}
        <div className="text-center mb-8 animate-fade-in">
          <div className="inline-block px-4 py-2 bg-gradient-to-r from-green-100 to-blue-100 rounded-full mb-4 shadow-sm hover:shadow-md transition-all duration-300 transform hover:scale-105">
            <span className="text-sm font-semibold gradient-text">Random Forest ML Algorithm</span>
          </div>
          <h2 className="text-4xl font-bold text-gray-900 mb-3 animate-slide-up">
            Intelligent <span className="gradient-text">Crop Recommendation</span> System
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Enter your soil and climate parameters to receive data-driven crop recommendations
          </p>
        </div>

        {/* Model Info */}
        {modelInfo.accuracy && (
          <div className="glass-card rounded-2xl shadow-2xl p-6 mb-8 border border-blue-200 animate-slide-in-left hover:scale-105 transition-all duration-300">
            <div className="flex items-center justify-between flex-wrap gap-6">
              <div className="flex items-center gap-4">
                <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl flex items-center justify-center shadow-lg animate-bounce-gentle">
                  <span className="text-3xl">🤖</span>
                </div>
                <div>
                  <h3 className="text-xl font-bold gradient-text">Model Performance</h3>
                  <p className="text-sm text-gray-600">Trained on 2,200+ crop samples</p>
                </div>
              </div>
              <div className="flex gap-8">
                <div className="text-center group">
                  <div className="text-4xl font-bold gradient-text transform group-hover:scale-110 transition-transform duration-300">
                    {modelInfo.accuracy}%
                  </div>
                  <div className="text-sm text-gray-600 font-medium">Model Accuracy</div>
                </div>
                <div className="w-px bg-gradient-to-b from-transparent via-gray-300 to-transparent"></div>
                <div className="text-center group">
                  <div className="text-4xl font-bold gradient-text transform group-hover:scale-110 transition-transform duration-300">
                    {modelInfo.n_crops}
                  </div>
                  <div className="text-sm text-gray-600 font-medium">Crops Supported</div>
                </div>
              </div>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Input Form */}
          <Card className="shadow-2xl border-t-4 border-green-500 animate-slide-in-left hover:shadow-3xl transition-all duration-300">
            <CardHeader className="bg-gradient-to-r from-green-600 via-blue-600 to-purple-600 text-white">
              <CardTitle className="text-2xl flex items-center gap-2">
                <span className="animate-bounce-gentle">📝</span> Input Parameters
              </CardTitle>
              <p className="text-sm text-blue-100 mt-2">
                Enter your field&apos;s soil and climate data for accurate prediction
              </p>
            </CardHeader>
            <CardContent className="pt-6">
              <form onSubmit={handlePredict} className="space-y-6">
                {/* Soil Nutrients */}
                <div className="glass-card rounded-xl p-6 border-2 border-green-200 hover:border-green-400 transition-all duration-300 hover:shadow-lg">
                  <h3 className="text-lg font-bold gradient-text mb-4 flex items-center gap-2">
                    🧪 Soil Nutrients <span className="text-sm font-normal text-gray-500">(kg/ha)</span>
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
                <div className="glass-card rounded-xl p-6 border-2 border-blue-200 hover:border-blue-400 transition-all duration-300 hover:shadow-lg">
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
                <div className="glass-card rounded-xl p-6 border-2 border-purple-200 hover:border-purple-400 transition-all duration-300 hover:shadow-lg">
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
                  className="w-full bg-gradient-to-r from-green-600 via-blue-600 to-purple-600 hover:from-green-700 hover:via-blue-700 hover:to-purple-700 text-white font-bold py-4 text-lg shadow-lg hover:shadow-2xl transform hover:scale-105 transition-all duration-300 animate-glow"
                >
                  {loading ? (
                    <span className="flex items-center justify-center gap-2">
                      <span className="animate-spin">🔄</span> Analyzing...
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
                    className="border-2 border-blue-400 text-blue-600 hover:bg-blue-50 transform hover:scale-105 transition-all duration-300"
                  >
                    <span className="flex items-center justify-center gap-2">
                      📋 Load Sample
                    </span>
                  </Button>
                  <Button 
                    type="button" 
                    variant="outline" 
                    onClick={handleReset}
                    className="border-2 border-gray-400 text-gray-600 hover:bg-gray-50 transform hover:scale-105 transition-all duration-300"
                  >
                    <span className="flex items-center justify-center gap-2">
                      🔄 Reset
                    </span>
                  </Button>
                </div>
              </form>

              {error && (
                <Alert className="mt-6 bg-red-50 border-2 border-red-300 animate-slide-in-left">
                  <AlertDescription className="text-red-800 font-medium">{error}</AlertDescription>
                </Alert>
              )}
            </CardContent>
          </Card>

          {/* Results */}
          <div className="space-y-6">
            {predictionResult ? (
              <>
                {/* Main Recommendation */}
                <Card className="shadow-2xl border-t-4 border-green-500 animate-bounce-in">
                  <CardHeader className="bg-gradient-to-r from-green-500 to-green-600 text-white">
                    <CardTitle className="text-2xl flex items-center gap-2">
                      🎯 Recommended Crop
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="pt-6">
                    <div className="text-center mb-6">
                      <div className="text-6xl font-bold gradient-text mb-2 animate-scale-in">
                        {predictionResult.recommended_crop.toUpperCase()}
                      </div>
                      <div className="text-2xl text-gray-600 mb-4 animate-fade-in">
                        {predictionResult.confidence}% Confidence
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-3 mb-4 overflow-hidden">
                        <div 
                          className="bg-gradient-to-r from-green-500 via-blue-500 to-purple-500 h-3 rounded-full animate-slide-in-left" 
                          style={{ width: `${predictionResult.confidence}%` }}
                        ></div>
                      </div>
                    </div>
                    <div className="glass-card rounded-lg p-4 mb-4 border border-blue-200 hover:shadow-lg transition-all duration-300">
                      <p className="text-gray-800">{predictionResult.explanation.crop_info}</p>
                    </div>
                  </CardContent>
                </Card>

                {/* Top 3 Recommendations */}
                <Card className="shadow-2xl animate-slide-in-right">
                  <CardHeader className="bg-gradient-to-r from-blue-500 to-purple-600 text-white">
                    <CardTitle className="flex items-center gap-2">📊 Top 3 Recommendations</CardTitle>
                  </CardHeader>
                  <CardContent className="pt-6">
                    <div className="space-y-3">
                      {predictionResult.top_recommendations.map((rec, index) => (
                        <div 
                          key={index} 
                          className={`p-4 rounded-lg border-2 transform hover:scale-105 transition-all duration-300 ${
                            index === 0 ? 'glass-card border-green-400 shadow-lg' : 
                            'glass-card border-gray-300'
                          }`}
                        >
                          <div className="flex justify-between items-center mb-2">
                            <span className="text-lg font-semibold flex items-center gap-2">
                              {index === 0 && '🥇'}
                              {index === 1 && '🥈'}
                              {index === 2 && '🥉'}
                              {rec.crop}
                            </span>
                            <span className="text-xl font-bold gradient-text">{rec.confidence}%</span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2.5 overflow-hidden">
                            <div 
                              className="bg-gradient-to-r from-blue-500 to-green-500 h-2.5 rounded-full transition-all duration-1000" 
                              style={{ width: `${rec.confidence}%` }}
                            ></div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>

                {/* Feature Importance - WITH FULL NAMES */}
                <Card className="shadow-2xl border-t-4 border-orange-500 animate-slide-up">
                  <CardHeader className="bg-gradient-to-r from-orange-500 to-red-600 text-white">
                    <CardTitle className="flex items-center gap-2">📈 Feature Importance Analysis</CardTitle>
                    <p className="text-sm text-orange-100 mt-2">Which factors influenced this recommendation</p>
                  </CardHeader>
                  <CardContent className="pt-6">
                    <div className="mb-6 p-4 glass-card rounded-xl border-2 border-orange-300 hover:shadow-lg transition-all duration-300">
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
    </div>
  );
}
