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
    """Machine Learning Classification Endpoints"""
    
    def post(self):
        """Train classification models"""
        try:
            data = request.get_json()
            model_type = data.get('model_type', 'decision_tree')
            target = data.get('target', 'crop')  # crop or fertilizer
            
            classification_service = ClassificationService()
            
            if model_type == 'decision_tree':
                result = classification_service.train_decision_tree(target)
            elif model_type == 'naive_bayes':
                result = classification_service.train_naive_bayes(target)
            elif model_type == 'both':
                dt_result = classification_service.train_decision_tree(target)
                nb_result = classification_service.train_naive_bayes(target)
                result = {
                    'decision_tree': dt_result,
                    'naive_bayes': nb_result
                }
            else:
                return {'error': 'Invalid model type'}, 400
            
            return result, 200
            
        except Exception as e:
            return {'error': str(e)}, 500
    
    def get(self):
        """Get classification results and model performance"""
        try:
            # Get latest model predictions
            predictions = ModelPrediction.query.order_by(
                ModelPrediction.created_at.desc()
            ).limit(10).all()
            
            result = []
            for pred in predictions:
                result.append({
                    'id': pred.id,
                    'model_name': pred.model_name,
                    'predicted_crop': pred.predicted_crop,
                    'predicted_fertilizer': pred.predicted_fertilizer,
                    'confidence_score': pred.confidence_score,
                    'accuracy': pred.accuracy,
                    'precision': pred.precision,
                    'recall': pred.recall,
                    'f1_score': pred.f1_score,
                    'created_at': pred.created_at.isoformat()
                })
            
            return {'predictions': result}, 200
            
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
# RECOMMENDATION ENGINE
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