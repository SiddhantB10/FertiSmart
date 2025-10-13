"""
API Routes for FertiSmart
RESTful endpoints for all 7 DMBI experiments
"""

from flask import Blueprint, request, jsonify, current_app
from flask_restful import Api, Resource
import pandas as pd
import numpy as np
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime

# Import ML services
from app.services.preprocessing_service import PreprocessingService
from app.services.classification_service import ClassificationService
from app.services.clustering_service import ClusteringService
from app.services.visualization_service import VisualizationService
from app.services.recommendation_service import RecommendationService
from app.services.analytics_service import AnalyticsService

# Import models
from app.models.database_models import *
from app import db

# Create Blueprint
api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def allowed_file(filename):
    """Check if file extension is allowed"""
    ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'json'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_soil_data(data):
    """Validate soil test data format"""
    required_fields = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
    return True, "Valid"

# =============================================================================
# EXPERIMENT 2: DATA PREPROCESSING ENDPOINTS
# =============================================================================

class DataPreprocessingAPI(Resource):
    """Data preprocessing and cleaning endpoints"""
    
    def post(self):
        """Upload and preprocess soil data"""
        try:
            # Handle file upload
            if 'file' not in request.files:
                return {'error': 'No file uploaded'}, 400
            
            file = request.files['file']
            if file.filename == '':
                return {'error': 'No file selected'}, 400
            
            if not allowed_file(file.filename):
                return {'error': 'Invalid file format. Use CSV, XLSX, or JSON'}, 400
            
            # Save uploaded file
            filename = secure_filename(file.filename)
            upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            os.makedirs(os.path.dirname(upload_path), exist_ok=True)
            file.save(upload_path)
            
            # Process the data
            preprocessing_service = PreprocessingService()
            result = preprocessing_service.process_file(upload_path)
            
            return {
                'message': 'Data preprocessed successfully',
                'data': result,
                'timestamp': datetime.utcnow().isoformat()
            }, 200
            
        except Exception as e:
            return {'error': str(e)}, 500
    
    def get(self):
        """Get preprocessing status and metrics"""
        try:
            # Get latest data quality metrics
            metrics = DataQualityMetrics.query.order_by(
                DataQualityMetrics.analyzed_at.desc()
            ).first()
            
            if not metrics:
                return {'message': 'No preprocessing data available'}, 404
            
            return {
                'dataset_name': metrics.dataset_name,
                'total_records': metrics.total_records,
                'missing_values': metrics.missing_values,
                'duplicate_records': metrics.duplicate_records,
                'outliers_detected': metrics.outliers_detected,
                'quality_score': metrics.quality_score,
                'analyzed_at': metrics.analyzed_at.isoformat()
            }, 200
            
        except Exception as e:
            return {'error': str(e)}, 500

# =============================================================================
# EXPERIMENT 3: EDA AND VISUALIZATION ENDPOINTS
# =============================================================================

class VisualizationAPI(Resource):
    """Exploratory Data Analysis and Visualization"""
    
    def get(self):
        """Generate EDA visualizations"""
        try:
            viz_type = request.args.get('type', 'correlation')
            
            visualization_service = VisualizationService()
            
            if viz_type == 'correlation':
                result = visualization_service.generate_correlation_matrix()
            elif viz_type == 'distribution':
                result = visualization_service.generate_nutrient_distribution()
            elif viz_type == 'trends':
                result = visualization_service.generate_trend_analysis()
            elif viz_type == 'summary':
                result = visualization_service.generate_summary_stats()
            else:
                return {'error': 'Invalid visualization type'}, 400
            
            return result, 200
            
        except Exception as e:
            return {'error': str(e)}, 500

class AnalyticsAPI(Resource):
    """Business Intelligence and Analytics"""
    
    def get(self):
        """Get analytical insights"""
        try:
            analytics_service = AnalyticsService()
            
            # Get comprehensive analytics
            result = {
                'overview': analytics_service.get_overview_stats(),
                'nutrient_analysis': analytics_service.analyze_nutrients(),
                'regional_insights': analytics_service.get_regional_insights(),
                'crop_fertilizer_trends': analytics_service.get_crop_fertilizer_trends(),
                'seasonal_patterns': analytics_service.get_seasonal_patterns()
            }
            
            return result, 200
            
        except Exception as e:
            return {'error': str(e)}, 500

# =============================================================================
# EXPERIMENTS 4 & 5: CLASSIFICATION ENDPOINTS
# =============================================================================

