'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Alert, AlertDescription } from '@/components/ui/alert';

const API_URL = 'http://localhost:5001';

interface ModelInfo {
  accuracy?: number;
  n_crops?: number;
  crops?: string[];
  features?: string[];
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
      // Convert form data to numbers
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
    } catch (err) {
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
    setFormData({
      N: '90',
      P: '42',
      K: '43',
      temperature: '20.8',
      humidity: '82',
      ph: '6.5',
      rainfall: '202.9'
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-blue-50 to-green-100 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            🌾 Smart Crop Recommendation
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Get AI-powered crop recommendations based on your soil and climate conditions
          </p>
          <p className="text-lg text-gray-500 mt-2">
            Using Random Forest Classification Algorithm
          </p>
        </div>

        {/* Model Info Banner */}
        {modelInfo.accuracy && (
          <div className="bg-white rounded-lg shadow-md p-6 mb-8 border-l-4 border-green-500">
            <div className="flex items-center justify-between flex-wrap gap-4">
              <div>
                <h3 className="text-lg font-semibold text-gray-900">Model Information</h3>
                <p className="text-sm text-gray-600">Random Forest Classifier</p>
              </div>
              <div className="flex gap-6">
                <div className="text-center">
                  <div className="text-3xl font-bold text-green-600">{modelInfo.accuracy}%</div>
                  <div className="text-sm text-gray-600">Accuracy</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-blue-600">{modelInfo.n_crops}</div>
                  <div className="text-sm text-gray-600">Crops Supported</div>
                </div>
              </div>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Input Form */}
          <Card className="shadow-xl">
            <CardHeader className="bg-gradient-to-r from-green-600 to-blue-600 text-white">
              <CardTitle className="text-2xl flex items-center gap-2">
                📝 Enter Soil & Climate Data
              </CardTitle>
            </CardHeader>
            <CardContent className="pt-6">
              <form onSubmit={handlePredict} className="space-y-6">
                {/* Soil Nutrients */}
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                    🧪 Soil Nutrients (kg/ha)
                  </h3>
                  <div className="grid grid-cols-3 gap-4">
                    <div>
                      <Label htmlFor="N">Nitrogen (N)</Label>
                      <Input
                        id="N"
                        name="N"
                        type="number"
                        step="0.01"
                        value={formData.N}
                        onChange={handleInputChange}
                        placeholder="0-140"
                        required
                        className="mt-1"
                      />
                    </div>
                    <div>
                      <Label htmlFor="P">Phosphorus (P)</Label>
                      <Input
                        id="P"
                        name="P"
                        type="number"
                        step="0.01"
                        value={formData.P}
                        onChange={handleInputChange}
                        placeholder="5-145"
                        required
                        className="mt-1"
                      />
                    </div>
                    <div>
                      <Label htmlFor="K">Potassium (K)</Label>
                      <Input
                        id="K"
                        name="K"
                        type="number"
                        step="0.01"
                        value={formData.K}
                        onChange={handleInputChange}
                        placeholder="5-205"
                        required
                        className="mt-1"
                      />
                    </div>
                  </div>
                </div>

                {/* Climate Conditions */}
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                    🌤️ Climate Conditions
                  </h3>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="temperature">Temperature (°C)</Label>
                      <Input
                        id="temperature"
                        name="temperature"
                        type="number"
                        step="0.1"
                        value={formData.temperature}
                        onChange={handleInputChange}
                        placeholder="8-44"
                        required
                        className="mt-1"
                      />
                    </div>
                    <div>
                      <Label htmlFor="humidity">Humidity (%)</Label>
                      <Input
                        id="humidity"
                        name="humidity"
                        type="number"
                        step="0.1"
                        value={formData.humidity}
                        onChange={handleInputChange}
                        placeholder="14-100"
                        required
                        className="mt-1"
                      />
                    </div>
                  </div>
                </div>

                {/* Soil & Rainfall */}
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                    🌧️ Soil pH & Rainfall
                  </h3>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="ph">Soil pH</Label>
                      <Input
                        id="ph"
                        name="ph"
                        type="number"
                        step="0.01"
                        value={formData.ph}
                        onChange={handleInputChange}
                        placeholder="3.5-9.9"
                        required
                        className="mt-1"
                      />
                    </div>
                    <div>
                      <Label htmlFor="rainfall">Rainfall (mm)</Label>
                      <Input
                        id="rainfall"
                        name="rainfall"
                        type="number"
                        step="0.1"
                        value={formData.rainfall}
                        onChange={handleInputChange}
                        placeholder="20-300"
                        required
                        className="mt-1"
                      />
                    </div>
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="flex gap-4">
                  <Button
                    type="submit"
                    disabled={loading}
                    className="flex-1 bg-gradient-to-r from-green-600 to-blue-600 hover:from-green-700 hover:to-blue-700 text-white font-semibold py-3"
                  >
                    {loading ? '🔄 Predicting...' : '🚀 Get Recommendation'}
                  </Button>
                  <Button
                    type="button"
                    variant="outline"
                    onClick={loadSampleData}
                    className="px-6"
                  >
                    📋 Sample
                  </Button>
                  <Button
                    type="button"
                    variant="outline"
                    onClick={handleReset}
                    className="px-6"
                  >
                    🔄 Reset
                  </Button>
                </div>
              </form>

              {error && (
                <Alert className="mt-6 bg-red-50 border-red-200">
                  <AlertDescription className="text-red-800">{error}</AlertDescription>
                </Alert>
              )}
            </CardContent>
          </Card>

          {/* Results */}
          <div className="space-y-6">
            {predictionResult ? (
              <>
                {/* Main Recommendation */}
                <Card className="shadow-xl border-2 border-green-500">
                  <CardHeader className="bg-gradient-to-r from-green-500 to-green-600 text-white">
                    <CardTitle className="text-2xl flex items-center gap-2">
                      🎯 Recommended Crop
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="pt-6">
                    <div className="text-center mb-6">
                      <div className="text-6xl font-bold text-green-600 mb-2">
                        {predictionResult.recommended_crop.toUpperCase()}
                      </div>
                      <div className="text-2xl text-gray-600 mb-4">
                        {predictionResult.confidence}% Confidence
                      </div>
                      <div className="inline-block px-4 py-2 bg-green-100 text-green-800 rounded-full font-semibold">
                        {predictionResult.explanation.confidence_level} Confidence Level
                      </div>
                    </div>

                    <div className="bg-blue-50 rounded-lg p-4 mb-4">
                      <p className="text-gray-800 leading-relaxed">
                        {predictionResult.explanation.crop_info}
                      </p>
                    </div>

                    <div className="bg-green-50 rounded-lg p-4">
                      <p className="text-gray-800 font-semibold">
                        {predictionResult.explanation.recommendation}
                      </p>
                    </div>
                  </CardContent>
                </Card>

                {/* Top Recommendations */}
                <Card className="shadow-xl">
                  <CardHeader className="bg-gradient-to-r from-blue-500 to-purple-600 text-white">
                    <CardTitle className="flex items-center gap-2">
                      📊 Top 3 Recommendations
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="pt-6">
                    <div className="space-y-3">
                      {predictionResult.top_recommendations.map((rec, index) => (
                        <div
                          key={index}
                          className={`p-4 rounded-lg border-2 ${
                            index === 0
                              ? 'bg-green-50 border-green-300'
                              : 'bg-gray-50 border-gray-200'
                          }`}
                        >
                          <div className="flex justify-between items-center">
                            <div className="flex items-center gap-3">
                              <span className="text-2xl font-bold text-gray-400">
                                #{index + 1}
                              </span>
                              <span className="text-lg font-semibold text-gray-900">
                                {rec.crop}
                              </span>
                            </div>
                            <div className="text-right">
                              <div className="text-xl font-bold text-blue-600">
                                {rec.confidence}%
                              </div>
                              <div className="text-xs text-gray-500">confidence</div>
                            </div>
                          </div>
                          <div className="mt-2">
                            <div className="w-full bg-gray-200 rounded-full h-2">
                              <div
                                className="bg-gradient-to-r from-blue-500 to-green-500 h-2 rounded-full transition-all duration-500"
                                style={{ width: `${rec.confidence}%` }}
                              ></div>
                            </div>
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
                      <CardTitle className="flex items-center gap-2">
                        🔍 Conditions Analysis
                      </CardTitle>
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

                {/* Feature Importance */}
                <Card className="shadow-xl">
                  <CardHeader className="bg-gradient-to-r from-orange-500 to-red-600 text-white">
                    <CardTitle className="flex items-center gap-2">
                      📈 Feature Importance
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="pt-6">
                    <div className="mb-4 p-3 bg-orange-50 rounded-lg">
                      <p className="text-sm text-gray-700">
                        <strong>Most Important Factor:</strong>{' '}
                        {predictionResult.most_important_factor.feature} (
                        {(predictionResult.most_important_factor.importance * 100).toFixed(1)}%)
                      </p>
                    </div>
                    <div className="space-y-3">
                      {Object.entries(predictionResult.feature_importance)
                        .sort(([, a], [, b]) => b - a)
                        .map(([feature, importance]) => (
                          <div key={feature}>
                            <div className="flex justify-between mb-1">
                              <span className="text-sm font-medium text-gray-700">
                                {feature}
                              </span>
                              <span className="text-sm text-gray-600">
                                {(importance * 100).toFixed(1)}%
                              </span>
                            </div>
                            <div className="w-full bg-gray-200 rounded-full h-2">
                              <div
                                className="bg-gradient-to-r from-orange-400 to-red-500 h-2 rounded-full"
                                style={{ width: `${importance * 100}%` }}
                              ></div>
                            </div>
                          </div>
                        ))}
                    </div>
                  </CardContent>
                </Card>
              </>
            ) : (
              <Card className="shadow-xl">
                <CardContent className="pt-12 pb-12 text-center">
                  <div className="text-6xl mb-4">🌱</div>
                  <h3 className="text-2xl font-semibold text-gray-700 mb-2">
                    Ready to Get Started?
                  </h3>
                  <p className="text-gray-500">
                    Enter your soil and climate conditions to receive crop recommendations
                  </p>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
