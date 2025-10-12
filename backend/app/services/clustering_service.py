"""
Clustering Service for FertiSmart
Implements K-Means, Agglomerative, and DBSCAN clustering (Experiments 6 & 7)
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.preprocessing import StandardScaler
import joblib
import os
import json
from datetime import datetime

from app.models.database_models import ClusterResult, PreprocessedData
from app.services.preprocessing_service import PreprocessingService
from app import db

class ClusteringService:
    """Machine Learning Clustering Service"""
    
    def __init__(self):
        self.clustering_models = {}
        self.preprocessing_service = PreprocessingService()
    
    def perform_kmeans(self, n_clusters=3, random_state=42):
        """Perform K-Means clustering"""
        try:
            # Get preprocessed data
            X = self._get_feature_data()
            
            if X is None or len(X) == 0:
                raise ValueError("No preprocessed data available for clustering")
            
            # Initialize K-Means
            kmeans = KMeans(
                n_clusters=n_clusters,
                random_state=random_state,
                n_init=10,
                max_iter=300
            )
            
            # Fit the model
            cluster_labels = kmeans.fit_predict(X)
            
            # Calculate clustering metrics
            metrics = self._calculate_clustering_metrics(X, cluster_labels, n_clusters)
            
            # Store results
            self._store_clustering_results(
                algorithm='KMeans',
                cluster_labels=cluster_labels,
                metrics=metrics,
                n_clusters=n_clusters,
                algorithm_params={'n_clusters': n_clusters, 'random_state': random_state}
            )
            
            # Save model
            model_path = os.path.join('trained_models', f'kmeans_{n_clusters}_clusters.pkl')
            os.makedirs('trained_models', exist_ok=True)
            joblib.dump(kmeans, model_path)
            
            # Generate cluster analysis
            cluster_analysis = self._analyze_clusters(X, cluster_labels, 'KMeans')
            
            # Dimensionality reduction for visualization
            viz_data = self._prepare_visualization_data(X, cluster_labels)
            
            result = {
                'algorithm': 'K-Means',
                'n_clusters': n_clusters,
                'cluster_centers': kmeans.cluster_centers_.tolist(),
                'inertia': kmeans.inertia_,
                'metrics': metrics,
                'cluster_analysis': cluster_analysis,
                'visualization_data': viz_data,
                'model_path': model_path,
                'cluster_labels': cluster_labels.tolist(),
                'feature_names': self._get_feature_names()
            }
            
            return result
            
        except Exception as e:
            raise Exception(f"K-Means clustering failed: {str(e)}")
    
    def perform_agglomerative(self, n_clusters=3, linkage='ward'):
        """Perform Agglomerative clustering"""
        try:
            # Get preprocessed data
            X = self._get_feature_data()
            
            if X is None or len(X) == 0:
                raise ValueError("No preprocessed data available for clustering")
            
            # Initialize Agglomerative Clustering
            agg_clustering = AgglomerativeClustering(
                n_clusters=n_clusters,
                linkage=linkage
            )
            
            # Fit the model
            cluster_labels = agg_clustering.fit_predict(X)
            
            # Calculate clustering metrics
            metrics = self._calculate_clustering_metrics(X, cluster_labels, n_clusters)
            
            # Store results
            self._store_clustering_results(
                algorithm='Agglomerative',
                cluster_labels=cluster_labels,
                metrics=metrics,
                n_clusters=n_clusters,
                algorithm_params={'n_clusters': n_clusters, 'linkage': linkage}
            )
            
            # Generate cluster analysis
            cluster_analysis = self._analyze_clusters(X, cluster_labels, 'Agglomerative')
            
            # Dimensionality reduction for visualization
            viz_data = self._prepare_visualization_data(X, cluster_labels)
            
            result = {
                'algorithm': 'Agglomerative Clustering',
                'n_clusters': n_clusters,
                'linkage': linkage,
                'metrics': metrics,
                'cluster_analysis': cluster_analysis,
                'visualization_data': viz_data,
                'cluster_labels': cluster_labels.tolist(),
                'feature_names': self._get_feature_names()
            }
            
            return result
            
        except Exception as e:
            raise Exception(f"Agglomerative clustering failed: {str(e)}")
    
    def perform_dbscan(self, eps=0.5, min_samples=5):
        """Perform DBSCAN clustering"""
        try:
            # Get preprocessed data
            X = self._get_feature_data()
            
            if X is None or len(X) == 0:
                raise ValueError("No preprocessed data available for clustering")
            
            # Initialize DBSCAN
            dbscan = DBSCAN(
                eps=eps,
                min_samples=min_samples
            )
            
            # Fit the model
            cluster_labels = dbscan.fit_predict(X)
            
            # Get number of clusters (excluding noise points)
            n_clusters = len(set(cluster_labels)) - (1 if -1 in cluster_labels else 0)
            n_noise = list(cluster_labels).count(-1)
            
            # Calculate clustering metrics (excluding noise points for some metrics)
            if n_clusters > 1:
                # Create mask for non-noise points
                mask = cluster_labels != -1
                X_clustered = X[mask]
                labels_clustered = cluster_labels[mask]
                
                if len(X_clustered) > 1:
                    metrics = self._calculate_clustering_metrics(X_clustered, labels_clustered, n_clusters)
                else:
                    metrics = {'silhouette_score': -1, 'calinski_harabasz_score': 0, 'davies_bouldin_score': float('inf')}
            else:
                metrics = {'silhouette_score': -1, 'calinski_harabasz_score': 0, 'davies_bouldin_score': float('inf')}
            
            # Store results
            self._store_clustering_results(
                algorithm='DBSCAN',
                cluster_labels=cluster_labels,
                metrics=metrics,
                n_clusters=n_clusters,
                algorithm_params={'eps': eps, 'min_samples': min_samples}
            )
            
            # Generate cluster analysis
            cluster_analysis = self._analyze_clusters(X, cluster_labels, 'DBSCAN')
            
            # Dimensionality reduction for visualization
            viz_data = self._prepare_visualization_data(X, cluster_labels)
            
            result = {
                'algorithm': 'DBSCAN',
                'eps': eps,
                'min_samples': min_samples,
                'n_clusters': n_clusters,
                'n_noise_points': n_noise,
                'metrics': metrics,
                'cluster_analysis': cluster_analysis,
                'visualization_data': viz_data,
                'cluster_labels': cluster_labels.tolist(),
                'feature_names': self._get_feature_names()
            }
            
            return result
            
        except Exception as e:
            raise Exception(f"DBSCAN clustering failed: {str(e)}")
    
    def _get_feature_data(self):
        """Get preprocessed feature data for clustering"""
        try:
            # Get preprocessed data from database
            preprocessed_data = PreprocessedData.query.all()
            
            if not preprocessed_data:
                # If no data, try to load sample data
                self.preprocessing_service.load_sample_data()
                preprocessed_data = PreprocessedData.query.all()
            
            if not preprocessed_data:
                return None
            
            # Convert to numpy array
            feature_data = []
            for record in preprocessed_data:
                feature_data.append([
                    record.nitrogen_scaled,
                    record.phosphorus_scaled,
                    record.potassium_scaled,
                    record.temperature_scaled,
                    record.humidity_scaled,
                    record.ph_scaled,
                    record.rainfall_scaled
                ])
            
            return np.array(feature_data)
            
        except Exception as e:
            print(f"Error getting feature data: {str(e)}")
            return None
    
    def _get_feature_names(self):
        """Get feature names for clustering"""
        return ['nitrogen_scaled', 'phosphorus_scaled', 'potassium_scaled', 
                'temperature_scaled', 'humidity_scaled', 'ph_scaled', 'rainfall_scaled']
    
    def _calculate_clustering_metrics(self, X, labels, n_clusters):
        """Calculate comprehensive clustering metrics"""
        metrics = {}
        
        try:
            # Silhouette Score
            if len(set(labels)) > 1:
                metrics['silhouette_score'] = round(silhouette_score(X, labels), 4)
            else:
                metrics['silhouette_score'] = -1
            
            # Calinski-Harabasz Index (Variance Ratio Criterion)
            if len(set(labels)) > 1:
                metrics['calinski_harabasz_score'] = round(calinski_harabasz_score(X, labels), 4)
            else:
                metrics['calinski_harabasz_score'] = 0
            
            # Davies-Bouldin Index
            if len(set(labels)) > 1:
                metrics['davies_bouldin_score'] = round(davies_bouldin_score(X, labels), 4)
            else:
                metrics['davies_bouldin_score'] = float('inf')
            
            # Additional metrics
            metrics['n_clusters'] = n_clusters
            metrics['n_samples'] = len(X)
            
        except Exception as e:
            print(f"Error calculating clustering metrics: {str(e)}")
            metrics = {
                'silhouette_score': -1,
                'calinski_harabasz_score': 0,
                'davies_bouldin_score': float('inf'),
                'n_clusters': n_clusters,
                'n_samples': len(X)
            }
        
        return metrics
    
    def _analyze_clusters(self, X, labels, algorithm):
        """Analyze cluster characteristics"""
        analysis = {}
        
        try:
            unique_labels = set(labels)
            feature_names = self._get_feature_names()
            
            for label in unique_labels:
                if label == -1:  # Noise points in DBSCAN
                    label_name = 'noise'
                else:
                    label_name = f'cluster_{label}'
                
                mask = labels == label
                cluster_data = X[mask]
                
                if len(cluster_data) > 0:
                    # Calculate cluster statistics
                    cluster_stats = {}
                    for i, feature in enumerate(feature_names):
                        cluster_stats[feature] = {
                            'mean': round(np.mean(cluster_data[:, i]), 4),
                            'std': round(np.std(cluster_data[:, i]), 4),
                            'min': round(np.min(cluster_data[:, i]), 4),
                            'max': round(np.max(cluster_data[:, i]), 4)
                        }
                    
                    analysis[label_name] = {
                        'size': len(cluster_data),
                        'percentage': round(len(cluster_data) / len(X) * 100, 2),
                        'feature_stats': cluster_stats,
                        'centroid': np.mean(cluster_data, axis=0).tolist()
                    }
        
        except Exception as e:
            print(f"Error analyzing clusters: {str(e)}")
            analysis = {'error': str(e)}
        
        return analysis
    
    def _prepare_visualization_data(self, X, labels):
        """Prepare data for 2D/3D visualization using PCA and t-SNE"""
        viz_data = {}
        
        try:
            # PCA for 2D
            pca_2d = PCA(n_components=2, random_state=42)
            X_pca_2d = pca_2d.fit_transform(X)
            
            viz_data['pca_2d'] = {
                'coordinates': X_pca_2d.tolist(),
                'labels': labels.tolist(),
                'explained_variance_ratio': pca_2d.explained_variance_ratio_.tolist(),
                'components': pca_2d.components_.tolist()
            }
            
            # PCA for 3D
            if X.shape[1] >= 3:
                pca_3d = PCA(n_components=3, random_state=42)
                X_pca_3d = pca_3d.fit_transform(X)
                
                viz_data['pca_3d'] = {
                    'coordinates': X_pca_3d.tolist(),
                    'labels': labels.tolist(),
                    'explained_variance_ratio': pca_3d.explained_variance_ratio_.tolist()
                }
            
            # t-SNE for 2D (if dataset is not too large)
            if len(X) <= 1000:  # t-SNE can be slow for large datasets
                tsne = TSNE(n_components=2, random_state=42, perplexity=min(30, len(X)-1))
                X_tsne = tsne.fit_transform(X)
                
                viz_data['tsne_2d'] = {
                    'coordinates': X_tsne.tolist(),
                    'labels': labels.tolist()
                }
        
        except Exception as e:
            print(f"Error preparing visualization data: {str(e)}")
            viz_data = {'error': str(e)}
        
        return viz_data
    
    def _store_clustering_results(self, algorithm, cluster_labels, metrics, n_clusters, algorithm_params):
        """Store clustering results in database"""
        try:
            for i, label in enumerate(cluster_labels):
                cluster_record = ClusterResult(
                    clustering_algorithm=algorithm,
                    cluster_id=int(label),
                    cluster_label=f'{algorithm}_cluster_{label}' if label != -1 else f'{algorithm}_noise',
                    silhouette_score=metrics.get('silhouette_score'),
                    distance_to_centroid=None,  # Could be calculated if needed
                    n_clusters=n_clusters,
                    algorithm_params=json.dumps(algorithm_params)
                )
                db.session.add(cluster_record)
            
            db.session.commit()
            
        except Exception as e:
            print(f"Warning: Could not store clustering results in database: {str(e)}")
    
    def find_optimal_clusters(self, max_clusters=10):
        """Find optimal number of clusters using elbow method and silhouette analysis"""
        try:
            X = self._get_feature_data()
            
            if X is None or len(X) == 0:
                raise ValueError("No data available for cluster optimization")
            
            results = {
                'elbow_method': {'k_values': [], 'inertias': []},
                'silhouette_method': {'k_values': [], 'silhouette_scores': []}
            }
            
            # Test different numbers of clusters
            k_range = range(2, min(max_clusters + 1, len(X)))
            
            for k in k_range:
                # K-Means for elbow method
                kmeans = KMeans(n_clusters=k, random_state=42)
                kmeans.fit(X)
                
                results['elbow_method']['k_values'].append(k)
                results['elbow_method']['inertias'].append(kmeans.inertia_)
                
                # Silhouette score
                silhouette = silhouette_score(X, kmeans.labels_)
                results['silhouette_method']['k_values'].append(k)
                results['silhouette_method']['silhouette_scores'].append(silhouette)
            
            # Find optimal k using silhouette score
            optimal_k_idx = np.argmax(results['silhouette_method']['silhouette_scores'])
            optimal_k = results['silhouette_method']['k_values'][optimal_k_idx]
            
            results['recommended_k'] = optimal_k
            results['best_silhouette_score'] = max(results['silhouette_method']['silhouette_scores'])
            
            return results
            
        except Exception as e:
            raise Exception(f"Cluster optimization failed: {str(e)}")
    
    def compare_clustering_algorithms(self, n_clusters=3):
        """Compare all clustering algorithms"""
        try:
            # Perform all clustering algorithms
            kmeans_result = self.perform_kmeans(n_clusters)
            agg_result = self.perform_agglomerative(n_clusters)
            dbscan_result = self.perform_dbscan()
            
            # Create comparison
            comparison = {
                'kmeans': {
                    'algorithm': 'K-Means',
                    'silhouette_score': kmeans_result['metrics']['silhouette_score'],
                    'calinski_harabasz_score': kmeans_result['metrics']['calinski_harabasz_score'],
                    'davies_bouldin_score': kmeans_result['metrics']['davies_bouldin_score'],
                    'n_clusters': kmeans_result['n_clusters']
                },
                'agglomerative': {
                    'algorithm': 'Agglomerative',
                    'silhouette_score': agg_result['metrics']['silhouette_score'],
                    'calinski_harabasz_score': agg_result['metrics']['calinski_harabasz_score'],
                    'davies_bouldin_score': agg_result['metrics']['davies_bouldin_score'],
                    'n_clusters': agg_result['n_clusters']
                },
                'dbscan': {
                    'algorithm': 'DBSCAN',
                    'silhouette_score': dbscan_result['metrics']['silhouette_score'],
                    'calinski_harabasz_score': dbscan_result['metrics']['calinski_harabasz_score'],
                    'davies_bouldin_score': dbscan_result['metrics']['davies_bouldin_score'],
                    'n_clusters': dbscan_result['n_clusters'],
                    'n_noise_points': dbscan_result['n_noise_points']
                }
            }
            
            # Determine best algorithm based on silhouette score
            best_algorithm = max(comparison.items(), 
                               key=lambda x: x[1]['silhouette_score'] if x[1]['silhouette_score'] != -1 else -2)
            
            return {
                'comparison': comparison,
                'best_algorithm': {
                    'name': best_algorithm[0],
                    'silhouette_score': best_algorithm[1]['silhouette_score']
                },
                'detailed_results': {
                    'kmeans': kmeans_result,
                    'agglomerative': agg_result,
                    'dbscan': dbscan_result
                }
            }
            
        except Exception as e:
            raise Exception(f"Clustering comparison failed: {str(e)}")