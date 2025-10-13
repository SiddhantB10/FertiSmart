'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Leaf, Brain, TrendingUp, Info, CheckCircle, AlertCircle } from 'lucide-react';
import api from '@/services/api';

interface SoilClimateData {
  N: number;
  P: number;
  K: number;
  temperature: number;
  humidity: number;
  ph: number;
  rainfall: number;
}

interface PredictionResult {
  recommended_crop: string;
  confidence: number;
  top_recommendations: Array<[string, number]>;
  input_analysis: {
    provided_conditions: SoilClimateData;
    condition_assessment: Record<string, string>;
    feature_importance: Record<string, number>;
  };
  recommendation_explanation: {
    crop: string;
    confidence_level: number;
    explanation: string;
    key_factors: string[];
    recommendation_strength: string;
  };
}

interface ModelInfo {
  model_trained: boolean;
  model_info?: {
    algorithm: string;
    available_crops: string[];
    total_crops: number;
    feature_names: string[];
  };
  feature_ranges?: Record<string, { min: number; max: number; mean: number; description: string }>;
  sample_input?: SoilClimateData;
}

const CropRecommendationPage: React.FC = () => {
  const [soilData, setSoilData] = useState<SoilClimateData>({
    N: 90,
    P: 42,
    K: 43,
    temperature: 20.8,
    humidity: 82.0,
    ph: 6.5,
    rainfall: 202.9
  });
  
  const [prediction, setPrediction] = useState<PredictionResult | null>(null);
  const [modelInfo, setModelInfo] = useState<ModelInfo | null>(null);
  const [loading, setLoading] = useState(false);
  const [training, setTraining] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    checkModelStatus();
  }, []);

  const checkModelStatus = async () => {
    try {
      const response = await api.get('/crop-prediction');
      setModelInfo(response.data);
    } catch (err) {
      console.error('Error checking model status:', err);
    }
  };

  const trainModel = async () => {
    setTraining(true);
    setError(null);
    try {
      const response = await api.post('/crop-recommendation');
      setModelInfo({ ...modelInfo, model_trained: true });
      setError(null);
      // Refresh model status
      await checkModelStatus();
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to train model');
    } finally {
      setTraining(false);
    }
  };

  const handleInputChange = (field: keyof SoilClimateData, value: string) => {
    const numValue = parseFloat(value);
    if (!isNaN(numValue)) {
      setSoilData(prev => ({ ...prev, [field]: numValue }));
    }
  };

  const predictCrop = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.post('/crop-prediction', soilData);
      setPrediction(response.data.prediction);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Prediction failed');
      setPrediction(null);
    } finally {
      setLoading(false);
    }
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 80) return 'text-green-600';
    if (confidence >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getStrengthIcon = (strength: string) => {
    switch (strength) {
      case 'High': return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'Medium': return <AlertCircle className="w-5 h-5 text-yellow-500" />;
      case 'Low': return <AlertCircle className="w-5 h-5 text-red-500" />;
      default: return <Info className="w-5 h-5 text-blue-500" />;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Leaf className="w-10 h-10 text-green-600" />
            <h1 className="text-4xl font-bold text-gray-800">Smart Crop Recommendation</h1>
          </div>
          <p className="text-lg text-gray-600">
            AI-powered crop recommendation using Random Forest classification
          </p>
        </div>

        {/* Model Status */}
        {modelInfo && !modelInfo.model_trained && (
          <Card className="mb-6 border-yellow-200 bg-yellow-50">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <Brain className="w-6 h-6 text-yellow-600" />
                  <div>
                    <h3 className="font-semibold text-yellow-800">Model Training Required</h3>
                    <p className="text-yellow-700">The crop recommendation model needs to be trained first.</p>
                  </div>
                </div>
                <Button 
                  onClick={trainModel} 
                  disabled={training}
                  className="bg-yellow-600 hover:bg-yellow-700"
                >
                  {training ? 'Training...' : 'Train Model'}
                </Button>
              </div>
            </CardContent>
          </Card>
        )}

        {error && (
          <Alert className="mb-6 border-red-200 bg-red-50">
            <AlertCircle className="w-4 h-4 text-red-600" />
            <AlertDescription className="text-red-700">{error}</AlertDescription>
          </Alert>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Input Form */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="w-5 h-5 text-blue-600" />
                Soil & Climate Conditions
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {/* Soil Nutrients */}
                <div>
                  <h3 className="font-semibold text-gray-700 mb-3">Soil Nutrients (NPK)</h3>
                  <div className="grid grid-cols-3 gap-4">
                    <div>
                      <Label htmlFor="N">Nitrogen (N)</Label>
                      <Input
                        id="N"
                        type="number"
                        value={soilData.N}
                        onChange={(e) => handleInputChange('N', e.target.value)}
                        placeholder="0-100"
                        min="0"
                        max="100"
                      />
                    </div>
                    <div>
                      <Label htmlFor="P">Phosphorus (P)</Label>
                      <Input
                        id="P"
                        type="number"
                        value={soilData.P}
                        onChange={(e) => handleInputChange('P', e.target.value)}
                        placeholder="0-80"
                        min="0"
                        max="80"
                      />
                    </div>
                    <div>
                      <Label htmlFor="K">Potassium (K)</Label>
                      <Input
                        id="K"
                        type="number"
                        value={soilData.K}
                        onChange={(e) => handleInputChange('K', e.target.value)}
                        placeholder="0-80"
                        min="0"
                        max="80"
                      />
                    </div>
                  </div>
                </div>

                {/* Climate Conditions */}
                <div>
                  <h3 className="font-semibold text-gray-700 mb-3">Climate Conditions</h3>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="temperature">Temperature (°C)</Label>
                      <Input
                        id="temperature"
                        type="number"
                        step="0.1"
                        value={soilData.temperature}
                        onChange={(e) => handleInputChange('temperature', e.target.value)}
                        placeholder="10-40"
                        min="10"
                        max="40"
                      />
                    </div>
                    <div>
                      <Label htmlFor="humidity">Humidity (%)</Label>
                      <Input
                        id="humidity"
                        type="number"
                        step="0.1"
                        value={soilData.humidity}
                        onChange={(e) => handleInputChange('humidity', e.target.value)}
                        placeholder="30-100"
                        min="30"
                        max="100"
                      />
                    </div>
                  </div>
                </div>

                {/* Soil Properties */}
                <div>
                  <h3 className="font-semibold text-gray-700 mb-3">Soil Properties</h3>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="ph">Soil pH</Label>
                      <Input
                        id="ph"
                        type="number"
                        step="0.1"
                        value={soilData.ph}
                        onChange={(e) => handleInputChange('ph', e.target.value)}
                        placeholder="4-9"
                        min="4"
                        max="9"
                      />
                    </div>
                    <div>
                      <Label htmlFor="rainfall">Rainfall (mm)</Label>
                      <Input
                        id="rainfall"
                        type="number"
                        step="0.1"
                        value={soilData.rainfall}
                        onChange={(e) => handleInputChange('rainfall', e.target.value)}
                        placeholder="50-300"
                        min="50"
                        max="300"
                      />
                    </div>
                  </div>
                </div>

                <Button 
                  onClick={predictCrop}
                  disabled={loading || !modelInfo?.model_trained}
                  className="w-full bg-green-600 hover:bg-green-700"
                  size="lg"
                >
                  {loading ? 'Analyzing...' : 'Get Crop Recommendation'}
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Results */}
          <div className="space-y-6">
            {/* Model Information */}
            {modelInfo?.model_trained && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Brain className="w-5 h-5 text-purple-600" />
                    Model Information
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="font-medium">Algorithm:</span>
                      <span>{modelInfo.model_info?.algorithm}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="font-medium">Available Crops:</span>
                      <span>{modelInfo.model_info?.total_crops}</span>
                    </div>
                    <div className="text-sm text-gray-600">
                      <strong>Supported crops:</strong> {modelInfo.model_info?.available_crops?.slice(0, 5).join(', ')}
                      {(modelInfo.model_info?.available_crops?.length || 0) > 5 && '...'}
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Prediction Results */}
            {prediction && (
              <>
                <Card className="border-green-200 bg-green-50">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Leaf className="w-5 h-5 text-green-600" />
                      Recommended Crop
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-center mb-4">
                      <h2 className="text-3xl font-bold text-green-700 capitalize">
                        {prediction.recommended_crop}
                      </h2>
                      <div className="flex items-center justify-center gap-2 mt-2">
                        {getStrengthIcon(prediction.recommendation_explanation.recommendation_strength)}
                        <span className={`text-lg font-semibold ${getConfidenceColor(prediction.confidence)}`}>
                          {prediction.confidence}% Confidence
                        </span>
                      </div>
                    </div>
                    
                    <div className="bg-white rounded-lg p-4">
                      <p className="text-gray-700 mb-3">
                        {prediction.recommendation_explanation.explanation}
                      </p>
                      
                      <div>
                        <h4 className="font-semibold text-gray-800 mb-2">Key Contributing Factors:</h4>
                        <ul className="list-disc list-inside space-y-1 text-sm text-gray-600">
                          {prediction.recommendation_explanation.key_factors.map((factor, index) => (
                            <li key={index}>{factor}</li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* Top Recommendations */}
                <Card>
                  <CardHeader>
                    <CardTitle>Alternative Options</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {prediction.top_recommendations.slice(0, 5).map(([crop, confidence], index) => (
                        <div key={crop} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                          <span className="capitalize font-medium">{crop}</span>
                          <div className="flex items-center gap-2">
                            <div className="w-20 bg-gray-200 rounded-full h-2">
                              <div
                                className={`h-2 rounded-full ${
                                  index === 0 ? 'bg-green-500' : 
                                  index === 1 ? 'bg-blue-500' : 'bg-gray-400'
                                }`}
                                style={{ width: `${confidence}%` }}
                              />
                            </div>
                            <span className="text-sm font-medium">{confidence}%</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>

                {/* Condition Analysis */}
                <Card>
                  <CardHeader>
                    <CardTitle>Soil & Climate Analysis</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {Object.entries(prediction.input_analysis.condition_assessment).map(([key, value]) => (
                        <div key={key} className="p-3 bg-gray-50 rounded-lg">
                          <div className="font-medium capitalize text-gray-800">
                            {key.replace('_', ' ')}
                          </div>
                          <div className="text-sm text-gray-600">{value}</div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default CropRecommendationPage;