"""
Classification Service for FertiSmart
Implements Decision Tree and Naive Bayes classification (Experiments 4 & 5)
"""

import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import cross_val_score
import joblib
import os
from datetime import datetime
import json

from app.models.database_models import ModelPrediction, PreprocessedData
from app.services.preprocessing_service import PreprocessingService
from app import db

class ClassificationService:
    """Machine Learning Classification Service"""
    
    def __init__(self):
        self.models = {}
        self.preprocessing_service = PreprocessingService()
    
    def train_decision_tree(self, target='crop', max_depth=10, random_state=42):
        """Train Decision Tree classifier"""
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
            
            # Initialize and train Decision Tree
            dt_model = DecisionTreeClassifier(
                max_depth=max_depth,
                random_state=random_state,
                min_samples_split=5,
                min_samples_leaf=2
            )
            
            dt_model.fit(X_train, y_train)
            
            # Make predictions
            y_pred = dt_model.predict(X_test)
            
            # Calculate metrics
            metrics = self._calculate_metrics(y_test, y_pred)
            
            # Cross-validation
            cv_scores = cross_val_score(dt_model, X_train, y_train, cv=5)
            
            # Save model
            model_name = f'decision_tree_{target}'
            model_path = os.path.join('trained_models', f'{model_name}.pkl')
            os.makedirs('trained_models', exist_ok=True)
            joblib.dump(dt_model, model_path)
            
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
                'model_type': 'Decision Tree',
                'target': target,
                'model_parameters': {
                    'max_depth': max_depth,
                    'min_samples_split': 5,
                    'min_samples_leaf': 2,
                    'random_state': random_state
                },
                'performance_metrics': metrics,
                'cross_validation': {
                    'cv_scores': cv_scores.tolist(),
                    'mean_cv_score': cv_scores.mean(),
                    'std_cv_score': cv_scores.std()
                },
                'feature_importance': self._get_feature_importance(dt_model, X_train.columns),
                'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
                'classification_report': classification_report(y_test, y_pred, output_dict=True),
                'model_path': model_path,
                'training_samples': len(X_train),
                'test_samples': len(X_test)
            }
            
            return result
            
        except Exception as e:
            raise Exception(f"Decision Tree training failed: {str(e)}")
    
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