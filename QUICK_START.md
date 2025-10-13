# 🚀 Quick Start Guide - FertiSmart Crop Recommendation

## Prerequisites
- Python 3.8+ installed
- Node.js 16+ installed
- Both backend and frontend dependencies installed

## Step 1: Start the Backend ⚙️

Open a terminal and run:

```bash
cd backend
python simple_app.py
```

You should see:
```
✓ Trained new Random Forest model - Accuracy: 99.55%
✓ Total crops supported: 22
============================================================
🌱 FertiSmart - Crop Recommendation System
🤖 Random Forest Classifier
============================================================
 * Running on http://127.0.0.1:5001
```

## Step 2: Start the Frontend 🎨

Open a **NEW** terminal and run:

```bash
cd frontend
npm run dev
```

You should see:
```
  ▲ Next.js 14.x.x
  - Local:        http://localhost:3000
  - Ready in Xs
```

## Step 3: Open in Browser 🌐

Navigate to: **http://localhost:3000**

## Step 4: Make a Prediction 🌾

1. Click "Get Crop Recommendation" on the homepage
2. OR click "Sample" button to load test data
3. OR enter your own values:
   - Nitrogen (N): 90
   - Phosphorus (P): 42
   - Potassium (K): 43
   - Temperature: 20.8°C
   - Humidity: 82%
   - pH: 6.5
   - Rainfall: 202.9mm

4. Click "🚀 Get Recommendation"

5. View your results! 🎉

## Expected Result

You should see:
- **Recommended Crop**: RICE
- **Confidence**: 95%+
- **Top 3 Recommendations** with confidence bars
- **Conditions Analysis**
- **Feature Importance** chart

## Troubleshooting 🔧

### Backend Issues:

**Problem**: `ModuleNotFoundError: No module named 'flask'`  
**Solution**: 
```bash
pip install flask flask-cors scikit-learn pandas numpy joblib
```

**Problem**: `FileNotFoundError: Crop_recommendation.csv`  
**Solution**: Make sure `Crop_recommendation.csv` is in the backend directory

### Frontend Issues:

**Problem**: `Module not found: Can't resolve '@/components/ui/card'`  
**Solution**: The UI components should already be in place. If not, they're in `frontend/src/components/ui/`

**Problem**: Port 3000 already in use  
**Solution**: The app will automatically use port 3001. Check the terminal output.

### API Connection Issues:

**Problem**: "Failed to connect to the server"  
**Solution**: 
1. Make sure backend is running on port 5001
2. Check for CORS errors in browser console
3. Verify both servers are running

## Testing the API Directly 🧪

### Using PowerShell:
```powershell
$body = @{N=90; P=42; K=43; temperature=20.8; humidity=82.0; ph=6.5; rainfall=202.9} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:5001/api/predict" -Method Post -Body $body -ContentType "application/json"
```

### Using curl:
```bash
curl -X POST http://localhost:5001/api/predict \
  -H "Content-Type: application/json" \
  -d '{"N":90,"P":42,"K":43,"temperature":20.8,"humidity":82,"ph":6.5,"rainfall":202.9}'
```

## Success Indicators ✅

1. ✅ Backend shows "Running on http://127.0.0.1:5001"
2. ✅ Frontend shows "Ready in Xs"
3. ✅ Homepage loads with FertiSmart branding
4. ✅ Prediction page has input form
5. ✅ Sample data button works
6. ✅ Prediction returns results
7. ✅ Results show crop name, confidence, and explanations

## Need Help? 🆘

Check these files:
- `RANDOM_FOREST_IMPLEMENTATION.md` - Complete documentation
- Backend logs in the terminal
- Browser console for frontend errors

**You're all set! 🎉 Happy farming! 🌾**
