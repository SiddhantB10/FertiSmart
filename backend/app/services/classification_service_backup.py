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
    
    def train_naive_bayes(self, target='crop'):
        """Train Naive Bayes classifier"""
        try:
            # Get preprocessed data
            data_split = self.preprocessing_service.get_train_test_split()
            
            X_train = data_split['X_train']
            X_test = data_split['X_test']
            
            if target == 'crop':
                y_train = data_split['y_crop_train']
                y_test = data_split['y_crop_test']
            else:
                y_train = data_split['y_fertilizer_train']
                y_test = data_split['y_fertilizer_test']
            
            # Initialize and train Naive Bayes
            nb_model = GaussianNB()
            nb_model.fit(X_train, y_train)
            
            # Make predictions
            y_pred = nb_model.predict(X_test)
            y_pred_proba = nb_model.predict_proba(X_test)
            
            # Calculate metrics
            metrics = self._calculate_metrics(y_test, y_pred)
            
            # Cross-validation
            cv_scores = cross_val_score(nb_model, X_train, y_train, cv=5)
            
            # Save model
            model_name = f'naive_bayes_{target}'
            model_path = os.path.join('trained_models', f'{model_name}.pkl')
            os.makedirs('trained_models', exist_ok=True)
            joblib.dump(nb_model, model_path)
            
            # Store results in database
            self._store_model_results(
                model_name=model_name,
                target=target,
                metrics=metrics,
                y_test=y_test,
                y_pred=y_pred
            )
            
            # Prepare detailed results
            result = {
                'model_type': 'Naive Bayes',
                'target': target,
                'model_parameters': {
                    'algorithm': 'Gaussian Naive Bayes',
                    'priors': 'None (calculated from data)'
                },
                'performance_metrics': metrics,
                'cross_validation': {
                    'cv_scores': cv_scores.tolist(),
                    'mean_cv_score': cv_scores.mean(),
                    'std_cv_score': cv_scores.std()
                },
                'prediction_probabilities': {
                    'mean_confidence': np.mean(np.max(y_pred_proba, axis=1)),
                    'confidence_distribution': np.histogram(np.max(y_pred_proba, axis=1), bins=10)[0].tolist()
                },
                'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
                'classification_report': classification_report(y_test, y_pred, output_dict=True),
                'model_path': model_path,
                'training_samples': len(X_train),
                'test_samples': len(X_test)
            }
            
            return result
            
        except Exception as e:
            raise Exception(f"Naive Bayes training failed: {str(e)}")
    
    def _calculate_metrics(self, y_true, y_pred):
        """Calculate comprehensive classification metrics"""
        return {
            'accuracy': round(accuracy_score(y_true, y_pred), 4),
            'precision': round(precision_score(y_true, y_pred, average='weighted'), 4),
            'recall': round(recall_score(y_true, y_pred, average='weighted'), 4),
            'f1_score': round(f1_score(y_true, y_pred, average='weighted'), 4),
            'precision_macro': round(precision_score(y_true, y_pred, average='macro'), 4),
            'recall_macro': round(recall_score(y_true, y_pred, average='macro'), 4),
            'f1_score_macro': round(f1_score(y_true, y_pred, average='macro'), 4)
        }
    
    def _get_feature_importance(self, model, feature_names):
        """Get feature importance for tree-based models"""
        if hasattr(model, 'feature_importances_'):
            importance_dict = {}
            for i, importance in enumerate(model.feature_importances_):
                importance_dict[feature_names[i]] = round(importance, 4)
            
            # Sort by importance
            sorted_importance = dict(sorted(importance_dict.items(), 
                                          key=lambda x: x[1], reverse=True))
            return sorted_importance
        return {}
    
    def _store_model_results(self, model_name, target, metrics, y_test, y_pred):
        """Store model results in database"""
        try:
            # Store one record for the overall model performance
            prediction_record = ModelPrediction(
                model_name=model_name,
                model_version='1.0',
                predicted_crop=target if target == 'crop' else None,
                predicted_fertilizer=target if target == 'fertilizer' else None,
                confidence_score=metrics['accuracy'],
                accuracy=metrics['accuracy'],
                precision=metrics['precision'],
                recall=metrics['recall'],
                f1_score=metrics['f1_score']
            )
            
            db.session.add(prediction_record)
            db.session.commit()
            
        except Exception as e:
            print(f"Warning: Could not store model results in database: {str(e)}")
    
    def predict_single(self, model_type, target, input_features):
        """Make prediction for a single sample"""
        try:
            model_name = f'{model_type}_{target}'
            model_path = os.path.join('trained_models', f'{model_name}.pkl')
            
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model {model_name} not found. Please train the model first.")
            
            # Load model
            model = joblib.load(model_path)
            
            # Make prediction
            prediction = model.predict([input_features])
            
            # Get prediction probability if available
            confidence = None
            if hasattr(model, 'predict_proba'):
                proba = model.predict_proba([input_features])
                confidence = np.max(proba[0])
            
            return {
                'prediction': int(prediction[0]),
                'confidence': float(confidence) if confidence else None,
                'model_type': model_type,
                'target': target
            }
            
        except Exception as e:
            raise Exception(f"Prediction failed: {str(e)}")
    
    def compare_models(self, target='crop'):
        """Compare Decision Tree and Naive Bayes performance"""
        try:
            # Train both models
            dt_results = self.train_decision_tree(target)
            nb_results = self.train_naive_bayes(target)
            
            # Compare performance
            comparison = {
                'target': target,
                'decision_tree': {
                    'accuracy': dt_results['performance_metrics']['accuracy'],
                    'precision': dt_results['performance_metrics']['precision'],
                    'recall': dt_results['performance_metrics']['recall'],
                    'f1_score': dt_results['performance_metrics']['f1_score'],
                    'cross_val_mean': dt_results['cross_validation']['mean_cv_score']
                },
                'naive_bayes': {
                    'accuracy': nb_results['performance_metrics']['accuracy'],
                    'precision': nb_results['performance_metrics']['precision'],
                    'recall': nb_results['performance_metrics']['recall'],
                    'f1_score': nb_results['performance_metrics']['f1_score'],
                    'cross_val_mean': nb_results['cross_validation']['mean_cv_score']
                }
            }
            
            # Determine best model
            dt_score = dt_results['performance_metrics']['f1_score']
            nb_score = nb_results['performance_metrics']['f1_score']
            
            comparison['best_model'] = 'Decision Tree' if dt_score > nb_score else 'Naive Bayes'
            comparison['performance_difference'] = abs(dt_score - nb_score)
            
            return {
                'comparison': comparison,
                'detailed_results': {
                    'decision_tree': dt_results,
                    'naive_bayes': nb_results
                }
            }
            
        except Exception as e:
            raise Exception(f"Model comparison failed: {str(e)}")
    
    def get_model_interpretability(self, model_type, target):
        """Get model interpretability insights"""
        try:
            model_name = f'{model_type}_{target}'
            model_path = os.path.join('trained_models', f'{model_name}.pkl')
            
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model {model_name} not found")
            
            model = joblib.load(model_path)
            
            if model_type == 'decision_tree':
                # For decision trees, we can extract rules
                feature_names = ['nitrogen_scaled', 'phosphorus_scaled', 'potassium_scaled', 
                               'temperature_scaled', 'humidity_scaled', 'ph_scaled', 'rainfall_scaled']
                
                importance = self._get_feature_importance(model, feature_names)
                
                return {
                    'model_type': 'Decision Tree',
                    'interpretability': {
                        'feature_importance': importance,
                        'max_depth': model.max_depth,
                        'n_leaves': model.get_n_leaves(),
                        'tree_structure': 'Available through visualization'
                    },
                    'insights': {
                        'most_important_feature': max(importance.items(), key=lambda x: x[1])[0] if importance else None,
                        'interpretable': True,
                        'explanation': 'Decision tree provides clear if-then rules for predictions'
                    }
                }
            
            elif model_type == 'naive_bayes':
                return {
                    'model_type': 'Naive Bayes',
                    'interpretability': {
                        'class_priors': model.class_prior_.tolist() if hasattr(model, 'class_prior_') else None,
                        'feature_log_prob': 'Available but complex to interpret',
                        'assumptions': 'Features are conditionally independent given class'
                    },
                    'insights': {
                        'interpretable': False,
                        'explanation': 'Naive Bayes assumes feature independence and uses probabilistic approach'
                    }
                }
            
        except Exception as e:
            raise Exception(f"Model interpretability analysis failed: {str(e)}")
    
    def load_sample_data_and_train(self):
        """Load sample data and train models for demonstration"""
        try:
            # First ensure we have processed data
            self.preprocessing_service.load_sample_data()
            
            # Train both models for both targets
            results = {}
            
            # Train crop prediction models
            results['crop_decision_tree'] = self.train_decision_tree('crop')
            results['crop_naive_bayes'] = self.train_naive_bayes('crop')
            
            # Train fertilizer prediction models (using crop as proxy for fertilizer)
            results['fertilizer_decision_tree'] = self.train_decision_tree('fertilizer')
            results['fertilizer_naive_bayes'] = self.train_naive_bayes('fertilizer')
            
            return {
                'message': 'All classification models trained successfully',
                'models_trained': list(results.keys()),
                'results': results
            }
            
        except Exception as e:
            raise Exception(f"Sample training failed: {str(e)}")
    
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
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            # Train Random Forest model
            rf_model = RandomForestClassifier(
                n_estimators=100,
                max_depth=15,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1
            )
            
            rf_model.fit(X_train_scaled, y_train)
            
            # Make predictions
            y_pred = rf_model.predict(X_test_scaled)
            y_pred_proba = rf_model.predict_proba(X_test_scaled)
            
            # Calculate metrics
            metrics = self._calculate_metrics(y_test, y_pred)
            
            # Cross-validation
            cv_scores = cross_val_score(rf_model, X_train_scaled, y_train, cv=5)
            
            # Save model and scaler
            os.makedirs('trained_models', exist_ok=True)
            
            model_path = os.path.join('trained_models', 'crop_recommendation_rf.pkl')
            scaler_path = os.path.join('trained_models', 'crop_recommendation_scaler.pkl')
            
            joblib.dump(rf_model, model_path)
            joblib.dump(scaler, scaler_path)
            
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
                'feature_importance': self._get_feature_importance(rf_model, feature_columns),
                'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
                'classification_report': classification_report(y_test, y_pred, output_dict=True),
                'model_paths': {
                    'model': model_path,
                    'scaler': scaler_path
                },
                'sample_predictions': self._get_sample_predictions(rf_model, scaler, X_test, y_test, y_pred, y_pred_proba),
                'training_timestamp': datetime.utcnow().isoformat()
            }
            
            return result
            
        except Exception as e:
            raise Exception(f"Crop recommendation model training failed: {str(e)}")
    
    def predict_crop(self, soil_climate_data):
        """Predict the most suitable crop based on soil and climate conditions"""
        try:
            # Load the trained model and scaler
            model_path = os.path.join('trained_models', 'crop_recommendation_rf.pkl')
            scaler_path = os.path.join('trained_models', 'crop_recommendation_scaler.pkl')
            
            if not os.path.exists(model_path) or not os.path.exists(scaler_path):
                raise FileNotFoundError("Trained crop recommendation model not found. Please train the model first.")
            
            model = joblib.load(model_path)
            scaler = joblib.load(scaler_path)
            
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
            input_scaled = scaler.transform(input_data)
            
            # Make prediction
            prediction = model.predict(input_scaled)[0]
            prediction_proba = model.predict_proba(input_scaled)[0]
            
            # Get top 3 crop recommendations with confidence scores
            class_names = model.classes_
            confidence_scores = [(class_names[i], round(prob * 100, 2)) 
                               for i, prob in enumerate(prediction_proba)]
            confidence_scores.sort(key=lambda x: x[1], reverse=True)
            
            # Get feature importance for this prediction
            feature_importance = dict(zip(required_features, model.feature_importances_))
            
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
            
            # Store prediction in database
            self._store_crop_prediction(soil_climate_data, result)
            
            return result
            
        except Exception as e:
            raise Exception(f"Crop prediction failed: {str(e)}")
    
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
    
    def _store_crop_prediction(self, input_data, prediction_result):
        """Store crop prediction in database for tracking"""
        try:
            # This would integrate with your database model
            # For now, we'll just pass as the database integration 
            # depends on your specific model structure
            pass
        except Exception as e:
            # Log the error but don't fail the prediction
            print(f"Warning: Could not store prediction in database: {str(e)}")