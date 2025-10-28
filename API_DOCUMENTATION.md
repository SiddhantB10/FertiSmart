# 📡 FertiSmart API Documentation

Complete API reference for the FertiSmart Crop Recommendation System backend.

## Base URL

**Production**: `https://fertismart-backend.onrender.com`  
**Development**: `http://localhost:5001`

## Authentication

Currently, the API is open and does not require authentication. All endpoints are publicly accessible.

## Response Format

All API responses follow this standard JSON format:

### Success Response
```json
{
  "success": true,
  "data": { /* response data */ },
  "timestamp": "2025-10-28T12:00:00Z"
}
```

### Error Response
```json
{
  "success": false,
  "error": "Error message description",
  "timestamp": "2025-10-28T12:00:00Z"
}
```

## Endpoints

### 1. Health Check

Check if the API server is running and healthy.

**Endpoint**: `GET /api/health`

**Response**:
```json
{
  "status": "healthy",
  "service": "FertiSmart Crop Recommendation",
  "model_loaded": true,
  "model": "Random Forest Classifier",
  "timestamp": "2025-10-28T12:00:00.000Z"
}
```

**Status Codes**:
- `200 OK`: Service is healthy
- `503 Service Unavailable`: Service is down

**Example**:
```bash
curl https://fertismart-backend.onrender.com/api/health
```

---

### 2. Model Information

Get detailed information about the ML model.

**Endpoint**: `GET /api/model/info`

**Response**:
```json
{
  "success": true,
  "model_type": "Random Forest Classifier",
  "algorithm": "Ensemble Learning - Random Forest",
  "features": ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"],
  "feature_descriptions": {
    "N": "Nitrogen content ratio in soil (kg/ha)",
    "P": "Phosphorus content ratio in soil (kg/ha)",
    "K": "Potassium content ratio in soil (kg/ha)",
    "temperature": "Temperature in Celsius",
    "humidity": "Relative humidity in %",
    "ph": "pH value of the soil",
    "rainfall": "Rainfall in mm"
  },
  "purpose": "Crop Recommendation based on Soil & Climate Conditions"
}
```

**Status Codes**:
- `200 OK`: Successfully retrieved model info

**Example**:
```bash
curl https://fertismart-backend.onrender.com/api/model/info
```

---

### 3. Crop Prediction

Get crop recommendation based on soil and climate parameters.

**Endpoint**: `POST /api/predict`

**Request Headers**:
```
Content-Type: application/json
```

**Request Body**:
```json
{
  "N": 90,
  "P": 42,
  "K": 43,
  "temperature": 20.87,
  "humidity": 82.00,
  "ph": 6.50,
  "rainfall": 202.93
}
```

**Parameters**:

| Parameter | Type | Required | Range | Description |
|-----------|------|----------|-------|-------------|
| N | float | Yes | 0-140 | Nitrogen content in soil (kg/ha) |
| P | float | Yes | 5-145 | Phosphorus content in soil (kg/ha) |
| K | float | Yes | 5-205 | Potassium content in soil (kg/ha) |
| temperature | float | Yes | 8-44 | Temperature in Celsius |
| humidity | float | Yes | 14-100 | Relative humidity (%) |
| ph | float | Yes | 3.5-9.9 | Soil pH level |
| rainfall | float | Yes | 20-300 | Rainfall in mm |

**Response**:
```json
{
  "success": true,
  "recommended_crop": "rice",
  "confidence": 0.95,
  "top_recommendations": [
    {
      "crop": "rice",
      "confidence": 0.95,
      "suitable": true
    },
    {
      "crop": "cotton",
      "confidence": 0.03,
      "suitable": false
    },
    {
      "crop": "jute",
      "confidence": 0.02,
      "suitable": false
    }
  ],
  "explanation": {
    "crop_info": "Rice (Oryza sativa) is a staple cereal crop...",
    "conditions_analysis": [
      "High humidity (82.0%) - Excellent for rice cultivation",
      "Moderate to high rainfall (202.9mm) - Ideal for rice growth",
      "Slightly acidic to neutral pH (6.5) - Perfect for rice"
    ],
    "confidence_level": "EXCELLENT - 95.0% confidence",
    "recommendation": "✅ HIGHLY RECOMMENDED: All conditions are optimal for rice cultivation"
  },
  "feature_importance": {
    "N": 0.15,
    "P": 0.12,
    "K": 0.14,
    "temperature": 0.18,
    "humidity": 0.16,
    "ph": 0.13,
    "rainfall": 0.12
  },
  "most_important_factor": {
    "feature": "temperature",
    "importance": 0.18
  },
  "timestamp": "2025-10-28T12:00:00.000Z"
}
```

**Status Codes**:
- `200 OK`: Successful prediction
- `400 Bad Request`: Invalid input parameters
- `500 Internal Server Error`: Server error

**Example**:
```bash
curl -X POST https://fertismart-backend.onrender.com/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "N": 90,
    "P": 42,
    "K": 43,
    "temperature": 20.87,
    "humidity": 82.00,
    "ph": 6.50,
    "rainfall": 202.93
  }'
```

