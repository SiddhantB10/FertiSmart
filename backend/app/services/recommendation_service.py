"""
Recommendation Service for FertiSmart
Smart fertilizer recommendation engine based on soil analysis
"""

import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime

from app.services.classification_service import ClassificationService
from app.services.preprocessing_service import PreprocessingService
from app.models.database_models import FertilizerDim, CropDim, SoilTestFact

class RecommendationService:
    """Smart fertilizer recommendation engine"""
    
    def __init__(self):
        self.classification_service = ClassificationService()
        self.preprocessing_service = PreprocessingService()
        self.fertilizer_knowledge_base = self._build_fertilizer_knowledge_base()
    
    def get_recommendations(self, soil_data):
        """Get comprehensive fertilizer recommendations"""
        try:
            # Validate and preprocess input
            processed_data = self._preprocess_input(soil_data)
            
            # Get ML predictions
            ml_recommendations = self._get_ml_recommendations(processed_data)
            
            # Get rule-based recommendations
            rule_based_recommendations = self._get_rule_based_recommendations(soil_data)
            
            # Combine and rank recommendations
            final_recommendations = self._combine_recommendations(
                ml_recommendations, 
                rule_based_recommendations,
                soil_data
            )
            
            # Add detailed explanations
            detailed_recommendations = self._add_explanations(final_recommendations, soil_data)
            
            return {
                'soil_analysis': self._analyze_soil_condition(soil_data),
                'recommendations': detailed_recommendations,
                'application_guidelines': self._get_application_guidelines(final_recommendations),
                'expected_outcomes': self._predict_outcomes(final_recommendations, soil_data),
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            raise Exception(f"Recommendation generation failed: {str(e)}")
    
    def _preprocess_input(self, soil_data):
        """Preprocess input soil data for ML models"""
        try:
            # Convert to the format expected by ML models
            feature_names = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
            
            # Create feature vector
            features = []
            for feature in feature_names:
                if feature in soil_data:
                    features.append(float(soil_data[feature]))
                else:
                    raise ValueError(f"Missing required feature: {feature}")
            
            # Load the scaler if available
            scaler_path = os.path.join('trained_models', 'feature_scaler.pkl')
            if os.path.exists(scaler_path):
                scaler = joblib.load(scaler_path)
                scaled_features = scaler.transform([features])
                return scaled_features[0]
            else:
                # Use simple normalization if scaler not available
                return self._simple_normalize(features)
                
        except Exception as e:
            raise Exception(f"Input preprocessing failed: {str(e)}")
    
    def _simple_normalize(self, features):
        """Simple feature normalization"""
        # Typical ranges for normalization
        ranges = {
            'N': (0, 100),      # Nitrogen
            'P': (0, 80),       # Phosphorus
            'K': (0, 80),       # Potassium
            'temperature': (10, 40),  # Temperature
            'humidity': (30, 100),    # Humidity
            'ph': (4, 9),       # pH
            'rainfall': (50, 300)     # Rainfall
        }
        
        normalized = []
        for i, value in enumerate(features):
            feature_name = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall'][i]
            min_val, max_val = ranges[feature_name]
            normalized_value = (value - min_val) / (max_val - min_val)
            normalized.append(max(0, min(1, normalized_value)))  # Clip to [0,1]
        
        return normalized
    
    def _get_ml_recommendations(self, processed_features):
        """Get recommendations from trained ML models"""
        recommendations = []
        
        try:
            # Try to use trained crop prediction model
            crop_models = ['decision_tree_crop', 'naive_bayes_crop']
            
            for model_name in crop_models:
                model_path = os.path.join('trained_models', f'{model_name}.pkl')
                
                if os.path.exists(model_path):
                    model = joblib.load(model_path)
                    prediction = model.predict([processed_features])
                    
                    # Get confidence if available
                    confidence = 0.8  # Default confidence
                    if hasattr(model, 'predict_proba'):
                        proba = model.predict_proba([processed_features])
                        confidence = np.max(proba[0])
                    
                    # Map prediction to crop/fertilizer
                    crop_fertilizer = self._decode_prediction(prediction[0])
                    
                    recommendations.append({
                        'source': 'ml_model',
                        'model': model_name,
                        'crop': crop_fertilizer['crop'],
                        'fertilizer': crop_fertilizer['fertilizer'],
                        'confidence': confidence,
                        'prediction_value': int(prediction[0])
                    })
        
        except Exception as e:
            print(f"ML recommendation failed: {str(e)}")
        
        return recommendations
    
    def _get_rule_based_recommendations(self, soil_data):
        """Get recommendations based on agronomic rules"""
        recommendations = []
        
        try:
            N = float(soil_data['N'])
            P = float(soil_data['P'])
            K = float(soil_data['K'])
            pH = float(soil_data['ph'])
            temperature = float(soil_data['temperature'])
            humidity = float(soil_data['humidity'])
            rainfall = float(soil_data['rainfall'])
            
            # Rule-based crop recommendations
            crop_recommendations = []
            
            # Rice recommendations
            if (N > 70 and humidity > 80 and rainfall > 200):
                crop_recommendations.append({
                    'crop': 'rice',
                    'fertilizer': 'urea',
                    'confidence': 0.9,
                    'reason': 'High nitrogen, humidity, and rainfall suitable for rice'
                })
            
            # Wheat recommendations
            if (20 <= temperature <= 25 and pH >= 6.0 and pH <= 7.5):
                crop_recommendations.append({
                    'crop': 'wheat',
                    'fertilizer': 'DAP',
                    'confidence': 0.8,
                    'reason': 'Optimal temperature and pH range for wheat'
                })
            
            # Maize recommendations
            if (temperature > 25 and N > 50 and K > 30):
                crop_recommendations.append({
                    'crop': 'maize',
                    'fertilizer': 'NPK_complex',
                    'confidence': 0.85,
                    'reason': 'High temperature and balanced NPK for maize'
                })
            
            # Soybean recommendations
            if (P > 40 and pH >= 6.0 and pH <= 7.0):
                crop_recommendations.append({
                    'crop': 'soybean',
                    'fertilizer': 'phosphate_fertilizer',
                    'confidence': 0.75,
                    'reason': 'Good phosphorus levels and pH for legumes'
                })
            
            # Cotton recommendations
            if (temperature > 27 and K > 40 and rainfall < 150):
                crop_recommendations.append({
                    'crop': 'cotton',
                    'fertilizer': 'potash_fertilizer',
                    'confidence': 0.8,
                    'reason': 'High temperature, potassium, and low rainfall for cotton'
                })
            
            # Nutrient deficiency corrections
            nutrient_corrections = []
            
            if N < 30:
                nutrient_corrections.append({
                    'nutrient': 'Nitrogen',
                    'status': 'Deficient',
                    'fertilizer': 'urea',
                    'application_rate': '120-150 kg/ha',
                    'priority': 'High'
                })
            
            if P < 20:
                nutrient_corrections.append({
                    'nutrient': 'Phosphorus',
                    'status': 'Deficient',
                    'fertilizer': 'DAP',
                    'application_rate': '60-80 kg/ha',
                    'priority': 'Medium'
                })
            
            if K < 25:
                nutrient_corrections.append({
                    'nutrient': 'Potassium',
                    'status': 'Deficient',
                    'fertilizer': 'MOP',
                    'application_rate': '50-75 kg/ha',
                    'priority': 'Medium'
                })
            
            # pH correction recommendations
            ph_corrections = []
            if pH < 6.0:
                ph_corrections.append({
                    'issue': 'Acidic soil',
                    'correction': 'lime_application',
                    'material': 'Agricultural lime',
                    'rate': f'{(6.5 - pH) * 500} kg/ha',
                    'timing': 'Apply 2-3 months before planting'
                })
            elif pH > 8.0:
                ph_corrections.append({
                    'issue': 'Alkaline soil',
                    'correction': 'sulfur_application',
                    'material': 'Elemental sulfur',
                    'rate': f'{(pH - 7.0) * 200} kg/ha',
                    'timing': 'Apply and incorporate before planting'
                })
            
            recommendations.append({
                'source': 'rule_based',
                'crop_recommendations': crop_recommendations,
                'nutrient_corrections': nutrient_corrections,
                'ph_corrections': ph_corrections
            })
        
        except Exception as e:
            print(f"Rule-based recommendation failed: {str(e)}")
        
        return recommendations
    
    def _combine_recommendations(self, ml_recs, rule_recs, soil_data):
        """Combine ML and rule-based recommendations"""
        combined = []
        
        # Process ML recommendations
        for ml_rec in ml_recs:
            combined.append({
                'type': 'crop_fertilizer',
                'crop': ml_rec['crop'],
                'fertilizer': ml_rec['fertilizer'],
                'confidence': ml_rec['confidence'],
                'source': f"ML Model ({ml_rec['model']})",
                'priority': 'High' if ml_rec['confidence'] > 0.8 else 'Medium'
            })
        
        # Process rule-based recommendations
        for rule_rec in rule_recs:
            if 'crop_recommendations' in rule_rec:
                for crop_rec in rule_rec['crop_recommendations']:
                    combined.append({
                        'type': 'crop_fertilizer',
                        'crop': crop_rec['crop'],
                        'fertilizer': crop_rec['fertilizer'],
                        'confidence': crop_rec['confidence'],
                        'source': 'Agronomic Rules',
                        'reason': crop_rec['reason'],
                        'priority': 'High' if crop_rec['confidence'] > 0.8 else 'Medium'
                    })
            
            if 'nutrient_corrections' in rule_rec:
                for nutrient_rec in rule_rec['nutrient_corrections']:
                    combined.append({
                        'type': 'nutrient_correction',
                        'nutrient': nutrient_rec['nutrient'],
                        'fertilizer': nutrient_rec['fertilizer'],
                        'application_rate': nutrient_rec['application_rate'],
                        'priority': nutrient_rec['priority'],
                        'source': 'Nutrient Analysis'
                    })
        
        # Sort by confidence and priority
        combined.sort(key=lambda x: (
            x.get('priority') == 'High',
            x.get('confidence', 0)
        ), reverse=True)
        
        return combined[:5]  # Return top 5 recommendations
    
    def _decode_prediction(self, prediction_value):
        """Decode ML prediction to crop/fertilizer names"""
        # This is a simplified mapping - in practice, you'd load the label encoders
        crop_mapping = {
            0: 'rice', 1: 'maize', 2: 'wheat', 3: 'soybean', 4: 'cotton',
            5: 'chickpea', 6: 'kidneybeans', 7: 'pigeonpeas', 8: 'mothbeans',
            9: 'mungbean', 10: 'blackgram', 11: 'lentil', 12: 'pomegranate'
        }
        
        fertilizer_mapping = {
            0: 'urea', 1: 'DAP', 2: 'NPK_complex', 3: 'phosphate_fertilizer',
            4: 'potash_fertilizer', 5: 'organic_compost'
        }
        
        crop = crop_mapping.get(prediction_value % len(crop_mapping), 'unknown')
        fertilizer = fertilizer_mapping.get(prediction_value % len(fertilizer_mapping), 'NPK_complex')
        
        return {'crop': crop, 'fertilizer': fertilizer}
    
    def _analyze_soil_condition(self, soil_data):
        """Analyze overall soil condition"""
        try:
            N = float(soil_data['N'])
            P = float(soil_data['P'])
            K = float(soil_data['K'])
            pH = float(soil_data['ph'])
            
            # Nutrient status
            nutrient_status = {}
            
            # Nitrogen status
            if N < 30:
                nutrient_status['nitrogen'] = 'Low'
            elif N < 60:
                nutrient_status['nitrogen'] = 'Medium'
            else:
                nutrient_status['nitrogen'] = 'High'
            
            # Phosphorus status
            if P < 20:
                nutrient_status['phosphorus'] = 'Low'
            elif P < 40:
                nutrient_status['phosphorus'] = 'Medium'
            else:
                nutrient_status['phosphorus'] = 'High'
            
            # Potassium status
            if K < 25:
                nutrient_status['potassium'] = 'Low'
            elif K < 50:
                nutrient_status['potassium'] = 'Medium'
            else:
                nutrient_status['potassium'] = 'High'
            
            # pH status
            if pH < 6.0:
                ph_status = 'Acidic'
            elif pH > 8.0:
                ph_status = 'Alkaline'
            else:
                ph_status = 'Neutral'
            
            # Overall fertility score
            fertility_score = self._calculate_fertility_score(soil_data)
            
            return {
                'nutrient_status': nutrient_status,
                'ph_status': ph_status,
                'fertility_score': fertility_score,
                'overall_condition': self._get_overall_condition(fertility_score)
            }
        
        except Exception as e:
            return {'error': f'Soil analysis failed: {str(e)}'}
    
    def _calculate_fertility_score(self, soil_data):
        """Calculate overall soil fertility score (0-100)"""
        try:
            N = float(soil_data['N'])
            P = float(soil_data['P'])
            K = float(soil_data['K'])
            pH = float(soil_data['ph'])
            
            # Normalize nutrient levels (0-1 scale)
            n_score = min(N / 80, 1.0)  # Optimal around 80
            p_score = min(P / 60, 1.0)  # Optimal around 60
            k_score = min(K / 70, 1.0)  # Optimal around 70
            
            # pH score (optimal around 6.5-7.0)
            if 6.5 <= pH <= 7.0:
                ph_score = 1.0
            elif 6.0 <= pH < 6.5 or 7.0 < pH <= 7.5:
                ph_score = 0.8
            elif 5.5 <= pH < 6.0 or 7.5 < pH <= 8.0:
                ph_score = 0.6
            else:
                ph_score = 0.3
            
            # Weighted average
            fertility_score = (n_score * 0.3 + p_score * 0.25 + k_score * 0.25 + ph_score * 0.2) * 100
            
            return round(fertility_score, 1)
        
        except Exception as e:
            return 0.0
    
    def _get_overall_condition(self, fertility_score):
        """Get overall soil condition based on fertility score"""
        if fertility_score >= 80:
            return 'Excellent'
        elif fertility_score >= 60:
            return 'Good'
        elif fertility_score >= 40:
            return 'Fair'
        else:
            return 'Poor'
    
    def _add_explanations(self, recommendations, soil_data):
        """Add detailed explanations to recommendations"""
        explained = []
        
        for rec in recommendations:
            explanation = {
                **rec,
                'explanation': self._generate_explanation(rec, soil_data),
                'benefits': self._get_benefits(rec),
                'precautions': self._get_precautions(rec)
            }
            explained.append(explanation)
        
        return explained
    
    def _generate_explanation(self, recommendation, soil_data):
        """Generate explanation for a recommendation"""
        if recommendation['type'] == 'crop_fertilizer':
            return f"Based on your soil's NPK levels ({soil_data['N']}-{soil_data['P']}-{soil_data['K']}) and environmental conditions, {recommendation['crop']} is suitable for cultivation with {recommendation['fertilizer']} fertilizer."
        elif recommendation['type'] == 'nutrient_correction':
            return f"Your soil shows {recommendation['nutrient'].lower()} deficiency. Applying {recommendation['fertilizer']} will help correct this imbalance."
        else:
            return "Recommendation based on soil analysis results."
    
    def _get_benefits(self, recommendation):
        """Get benefits of following the recommendation"""
        benefits = []
        
        if recommendation['type'] == 'crop_fertilizer':
            benefits = [
                "Optimized crop yield",
                "Efficient nutrient utilization",
                "Improved soil health",
                "Cost-effective farming"
            ]
        elif recommendation['type'] == 'nutrient_correction':
            benefits = [
                "Corrected nutrient deficiency",
                "Enhanced plant growth",
                "Better root development",
                "Improved disease resistance"
            ]
        
        return benefits
    
    def _get_precautions(self, recommendation):
        """Get precautions for the recommendation"""
        precautions = [
            "Follow recommended application rates",
            "Apply fertilizer at appropriate timing",
            "Consider weather conditions",
            "Monitor soil moisture levels"
        ]
        
        if recommendation.get('fertilizer') == 'urea':
            precautions.append("Apply urea when soil moisture is adequate")
        
        return precautions
    
    def _get_application_guidelines(self, recommendations):
        """Get fertilizer application guidelines"""
        guidelines = {
            'timing': {
                'pre_planting': 'Apply phosphorus and potassium fertilizers 1-2 weeks before planting',
                'at_planting': 'Apply starter fertilizer at planting time',
                'post_planting': 'Apply nitrogen fertilizer in split doses during crop growth'
            },
            'method': {
                'broadcasting': 'Uniform distribution across the field',
                'band_placement': 'Placement in bands near plant roots',
                'foliar_application': 'Spray application on leaves for quick uptake'
            },
            'general_tips': [
                'Calibrate application equipment properly',
                'Apply fertilizers when soil moisture is adequate',
                'Avoid fertilizer application before heavy rains',
                'Incorporate fertilizers into soil when possible'
            ]
        }
        
        return guidelines
    
    def _predict_outcomes(self, recommendations, soil_data):
        """Predict expected outcomes from recommendations"""
        outcomes = {
            'yield_improvement': '15-25% increase in crop yield',
            'soil_health': 'Improved soil nutrient balance',
            'cost_benefit': 'Positive return on investment',
            'environmental_impact': 'Reduced nutrient wastage and environmental impact',
            'timeline': {
                'immediate': 'Improved plant growth within 2-3 weeks',
                'short_term': 'Visible crop improvement in 4-6 weeks',
                'long_term': 'Enhanced soil fertility over growing season'
            }
        }
        
        return outcomes
    
    def _build_fertilizer_knowledge_base(self):
        """Build fertilizer knowledge base"""
        return {
            'urea': {
                'nitrogen_content': 46,
                'suitable_crops': ['rice', 'wheat', 'maize', 'sugarcane'],
                'application_rate': '100-150 kg/ha',
                'timing': 'Split application during crop growth'
            },
            'DAP': {
                'nitrogen_content': 18,
                'phosphorus_content': 46,
                'suitable_crops': ['wheat', 'rice', 'legumes'],
                'application_rate': '60-80 kg/ha',
                'timing': 'Basal application before planting'
            },
            'NPK_complex': {
                'balanced_nutrition': True,
                'suitable_crops': ['vegetables', 'fruits', 'cereals'],
                'application_rate': '75-125 kg/ha',
                'timing': 'Basal and top dressing'
            },
            'organic_compost': {
                'organic_matter': True,
                'slow_release': True,
                'suitable_crops': ['all crops'],
                'application_rate': '2-5 tons/ha',
                'timing': 'Before planting'
            }
        }