class ClassificationAPI(Resource):
    """Random Forest Classification for Crop Recommendation"""
    
    def post(self):
        """Train Random Forest crop recommendation model"""
        try:
            classification_service = ClassificationService()
            result = classification_service.train_crop_recommendation_model()
            
            return {
                'message': 'Random Forest crop recommendation model trained successfully',
                'model_info': result,
                'timestamp': datetime.utcnow().isoformat()
            }, 200
            
        except Exception as e:
            return {'error': str(e)}, 500
    
    def get(self):
        """Get Random Forest model information and performance"""
        try:
            # Check if model exists
            model_path = os.path.join('trained_models', 'crop_recommendation_rf.pkl')
            
            if not os.path.exists(model_path):
                return {
                    'message': 'Random Forest model not found. Please train the model first.',
                    'model_trained': False
                }, 404
            
            # Load model info
            import joblib
            model = joblib.load(model_path)
            
            # Get sample data for demonstration
            df = pd.read_csv('Crop_recommendation.csv')
            sample_data = df.sample(5).to_dict('records')
            
            return {
                'message': 'Random Forest crop recommendation model is ready',
                'model_trained': True,
                'model_info': {
                    'algorithm': 'Random Forest Classifier',
                    'n_estimators': model.n_estimators,
                    'max_depth': model.max_depth,
                    'available_crops': sorted(model.classes_.tolist()),
                    'total_crops': len(model.classes_),
                    'feature_names': ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
                },
                'sample_data': sample_data,
                'timestamp': datetime.utcnow().isoformat()
            }, 200
            
        except Exception as e:
            return {'error': str(e)}, 500

# =============================================================================
# EXPERIMENTS 6 & 7: CLUSTERING ENDPOINTS
# =============================================================================

class ClusteringAPI(Resource):
    """Machine Learning Clustering Endpoints"""
    
    def post(self):
        """Perform clustering analysis"""
        try:
            data = request.get_json()
            algorithm = data.get('algorithm', 'kmeans')
            n_clusters = data.get('n_clusters', 3)
            
            clustering_service = ClusteringService()
            
            if algorithm == 'kmeans':
                result = clustering_service.perform_kmeans(n_clusters)
            elif algorithm == 'agglomerative':
                result = clustering_service.perform_agglomerative(n_clusters)
            elif algorithm == 'dbscan':
                eps = data.get('eps', 0.5)
                min_samples = data.get('min_samples', 5)
                result = clustering_service.perform_dbscan(eps, min_samples)
            elif algorithm == 'all':
                kmeans_result = clustering_service.perform_kmeans(n_clusters)
                agg_result = clustering_service.perform_agglomerative(n_clusters)
                dbscan_result = clustering_service.perform_dbscan(0.5, 5)
                result = {
                    'kmeans': kmeans_result,
                    'agglomerative': agg_result,
                    'dbscan': dbscan_result
                }
            else:
                return {'error': 'Invalid clustering algorithm'}, 400
            
            return result, 200
            
        except Exception as e:
            return {'error': str(e)}, 500
    
    def get(self):
        """Get clustering results"""
        try:
            algorithm = request.args.get('algorithm', 'all')
            
            query = ClusterResult.query
            if algorithm != 'all':
                query = query.filter_by(clustering_algorithm=algorithm)
            
            results = query.order_by(ClusterResult.created_at.desc()).limit(100).all()
            
            cluster_data = []
            for result in results:
                cluster_data.append({
                    'id': result.id,
                    'algorithm': result.clustering_algorithm,
                    'cluster_id': result.cluster_id,
                    'cluster_label': result.cluster_label,
                    'silhouette_score': result.silhouette_score,
                    'distance_to_centroid': result.distance_to_centroid,
                    'n_clusters': result.n_clusters,
                    'created_at': result.created_at.isoformat()
                })
            
            return {'clusters': cluster_data}, 200
            
        except Exception as e:
            return {'error': str(e)}, 500

# =============================================================================
# CROP RECOMMENDATION ENGINE
# =============================================================================

