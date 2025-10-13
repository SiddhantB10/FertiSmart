"""
FertiSmart - Crop Recommendation System
Random Forest Classifier for Smart Crop Selection
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
from datetime import datetime, timezone
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure CORS for production
frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:3000')
CORS(app, origins=[frontend_url, 'https://*.vercel.app'], supports_credentials=True)

# Global variables for model and scaler
model = None
scaler = None
feature_names = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
model_info = {}

def load_or_train_model():
    """Load existing model or train a new one"""
    global model, scaler, model_info
    
    model_path = 'crop_model.pkl'
    scaler_path = 'crop_scaler.pkl'
    
    # Try to load existing model
    if os.path.exists(model_path) and os.path.exists(scaler_path):
        try:
            model = joblib.load(model_path)
            scaler = joblib.load(scaler_path)
            print("✓ Loaded existing Random Forest model")
            return True
        except:
            print("! Failed to load existing model, will train new one")
    
    # Train new model
    try:
        # Load dataset
        df = pd.read_csv('Crop_recommendation.csv')
        
        # Prepare features and labels
        X = df[feature_names]
        y = df['label']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train Random Forest
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        
        model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        
        # Save model
        joblib.dump(model, model_path)
        joblib.dump(scaler, scaler_path)
        
        # Store model info
        model_info = {
            'accuracy': round(accuracy * 100, 2),
            'total_samples': len(df),
            'train_samples': len(X_train),
            'test_samples': len(X_test),
            'n_crops': len(df['label'].unique()),
            'crops': sorted(df['label'].unique().tolist()),
            'trained_at': datetime.now(timezone.utc).isoformat()
        }
        
        print(f"✓ Trained new Random Forest model - Accuracy: {accuracy*100:.2f}%")
        print(f"✓ Total crops supported: {model_info['n_crops']}")
        return True
        
    except Exception as e:
        print(f"✗ Error training model: {str(e)}")
        return False

# Initialize model on startup
load_or_train_model()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'FertiSmart Crop Recommendation',
        'model': 'Random Forest Classifier',
        'model_loaded': model is not None,
        'timestamp': datetime.now(timezone.utc).isoformat()
    })

@app.route('/api/model/info', methods=['GET'])
def get_model_info():
    """Get model information"""
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    return jsonify({
        'success': True,
        'model_type': 'Random Forest Classifier',
        'algorithm': 'Ensemble Learning - Random Forest',
        'purpose': 'Crop Recommendation based on Soil & Climate Conditions',
        'features': feature_names,
        'feature_descriptions': {
            'N': 'Nitrogen content ratio in soil (kg/ha)',
            'P': 'Phosphorus content ratio in soil (kg/ha)',
            'K': 'Potassium content ratio in soil (kg/ha)',
            'temperature': 'Temperature in Celsius',
            'humidity': 'Relative humidity in %',
            'ph': 'pH value of the soil',
            'rainfall': 'Rainfall in mm'
        },
        **model_info
    })

@app.route('/api/model/train', methods=['POST'])
def train_model():
    """Train or retrain the model"""
    success = load_or_train_model()
    
    if success:
        return jsonify({
            'success': True,
            'message': 'Model trained successfully',
            **model_info
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Failed to train model'
        }), 500

@app.route('/api/predict', methods=['POST'])
def predict_crop():
    """Predict the best crop for given conditions"""
    try:
        if model is None or scaler is None:
            return jsonify({'error': 'Model not loaded. Please train the model first.'}), 500
        
        # Get input data
        data = request.get_json()
        
        # Validate input
        for feature in feature_names:
            if feature not in data:
                return jsonify({'error': f'Missing required field: {feature}'}), 400
        
        # Prepare input as DataFrame to preserve feature names
        input_df = pd.DataFrame([[
            float(data['N']),
            float(data['P']),
            float(data['K']),
            float(data['temperature']),
            float(data['humidity']),
            float(data['ph']),
            float(data['rainfall'])
        ]], columns=feature_names)
        
        # Scale and predict
        input_scaled = scaler.transform(input_df)
        prediction = model.predict(input_scaled)[0]
        probabilities = model.predict_proba(input_scaled)[0]
        
        # Get top 3 recommendations
        classes = model.classes_
        top_indices = np.argsort(probabilities)[-3:][::-1]
        recommendations = [
            {
                'crop': str(classes[i]),
                'confidence': round(float(probabilities[i] * 100), 2),
                'suitable': bool(probabilities[i] > 0.15)
            }
            for i in top_indices
        ]
        
        # Feature importance
        feature_importance = dict(zip(feature_names, model.feature_importances_))
        most_important = max(feature_importance.items(), key=lambda x: x[1])
        
        # Generate explanation
        explanation = generate_explanation(prediction, data, probabilities[top_indices[0]])
        
        return jsonify({
            'success': True,
            'recommended_crop': str(prediction),
            'confidence': round(float(probabilities[top_indices[0]] * 100), 2),
            'top_recommendations': recommendations,
            'input_conditions': data,
            'feature_importance': {k: round(v, 4) for k, v in feature_importance.items()},
            'most_important_factor': {
                'feature': most_important[0],
                'importance': round(most_important[1], 4)
            },
            'explanation': explanation,
            'timestamp': datetime.now(timezone.utc).isoformat()
        })
        
    except ValueError as e:
        return jsonify({'error': f'Invalid input values: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500

def generate_explanation(crop, conditions, confidence):
    """Generate human-readable explanation"""
    explanations = {
        'rice': 'Rice thrives in high humidity and adequate rainfall with moderate NPK levels. Best grown in flooded fields.',
        'wheat': 'Wheat grows well in moderate temperatures with balanced soil nutrients. Requires well-drained soil.',
        'maize': 'Maize (corn) requires warm temperatures and moderate to high nitrogen levels. Needs good drainage.',
        'cotton': 'Cotton needs warm temperatures, moderate rainfall, and well-drained soil. Requires careful irrigation.',
        'sugarcane': 'Sugarcane thrives in high temperatures, humidity, and rich soil conditions. Needs consistent moisture.',
        'coffee': 'Coffee requires moderate temperatures, high humidity, and acidic to neutral soil. Shade-tolerant crop.',
        'banana': 'Bananas need warm temperatures, high humidity, and potassium-rich soil. Requires year-round warmth.',
        'grapes': 'Grapes prefer moderate temperatures, low to moderate rainfall, and well-drained soil. Needs dry climate.',
        'apple': 'Apples grow best in cool to moderate temperatures with balanced soil nutrients. Needs winter chill.',
        'orange': 'Oranges require warm temperatures, moderate humidity, and slightly acidic soil. Frost-sensitive.',
        'coconut': 'Coconut palms need warm temperatures, high humidity, and sandy soil. Grows well in coastal areas.',
        'jute': 'Jute requires warm, humid climate with plenty of rainfall. Grows well in alluvial soil.',
        'mango': 'Mangoes need warm to hot temperatures with moderate rainfall. Prefers well-drained sandy loam.',
        'papaya': 'Papaya requires warm temperatures, good drainage, and rich organic soil. Fast-growing fruit tree.',
        'pomegranate': 'Pomegranate thrives in hot, dry climates with good drainage. Drought-tolerant once established.'
    }
    
    base_explanation = explanations.get(crop, f'{crop} is suitable for the provided conditions.')
    
    # Analyze conditions
    conditions_analysis = []
    
    if conditions['temperature'] > 30:
        conditions_analysis.append('High temperature favors warm-season crops')
    elif conditions['temperature'] < 15:
        conditions_analysis.append('Cool temperature suits cold-season crops')
    
    if conditions['humidity'] > 80:
        conditions_analysis.append('High humidity suitable for moisture-loving crops')
    elif conditions['humidity'] < 50:
        conditions_analysis.append('Low humidity requires drought-tolerant crops')
    
    if conditions['rainfall'] > 200:
        conditions_analysis.append('High rainfall supports water-intensive crops')
    elif conditions['rainfall'] < 100:
        conditions_analysis.append('Low rainfall requires drought-resistant crops')
    
    if conditions['ph'] < 6:
        conditions_analysis.append('Acidic soil - some crops may need pH adjustment')
    elif conditions['ph'] > 8:
        conditions_analysis.append('Alkaline soil - may need pH correction')
    
    return {
        'crop_info': base_explanation,
        'conditions_analysis': conditions_analysis,
        'confidence_level': 'High' if confidence > 0.7 else 'Medium' if confidence > 0.4 else 'Moderate',
        'recommendation': f'Based on your soil and climate conditions, {crop} is the most suitable crop with {round(confidence*100, 1)}% confidence.'
    }

@app.route('/api/crops', methods=['GET'])
def get_all_crops():
    """Get list of all supported crops"""
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    crops = sorted(model.classes_.tolist())
    
    return jsonify({
        'success': True,
        'total_crops': len(crops),
        'crops': crops
    })

if __name__ == '__main__':
    print("=" * 60)
    print("🌱 FertiSmart - Crop Recommendation System")
    print("🤖 Random Forest Classifier")
    print("=" * 60)
    
    print("🔄 Initializing system...")
    if load_or_train_model():
        print("✅ System ready!")
        print(f"📊 Model accuracy: {model_info.get('accuracy', 'N/A')}%")
        print(f"🌾 Crops supported: {model_info.get('n_crops', 'N/A')}")
        print("🚀 Starting Flask server...")
        print("=" * 60)
        
        # Use PORT from environment (Railway sets this) or default to 5001
        port = int(os.getenv('PORT', 5001))
        debug = os.getenv('FLASK_ENV', 'development') == 'development'
        app.run(debug=debug, host='0.0.0.0', port=port)
    else:
        print("❌ Failed to initialize system")
        print("Please check your data files and try again.")