**JavaScript Example**:
```javascript
const response = await fetch('https://fertismart-backend.onrender.com/api/predict', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    N: 90,
    P: 42,
    K: 43,
    temperature: 20.87,
    humidity: 82.00,
    ph: 6.50,
    rainfall: 202.93
  })
});

const data = await response.json();
console.log(data.recommended_crop); // "rice"
```

**Python Example**:
```python
import requests

url = "https://fertismart-backend.onrender.com/api/predict"
payload = {
    "N": 90,
    "P": 42,
    "K": 43,
    "temperature": 20.87,
    "humidity": 82.00,
    "ph": 6.50,
    "rainfall": 202.93
}

response = requests.post(url, json=payload)
data = response.json()
print(data['recommended_crop'])  # "rice"
```

---

### 4. Supported Crops

Get list of all crops supported by the model.

**Endpoint**: `GET /api/crops`

**Response**:
```json
{
  "success": true,
  "crops": [
    "rice", "maize", "wheat", "barley", "sorghum", "millet",
    "chickpea", "kidneybeans", "pigeonpeas", "mothbeans", "mungbean", 
    "blackgram", "lentil", "cotton", "jute", "sugarcane", "tobacco",
    "banana", "mango", "grapes", "watermelon", "muskmelon", "apple",
    "orange", "papaya", "coconut", "coffee", "pomegranate", "tomato",
    "potato", "onion", "cabbage", "carrot", "cucumber", "spinach",
    "lettuce", "broccoli"
  ],
  "total_crops": 37
}
```

**Status Codes**:
- `200 OK`: Successfully retrieved crop list

**Example**:
```bash
curl https://fertismart-backend.onrender.com/api/crops
```

---

## Error Handling

### Error Codes

| Status Code | Meaning | Description |
|-------------|---------|-------------|
| 400 | Bad Request | Invalid input parameters |
| 404 | Not Found | Endpoint not found |
| 500 | Internal Server Error | Server-side error |
| 503 | Service Unavailable | Service temporarily unavailable |

### Error Response Example

```json
{
  "success": false,
  "error": "Missing required parameter: N",
  "timestamp": "2025-10-28T12:00:00.000Z"
}
```

---

## Rate Limiting

**Current**: No rate limiting implemented  
**Recommendation**: Implement rate limiting for production use

---

## CORS

Cross-Origin Resource Sharing (CORS) is enabled for all origins:
```python
CORS(app, origins="*")
```

Allowed methods: `GET`, `POST`, `PUT`, `DELETE`, `OPTIONS`

---

## Data Types & Validation

### Input Validation

All numeric inputs must be:
- Valid numbers (float or int)
- Within specified ranges
- Non-null/non-empty

### Type Conversion

The API automatically converts string numbers to floats:
```json
{
  "N": "90",      // Converted to 90.0
  "P": 42         // Remains 42.0
}
```

---

## Best Practices

### 1. Input Validation
Always validate user input on the client side before sending to API.

### 2. Error Handling
```javascript
try {
  const response = await fetch(API_URL + '/api/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  
  const result = await response.json();
  return result;
} catch (error) {
  console.error('API Error:', error);
  // Handle error appropriately
}
```

### 3. Timeout Handling
Set appropriate timeouts for requests:
```javascript
const controller = new AbortController();
const timeoutId = setTimeout(() => controller.abort(), 30000);

const response = await fetch(url, {
  signal: controller.signal
});
```

### 4. Retry Logic
Implement retry logic for failed requests (especially on first load).

---

## Performance Considerations

### Cold Start (Render Free Tier)
- First request after 15 min inactivity: 30-60 seconds
- Subsequent requests: < 1 second
- Solution: Implement warming strategy on frontend

### Model Loading
- Model is loaded once on server startup
- All predictions use the same loaded model
- No model loading delay per request

---

## Sample Test Data

### Rice-Friendly Conditions
```json
{
  "N": 90, "P": 42, "K": 43,
  "temperature": 20.87, "humidity": 82.00,
  "ph": 6.50, "rainfall": 202.93
}
```

### Cotton-Friendly Conditions
```json
{
  "N": 120, "P": 50, "K": 50,
  "temperature": 25.5, "humidity": 70.0,
  "ph": 6.8, "rainfall": 100.0
}
```

### Apple-Friendly Conditions
```json
{
  "N": 70, "P": 60, "K": 100,
  "temperature": 18.0, "humidity": 70.0,
  "ph": 6.0, "rainfall": 120.0
}
```

---

## Changelog

### Version 1.0.0 (October 28, 2025)
- Initial API release
- 37 crop support
- Random Forest model with 97.32% accuracy
- Real-time prediction endpoint
- Health check and model info endpoints

---

## Support

For API issues or questions:
- GitHub Issues: `https://github.com/SiddhantB10/FertiSmart/issues`
- Check deployment status: `/api/health`

---

**Last Updated**: October 28, 2025  
**API Version**: 1.0.0

<div align="center">
  <strong>🌾 FertiSmart API - Powered by Machine Learning 🌾</strong>
</div>