class CropRecommendationAPI(Resource):
    """Smart Crop Recommendation using Random Forest"""
    
    def post(self):
        """Train the Random Forest crop recommendation model"""
        try:
            classification_service = ClassificationService()
            result = classification_service.train_crop_recommendation_model()
            
            return {
                'message': 'Crop recommendation model trained successfully',
                'model_info': result,
                'timestamp': datetime.utcnow().isoformat()
            }, 200
            
        except Exception as e:
            return {'error': str(e)}, 500
    
    def get(self):
        """Get model information and sample predictions"""
        try:
            # Check if model exists
            import os
            model_path = os.path.join('trained_models', 'crop_recommendation_rf.pkl')
            
            if not os.path.exists(model_path):
                return {
                    'message': 'Crop recommendation model not found. Please train the model first.',
                    'model_trained': False
                }, 404
            
            # Load model info
            import joblib
            model = joblib.load(model_path)
            
            # Get sample data for demonstration
            import pandas as pd
            df = pd.read_csv('Crop_recommendation.csv')
            sample_data = df.sample(5).to_dict('records')
            
            return {
                'message': 'Crop recommendation model is ready',
                'model_trained': True,
                'model_info': {
                    'algorithm': 'Random Forest Classifier',
                    'n_estimators': model.n_estimators,
                    'max_depth': model.max_depth,
                    'available_crops': sorted(model.classes_.tolist()),
                    'total_crops': len(model.classes_),
                    'feature_names': ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
                },
                'sample_data': sample_data,
                'timestamp': datetime.utcnow().isoformat()
            }, 200
            
        except Exception as e:
            return {'error': str(e)}, 500

class CropPredictionAPI(Resource):
    """Predict suitable crop based on soil and climate conditions"""
    
    def post(self):
        """Predict the most suitable crop for given conditions"""
        try:
            data = request.get_json()
            
            # Validate input data
            required_fields = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
            for field in required_fields:
                if field not in data:
                    return {'error': f'Missing required field: {field}'}, 400
                
                # Validate that values are numeric
                try:
                    float(data[field])
                except (ValueError, TypeError):
                    return {'error': f'Invalid value for {field}. Must be a number.'}, 400
            
            # Make prediction
            classification_service = ClassificationService()
            prediction_result = classification_service.predict_crop(data)
            
            return {
                'success': True,
                'prediction': prediction_result,
                'timestamp': datetime.utcnow().isoformat()
            }, 200
            
        except FileNotFoundError:
            return {
                'error': 'Crop recommendation model not found. Please train the model first.',
                'suggestion': 'Use POST /api/crop-recommendation to train the model'
            }, 404
        except Exception as e:
            return {'error': str(e)}, 500
    
    def get(self):
        """Get sample input format and available crops"""
        try:
            # Check if model exists
            import os
            model_path = os.path.join('trained_models', 'crop_recommendation_rf.pkl')
            
            if os.path.exists(model_path):
                import joblib
                model = joblib.load(model_path)
                available_crops = sorted(model.classes_.tolist())
            else:
                available_crops = []
            
            # Get sample data ranges from CSV
            import pandas as pd
            df = pd.read_csv('Crop_recommendation.csv')
            
            feature_ranges = {}
            for col in ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']:
                feature_ranges[col] = {
                    'min': float(df[col].min()),
                    'max': float(df[col].max()),
                    'mean': float(df[col].mean()),
                    'description': self._get_feature_description(col)
                }
            
            return {
                'input_format': {
                    'N': 'Nitrogen content (0-100)',
                    'P': 'Phosphorus content (0-80)',
                    'K': 'Potassium content (0-80)',
                    'temperature': 'Temperature in Celsius (10-40)',
                    'humidity': 'Humidity percentage (30-100)',
                    'ph': 'Soil pH level (4-9)',
                    'rainfall': 'Rainfall in mm (50-300)'
                },
                'feature_ranges': feature_ranges,
                'available_crops': available_crops,
                'total_crops': len(available_crops),
                'sample_input': {
                    'N': 90,
                    'P': 42,
                    'K': 43,
                    'temperature': 20.8,
                    'humidity': 82.0,
                    'ph': 6.5,
                    'rainfall': 202.9
                },
                'model_ready': len(available_crops) > 0
            }, 200
            
        except Exception as e:
            return {'error': str(e)}, 500
    
    def _get_feature_description(self, feature):
        """Get description for each feature"""
        descriptions = {
            'N': 'Nitrogen (N) - Essential for leaf growth and green color',
            'P': 'Phosphorus (P) - Important for root development and flowering',
            'K': 'Potassium (K) - Crucial for fruit development and disease resistance',
            'temperature': 'Average temperature - Affects plant growth and development',
            'humidity': 'Relative humidity - Influences water availability and disease risk',
            'ph': 'Soil pH - Determines nutrient availability to plants',
            'rainfall': 'Annual rainfall - Primary source of water for crops'
        }
        return descriptions.get(feature, f'{feature} - Agricultural parameter')

# =============================================================================
# FERTILIZER RECOMMENDATION ENGINE
# =============================================================================

