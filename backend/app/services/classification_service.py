"""
Classification Service for FertiSmart
Implements Random Forest classification for Crop Recommendation
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import os
from datetime import datetime

class ClassificationService:
    """Random Forest Classification Service for Crop Recommendation"""
    
    def __init__(self):
        self.model = None
        self.scaler = None
    
    def train_crop_recommendation_model(self):
        """Train Random Forest model specifically for crop recommendation using the CSV data"""
        try:
            # Load the crop recommendation dataset
            csv_path = 'Crop_recommendation.csv'
            if not os.path.exists(csv_path):
                raise FileNotFoundError("Crop_recommendation.csv not found in project root")
            
            # Load and prepare the data
            df = pd.read_csv(csv_path)
            
            # Features (soil and climate conditions)
            feature_columns = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
            X = df[feature_columns]
            y = df['label']  # Crop labels
            
            # Split the data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
            
            # Scale the features
            self.scaler = StandardScaler()
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Train Random Forest model
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=15,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1
            )
            
            self.model.fit(X_train_scaled, y_train)
            
            # Make predictions
            y_pred = self.model.predict(X_test_scaled)
            y_pred_proba = self.model.predict_proba(X_test_scaled)
            
            # Calculate metrics
            metrics = self._calculate_metrics(y_test, y_pred)
            
            # Cross-validation
            cv_scores = cross_val_score(self.model, X_train_scaled, y_train, cv=5)
            
            # Save model and scaler
            os.makedirs('trained_models', exist_ok=True)
            
            model_path = os.path.join('trained_models', 'crop_recommendation_rf.pkl')
            scaler_path = os.path.join('trained_models', 'crop_recommendation_scaler.pkl')
            
            joblib.dump(self.model, model_path)
            joblib.dump(self.scaler, scaler_path)
            
            # Get unique crops and their counts
            crop_info = {
                'total_crops': len(df['label'].unique()),
                'crops': df['label'].unique().tolist(),
                'crop_distribution': df['label'].value_counts().to_dict()
            }
            
            # Prepare detailed results
            result = {
                'model_type': 'Random Forest',
                'purpose': 'Crop Recommendation',
                'dataset_info': {
                    'total_samples': len(df),
                    'features': feature_columns,
                    'training_samples': len(X_train),
                    'test_samples': len(X_test)
                },
                'crop_info': crop_info,
                'model_parameters': {
                    'n_estimators': 100,
                    'max_depth': 15,
                    'min_samples_split': 5,
                    'min_samples_leaf': 2,
                    'random_state': 42
                },
                'performance_metrics': metrics,
                'cross_validation': {
                    'cv_scores': cv_scores.tolist(),
                    'mean_cv_score': round(cv_scores.mean(), 4),
                    'std_cv_score': round(cv_scores.std(), 4)
                },
                'feature_importance': self._get_feature_importance(self.model, feature_columns),
                'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
                'classification_report': classification_report(y_test, y_pred, output_dict=True),
                'model_paths': {
                    'model': model_path,
                    'scaler': scaler_path
                },
                'sample_predictions': self._get_sample_predictions(self.model, self.scaler, X_test, y_test, y_pred, y_pred_proba),
                'training_timestamp': datetime.utcnow().isoformat()
            }
            
            return result
            
        except Exception as e:
            raise Exception(f"Crop recommendation model training failed: {str(e)}")
    
    def predict_crop(self, soil_climate_data):
        """Predict the most suitable crop based on soil and climate conditions"""
        try:
            # Load the trained model and scaler if not already loaded
            if self.model is None or self.scaler is None:
                model_path = os.path.join('trained_models', 'crop_recommendation_rf.pkl')
                scaler_path = os.path.join('trained_models', 'crop_recommendation_scaler.pkl')
                
                if not os.path.exists(model_path) or not os.path.exists(scaler_path):
                    raise FileNotFoundError("Trained crop recommendation model not found. Please train the model first.")
                
                self.model = joblib.load(model_path)
                self.scaler = joblib.load(scaler_path)
            
            # Validate input data
            required_features = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
            for feature in required_features:
                if feature not in soil_climate_data:
                    raise ValueError(f"Missing required feature: {feature}")
            
            # Prepare input data
            input_data = np.array([[
                float(soil_climate_data['N']),
                float(soil_climate_data['P']),
                float(soil_climate_data['K']),
                float(soil_climate_data['temperature']),
                float(soil_climate_data['humidity']),
                float(soil_climate_data['ph']),
                float(soil_climate_data['rainfall'])
            ]])
            
            # Scale the input data
            input_scaled = self.scaler.transform(input_data)
            
            # Make prediction
            prediction = self.model.predict(input_scaled)[0]
            prediction_proba = self.model.predict_proba(input_scaled)[0]
            
            # Get top 3 crop recommendations with confidence scores
            class_names = self.model.classes_
            confidence_scores = [(class_names[i], round(prob * 100, 2)) 
                               for i, prob in enumerate(prediction_proba)]
            confidence_scores.sort(key=lambda x: x[1], reverse=True)
            
            # Get feature importance for this prediction
            feature_importance = dict(zip(required_features, self.model.feature_importances_))
            
            # Analyze input conditions
            condition_analysis = self._analyze_input_conditions(soil_climate_data)
            
            result = {
                'recommended_crop': prediction,
                'confidence': round(max(prediction_proba) * 100, 2),
                'top_recommendations': confidence_scores[:3],
                'all_probabilities': confidence_scores,
                'input_analysis': {
                    'provided_conditions': soil_climate_data,
                    'condition_assessment': condition_analysis,
                    'feature_importance': {k: round(v, 4) for k, v in feature_importance.items()}
                },
                'recommendation_explanation': self._generate_crop_explanation(
                    prediction, soil_climate_data, confidence_scores[0][1]
                ),
                'timestamp': datetime.utcnow().isoformat()
            }
            
            return result
            
        except Exception as e:
            raise Exception(f"Crop prediction failed: {str(e)}")
    
    def _calculate_metrics(self, y_true, y_pred):
        """Calculate classification metrics"""
        return {
            'accuracy': round(accuracy_score(y_true, y_pred), 4),
            'precision': round(precision_score(y_true, y_pred, average='weighted'), 4),
            'recall': round(recall_score(y_true, y_pred, average='weighted'), 4),
            'f1_score': round(f1_score(y_true, y_pred, average='weighted'), 4)
        }
    
    def _get_feature_importance(self, model, feature_names):
        """Get feature importance from the model"""
        if hasattr(model, 'feature_importances_'):
            importance = model.feature_importances_
            return {feature: round(importance[i], 4) for i, feature in enumerate(feature_names)}
        return {}
    
    def _get_sample_predictions(self, model, scaler, X_test, y_test, y_pred, y_pred_proba, sample_size=5):
        """Get sample predictions for demonstration"""
        samples = []
        indices = np.random.choice(len(X_test), min(sample_size, len(X_test)), replace=False)
        
        for i in indices:
            sample = {
                'input_conditions': X_test.iloc[i].to_dict(),
                'actual_crop': y_test.iloc[i],
                'predicted_crop': y_pred[i],
                'confidence': round(max(y_pred_proba[i]) * 100, 2),
                'correct_prediction': y_test.iloc[i] == y_pred[i]
            }
            samples.append(sample)
        
        return samples
    
    def _analyze_input_conditions(self, conditions):
        """Analyze the input soil and climate conditions"""
        analysis = {}
        
        # Nutrient analysis
        n_level = conditions['N']
        p_level = conditions['P']
        k_level = conditions['K']
        
        if n_level < 30:
            analysis['nitrogen'] = "Low - May need nitrogen-rich fertilizer"
        elif n_level > 70:
            analysis['nitrogen'] = "High - Good for leafy crops"
        else:
            analysis['nitrogen'] = "Moderate - Suitable for most crops"
        
        if p_level < 20:
            analysis['phosphorus'] = "Low - May need phosphorus supplement"
        elif p_level > 60:
            analysis['phosphorus'] = "High - Good for root development"
        else:
            analysis['phosphorus'] = "Moderate - Adequate for most crops"
        
        if k_level < 20:
            analysis['potassium'] = "Low - May need potassium supplement"
        elif k_level > 60:
            analysis['potassium'] = "High - Good for fruit/flower development"
        else:
            analysis['potassium'] = "Moderate - Adequate for most crops"
        
        # Climate analysis
        temp = conditions['temperature']
        humidity = conditions['humidity']
        rainfall = conditions['rainfall']
        ph = conditions['ph']
        
        if temp < 15:
            analysis['temperature'] = "Cold - Suitable for cool-season crops"
        elif temp > 30:
            analysis['temperature'] = "Hot - Suitable for warm-season crops"
        else:
            analysis['temperature'] = "Moderate - Suitable for most crops"
        
        if humidity < 50:
            analysis['humidity'] = "Low - May need irrigation support"
        elif humidity > 85:
            analysis['humidity'] = "High - Good moisture availability"
        else:
            analysis['humidity'] = "Moderate - Adequate moisture"
        
        if rainfall < 100:
            analysis['rainfall'] = "Low - Drought-tolerant crops recommended"
        elif rainfall > 250:
            analysis['rainfall'] = "High - Water-loving crops suitable"
        else:
            analysis['rainfall'] = "Moderate - Suitable for most crops"
        
        if ph < 6:
            analysis['soil_ph'] = "Acidic - Some crops may need pH adjustment"
        elif ph > 8:
            analysis['soil_ph'] = "Alkaline - May need pH adjustment"
        else:
            analysis['soil_ph'] = "Neutral - Optimal for most crops"
        
        return analysis
    
    def _generate_crop_explanation(self, predicted_crop, conditions, confidence):
        """Generate explanation for the crop recommendation"""
        explanations = {
            'rice': "Rice thrives in high humidity and adequate rainfall with moderate NPK levels.",
            'wheat': "Wheat grows well in moderate temperatures with balanced soil nutrients.",
            'maize': "Maize (corn) requires warm temperatures and moderate to high nitrogen levels.",
            'cotton': "Cotton needs warm temperatures, moderate rainfall, and well-drained soil.",
            'sugarcane': "Sugarcane thrives in high temperatures, humidity, and rich soil conditions.",
            'coffee': "Coffee requires moderate temperatures, high humidity, and acidic to neutral soil.",
            'banana': "Bananas need warm temperatures, high humidity, and potassium-rich soil.",
            'grapes': "Grapes prefer moderate temperatures, low to moderate rainfall, and well-drained soil.",
            'apple': "Apples grow best in cool to moderate temperatures with balanced soil nutrients.",
            'orange': "Oranges require warm temperatures, moderate humidity, and slightly acidic soil."
        }
        
        base_explanation = explanations.get(
            predicted_crop, 
            f"{predicted_crop} is recommended based on the provided soil and climate conditions."
        )
        
        return {
            'crop': predicted_crop,
            'confidence_level': confidence,
            'explanation': base_explanation,
            'key_factors': self._identify_key_factors(predicted_crop, conditions),
            'recommendation_strength': 'High' if confidence > 80 else 'Medium' if confidence > 60 else 'Low'
        }
    
    def _identify_key_factors(self, crop, conditions):
        """Identify key factors that influenced the crop recommendation"""
        factors = []
        
        # This is a simplified version - in practice, you'd use feature importance
        # and domain knowledge to identify the most influential factors
        
        temp = conditions['temperature']
        humidity = conditions['humidity']
        rainfall = conditions['rainfall']
        n = conditions['N']
        ph = conditions['ph']
        
        if crop in ['rice', 'sugarcane'] and humidity > 80:
            factors.append("High humidity favorable for water-loving crops")
        
        if crop in ['wheat', 'barley'] and 15 <= temp <= 25:
            factors.append("Moderate temperature ideal for cool-season grains")
        
        if crop in ['cotton', 'maize'] and temp > 25:
            factors.append("Warm temperature suitable for heat-loving crops")
        
        if crop in ['banana', 'coconut'] and n > 50:
            factors.append("High nitrogen content supports leafy growth")
        
        if crop in ['apple', 'grapes'] and 6 <= ph <= 7:
            factors.append("Neutral pH optimal for fruit crops")
        
        return factors if factors else ["All conditions within suitable range for this crop"]