class RecommendationAPI(Resource):
    """Smart Fertilizer Recommendation Engine"""
    
    def post(self):
        """Get fertilizer recommendations based on soil data"""
        try:
            data = request.get_json()
            
            # Validate input data
            is_valid, message = validate_soil_data(data)
            if not is_valid:
                return {'error': message}, 400
            
            recommendation_service = RecommendationService()
            recommendations = recommendation_service.get_recommendations(data)
            
            return recommendations, 200
            
        except Exception as e:
            return {'error': str(e)}, 500

# =============================================================================
# DATA WAREHOUSE SCHEMA ENDPOINTS (EXPERIMENT 1)
# =============================================================================

class SchemaAPI(Resource):
    """Database Schema Information and ER Diagrams"""
    
    def get(self):
        """Get database schema information"""
        try:
            schema_type = request.args.get('type', 'star')
            
            if schema_type == 'star':
                schema_info = {
                    'schema_type': 'Star Schema',
                    'fact_table': 'soil_test_fact',
                    'dimension_tables': [
                        'region_dim',
                        'crop_dim', 
                        'fertilizer_dim',
                        'time_dim'
                    ],
                    'relationships': {
                        'soil_test_fact': {
                            'region_id': 'region_dim.region_id',
                            'crop_id': 'crop_dim.crop_id',
                            'fertilizer_id': 'fertilizer_dim.fertilizer_id',
                            'time_id': 'time_dim.time_id'
                        }
                    }
                }
            elif schema_type == 'snowflake':
                schema_info = {
                    'schema_type': 'Snowflake Schema',
                    'fact_table': 'soil_test_fact',
                    'dimension_tables': [
                        'region_dim',
                        'state_dim',
                        'district_dim',
                        'crop_dim',
                        'crop_type_dim',
                        'fertilizer_dim',
                        'time_dim'
                    ],
                    'normalized_relationships': {
                        'region_dim': 'state_dim, district_dim',
                        'crop_dim': 'crop_type_dim'
                    }
                }
            else:
                return {'error': 'Invalid schema type'}, 400
            
            return schema_info, 200
            
        except Exception as e:
            return {'error': str(e)}, 500

# =============================================================================
# REGISTER API ENDPOINTS
# =============================================================================

# Register all API resources
api.add_resource(DataPreprocessingAPI, '/preprocess')
api.add_resource(VisualizationAPI, '/visualize')
api.add_resource(AnalyticsAPI, '/analytics')
api.add_resource(ClassificationAPI, '/classify')
api.add_resource(ClusteringAPI, '/cluster')
api.add_resource(CropRecommendationAPI, '/crop-recommendation')
api.add_resource(CropPredictionAPI, '/crop-prediction')
api.add_resource(RecommendationAPI, '/recommend')
api.add_resource(SchemaAPI, '/schema')

# Additional utility endpoints
@api_bp.route('/health', methods=['GET'])
def api_health():
    """API health check"""
    return jsonify({
        'status': 'healthy',
        'api_version': '1.0.0',
        'endpoints': {
            'preprocess': '/api/preprocess',
            'visualize': '/api/visualize',
            'analytics': '/api/analytics',
            'classify': '/api/classify',
            'cluster': '/api/cluster',
            'recommend': '/api/recommend',
            'schema': '/api/schema'
        }
    })

@api_bp.route('/experiments', methods=['GET'])
def get_experiments():
    """Get information about all 7 DMBI experiments"""
    return jsonify({
        'experiments': [
            {
                'id': 1,
                'name': 'Data Warehouse Design',
                'description': 'Star Schema and Snowflake Schema implementation',
                'endpoint': '/api/schema'
            },
            {
                'id': 2,
                'name': 'Data Preprocessing',
                'description': 'Data cleaning, normalization, and quality metrics',
                'endpoint': '/api/preprocess'
            },
            {
                'id': 3,
                'name': 'Exploratory Data Analysis',
                'description': 'Statistical analysis and visualizations',
                'endpoint': '/api/visualize'
            },
            {
                'id': 4,
                'name': 'Classification (Weka/RapidMiner)',
                'description': 'External tool classification results',
                'endpoint': '/api/classify?tool=weka'
            },
            {
                'id': 5,
                'name': 'Classification (Python)',
                'description': 'Python scikit-learn classification models',
                'endpoint': '/api/classify'
            },
            {
                'id': 6,
                'name': 'Clustering (Weka/RapidMiner)',
                'description': 'External tool clustering analysis',
                'endpoint': '/api/cluster?tool=weka'
            },
            {
                'id': 7,
                'name': 'Clustering (Python)',
                'description': 'Python clustering algorithms with visualization',
                'endpoint': '/api/cluster'
            }
        ]
    })