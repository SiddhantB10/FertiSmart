"""
Analytics Service for FertiSmart
Business Intelligence and analytical insights
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy import func, text
from app.models.database_models import *
from app import db

class AnalyticsService:
    """Business Intelligence and Analytics Service"""
    
    def __init__(self):
        pass
    
    def get_overview_stats(self):
        """Get high-level overview statistics"""
        try:
            stats = {}
            
            # Total samples
            total_samples = db.session.query(SoilTestFact).count()
            stats['total_samples'] = total_samples
            
            # Unique regions
            unique_regions = db.session.query(RegionDim).count()
            stats['unique_regions'] = unique_regions
            
            # Crop varieties
            unique_crops = db.session.query(CropDim).count()
            stats['unique_crops'] = unique_crops
            
            # Fertilizer types
            unique_fertilizers = db.session.query(FertilizerDim).count()
            stats['unique_fertilizers'] = unique_fertilizers
            
            # Recent activity (last 30 days)
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            recent_samples = db.session.query(SoilTestFact).filter(
                SoilTestFact.created_at >= thirty_days_ago
            ).count()
            stats['recent_samples'] = recent_samples
            
            # Data quality metrics
            quality_metrics = db.session.query(DataQualityMetrics).order_by(
                DataQualityMetrics.analyzed_at.desc()
            ).first()
            
            if quality_metrics:
                stats['data_quality'] = {
                    'quality_score': quality_metrics.quality_score,
                    'total_records': quality_metrics.total_records,
                    'missing_values': quality_metrics.missing_values,
                    'last_updated': quality_metrics.analyzed_at.isoformat()
                }
            
            return stats
            
        except Exception as e:
            return {'error': f'Overview statistics failed: {str(e)}'}
    
    def analyze_nutrients(self):
        """Analyze nutrient distribution and patterns"""
        try:
            # Get nutrient statistics
            nutrient_stats = db.session.query(
                func.avg(SoilTestFact.nitrogen).label('avg_nitrogen'),
                func.avg(SoilTestFact.phosphorus).label('avg_phosphorus'),
                func.avg(SoilTestFact.potassium).label('avg_potassium'),
                func.min(SoilTestFact.nitrogen).label('min_nitrogen'),
                func.max(SoilTestFact.nitrogen).label('max_nitrogen'),
                func.min(SoilTestFact.phosphorus).label('min_phosphorus'),
                func.max(SoilTestFact.phosphorus).label('max_phosphorus'),
                func.min(SoilTestFact.potassium).label('min_potassium'),
                func.max(SoilTestFact.potassium).label('max_potassium')
            ).first()
            
            analysis = {}
            
            if nutrient_stats:
                analysis['averages'] = {
                    'nitrogen': round(nutrient_stats.avg_nitrogen or 0, 2),
                    'phosphorus': round(nutrient_stats.avg_phosphorus or 0, 2),
                    'potassium': round(nutrient_stats.avg_potassium or 0, 2)
                }
                
                analysis['ranges'] = {
                    'nitrogen': {
                        'min': round(nutrient_stats.min_nitrogen or 0, 2),
                        'max': round(nutrient_stats.max_nitrogen or 0, 2)
                    },
                    'phosphorus': {
                        'min': round(nutrient_stats.min_phosphorus or 0, 2),
                        'max': round(nutrient_stats.max_phosphorus or 0, 2)
                    },
                    'potassium': {
                        'min': round(nutrient_stats.min_potassium or 0, 2),
                        'max': round(nutrient_stats.max_potassium or 0, 2)
                    }
                }
            
            # Nutrient deficiency analysis
            deficiency_analysis = self._analyze_nutrient_deficiencies()
            analysis['deficiency_analysis'] = deficiency_analysis
            
            # NPK ratio analysis
            npk_ratios = self._analyze_npk_ratios()
            analysis['npk_ratios'] = npk_ratios
            
            return analysis
            
        except Exception as e:
            return {'error': f'Nutrient analysis failed: {str(e)}'}
    
    def get_regional_insights(self):
        """Get regional agricultural insights"""
        try:
            # Regional nutrient averages
            regional_data = db.session.query(
                RegionDim.region_name,
                RegionDim.state,
                func.avg(SoilTestFact.nitrogen).label('avg_nitrogen'),
                func.avg(SoilTestFact.phosphorus).label('avg_phosphorus'),
                func.avg(SoilTestFact.potassium).label('avg_potassium'),
                func.avg(SoilTestFact.ph).label('avg_ph'),
                func.count(SoilTestFact.id).label('sample_count')
            ).join(
                SoilTestFact, RegionDim.region_id == SoilTestFact.region_id
            ).group_by(
                RegionDim.region_name, RegionDim.state
            ).all()
            
            regional_insights = []
            
            for region in regional_data:
                insight = {
                    'region_name': region.region_name,
                    'state': region.state,
                    'sample_count': region.sample_count,
                    'nutrient_profile': {
                        'nitrogen': round(region.avg_nitrogen or 0, 2),
                        'phosphorus': round(region.avg_phosphorus or 0, 2),
                        'potassium': round(region.avg_potassium or 0, 2),
                        'ph': round(region.avg_ph or 0, 2)
                    },
                    'fertility_rating': self._calculate_regional_fertility(region)
                }
                regional_insights.append(insight)
            
            # Sort by sample count
            regional_insights.sort(key=lambda x: x['sample_count'], reverse=True)
            
            return {
                'regional_data': regional_insights,
                'top_regions': regional_insights[:5],
                'summary': self._summarize_regional_data(regional_insights)
            }
            
        except Exception as e:
            return {'error': f'Regional analysis failed: {str(e)}'}
    
    def get_crop_fertilizer_trends(self):
        """Analyze crop and fertilizer usage trends"""
        try:
            # Most common crops
            crop_data = db.session.query(
                CropDim.crop_name,
                CropDim.season,
                func.count(SoilTestFact.id).label('usage_count')
            ).join(
                SoilTestFact, CropDim.crop_id == SoilTestFact.crop_id
            ).group_by(
                CropDim.crop_name, CropDim.season
            ).order_by(
                func.count(SoilTestFact.id).desc()
            ).all()
            
            # Most used fertilizers
            fertilizer_data = db.session.query(
                FertilizerDim.fertilizer_name,
                FertilizerDim.fertilizer_type,
                func.count(SoilTestFact.id).label('usage_count')
            ).join(
                SoilTestFact, FertilizerDim.fertilizer_id == SoilTestFact.fertilizer_id
            ).group_by(
                FertilizerDim.fertilizer_name, FertilizerDim.fertilizer_type
            ).order_by(
                func.count(SoilTestFact.id).desc()
            ).all()
            
            trends = {
                'popular_crops': [
                    {
                        'crop_name': crop.crop_name,
                        'season': crop.season,
                        'usage_count': crop.usage_count
                    } for crop in crop_data[:10]
                ],
                'popular_fertilizers': [
                    {
                        'fertilizer_name': fert.fertilizer_name,
                        'fertilizer_type': fert.fertilizer_type,
                        'usage_count': fert.usage_count
                    } for fert in fertilizer_data[:10]
                ]
            }
            
            # Crop-fertilizer combinations
            combinations = self._analyze_crop_fertilizer_combinations()
            trends['crop_fertilizer_combinations'] = combinations
            
            return trends
            
        except Exception as e:
            return {'error': f'Trend analysis failed: {str(e)}'}
    
    def get_seasonal_patterns(self):
        """Analyze seasonal patterns in soil data"""
        try:
            # Monthly soil test patterns
            monthly_data = db.session.query(
                func.extract('month', SoilTestFact.created_at).label('month'),
                func.avg(SoilTestFact.nitrogen).label('avg_nitrogen'),
                func.avg(SoilTestFact.phosphorus).label('avg_phosphorus'),
                func.avg(SoilTestFact.potassium).label('avg_potassium'),
                func.avg(SoilTestFact.temperature).label('avg_temperature'),
                func.avg(SoilTestFact.humidity).label('avg_humidity'),
                func.avg(SoilTestFact.rainfall).label('avg_rainfall'),
                func.count(SoilTestFact.id).label('test_count')
            ).group_by(
                func.extract('month', SoilTestFact.created_at)
            ).order_by('month').all()
            
            seasonal_patterns = []
            
            for month_data in monthly_data:
                pattern = {
                    'month': int(month_data.month) if month_data.month else 0,
                    'month_name': self._get_month_name(int(month_data.month) if month_data.month else 0),
                    'test_count': month_data.test_count,
                    'averages': {
                        'nitrogen': round(month_data.avg_nitrogen or 0, 2),
                        'phosphorus': round(month_data.avg_phosphorus or 0, 2),
                        'potassium': round(month_data.avg_potassium or 0, 2),
                        'temperature': round(month_data.avg_temperature or 0, 2),
                        'humidity': round(month_data.avg_humidity or 0, 2),
                        'rainfall': round(month_data.avg_rainfall or 0, 2)
                    }
                }
                seasonal_patterns.append(pattern)
            
            # Seasonal crop preferences
            seasonal_crops = self._analyze_seasonal_crop_preferences()
            
            return {
                'monthly_patterns': seasonal_patterns,
                'seasonal_crops': seasonal_crops,
                'insights': self._generate_seasonal_insights(seasonal_patterns)
            }
            
        except Exception as e:
            return {'error': f'Seasonal analysis failed: {str(e)}'}
    
    def get_model_performance_analytics(self):
        """Analyze ML model performance metrics"""
        try:
            # Get model prediction statistics
            model_stats = db.session.query(
                ModelPrediction.model_name,
                func.avg(ModelPrediction.accuracy).label('avg_accuracy'),
                func.avg(ModelPrediction.precision).label('avg_precision'),
                func.avg(ModelPrediction.recall).label('avg_recall'),
                func.avg(ModelPrediction.f1_score).label('avg_f1_score'),
                func.count(ModelPrediction.id).label('prediction_count')
            ).group_by(
                ModelPrediction.model_name
            ).all()
            
            performance_analytics = []
            
            for model in model_stats:
                analytics = {
                    'model_name': model.model_name,
                    'prediction_count': model.prediction_count,
                    'performance_metrics': {
                        'accuracy': round(model.avg_accuracy or 0, 4),
                        'precision': round(model.avg_precision or 0, 4),
                        'recall': round(model.avg_recall or 0, 4),
                        'f1_score': round(model.avg_f1_score or 0, 4)
                    }
                }
                performance_analytics.append(analytics)
            
            # Clustering performance
            clustering_stats = self._analyze_clustering_performance()
            
            return {
                'classification_models': performance_analytics,
                'clustering_analysis': clustering_stats,
                'model_recommendations': self._generate_model_recommendations(performance_analytics)
            }
            
        except Exception as e:
            return {'error': f'Model performance analysis failed: {str(e)}'}
    
    def _analyze_nutrient_deficiencies(self):
        """Analyze nutrient deficiency patterns"""
        try:
            # Define deficiency thresholds
            thresholds = {
                'nitrogen': 30,
                'phosphorus': 20,
                'potassium': 25
            }
            
            deficiencies = {}
            
            for nutrient, threshold in thresholds.items():
                if nutrient == 'nitrogen':
                    column = SoilTestFact.nitrogen
                elif nutrient == 'phosphorus':
                    column = SoilTestFact.phosphorus
                else:
                    column = SoilTestFact.potassium
                
                total_samples = db.session.query(SoilTestFact).count()
                deficient_samples = db.session.query(SoilTestFact).filter(
                    column < threshold
                ).count()
                
                deficiency_percentage = (deficient_samples / total_samples * 100) if total_samples > 0 else 0
                
                deficiencies[nutrient] = {
                    'threshold': threshold,
                    'deficient_samples': deficient_samples,
                    'total_samples': total_samples,
                    'deficiency_percentage': round(deficiency_percentage, 2)
                }
            
            return deficiencies
            
        except Exception as e:
            return {'error': str(e)}
    
    def _analyze_npk_ratios(self):
        """Analyze NPK ratio patterns"""
        try:
            # Get NPK data
            npk_data = db.session.query(
                SoilTestFact.nitrogen,
                SoilTestFact.phosphorus,
                SoilTestFact.potassium
            ).all()
            
            if not npk_data:
                return {'message': 'No NPK data available'}
            
            # Calculate ratios
            ratios = []
            for data in npk_data:
                if data.nitrogen and data.phosphorus and data.potassium:
                    # Normalize to smallest value
                    min_val = min(data.nitrogen, data.phosphorus, data.potassium)
                    if min_val > 0:
                        n_ratio = data.nitrogen / min_val
                        p_ratio = data.phosphorus / min_val
                        k_ratio = data.potassium / min_val
                        ratios.append({
                            'N': round(n_ratio, 2),
                            'P': round(p_ratio, 2),
                            'K': round(k_ratio, 2)
                        })
            
            if ratios:
                # Calculate average ratios
                avg_ratios = {
                    'N': round(sum(r['N'] for r in ratios) / len(ratios), 2),
                    'P': round(sum(r['P'] for r in ratios) / len(ratios), 2),
                    'K': round(sum(r['K'] for r in ratios) / len(ratios), 2)
                }
                
                return {
                    'average_ratio': f"{avg_ratios['N']}:{avg_ratios['P']}:{avg_ratios['K']}",
                    'sample_count': len(ratios),
                    'ratio_analysis': avg_ratios
                }
            
            return {'message': 'Insufficient data for ratio calculation'}
            
        except Exception as e:
            return {'error': str(e)}
    
    def _calculate_regional_fertility(self, region_data):
        """Calculate fertility rating for a region"""
        try:
            # Simple fertility scoring based on NPK levels
            n_score = min((region_data.avg_nitrogen or 0) / 60, 1.0)
            p_score = min((region_data.avg_phosphorus or 0) / 40, 1.0)
            k_score = min((region_data.avg_potassium or 0) / 50, 1.0)
            
            # pH score (optimal around 6.5-7.0)
            ph = region_data.avg_ph or 6.5
            if 6.5 <= ph <= 7.0:
                ph_score = 1.0
            elif 6.0 <= ph < 6.5 or 7.0 < ph <= 7.5:
                ph_score = 0.8
            else:
                ph_score = 0.6
            
            fertility_score = (n_score + p_score + k_score + ph_score) / 4 * 100
            
            if fertility_score >= 80:
                return 'Excellent'
            elif fertility_score >= 60:
                return 'Good'
            elif fertility_score >= 40:
                return 'Fair'
            else:
                return 'Poor'
                
        except Exception as e:
            return 'Unknown'
    
    def _summarize_regional_data(self, regional_data):
        """Summarize regional data"""
        if not regional_data:
            return {'message': 'No regional data available'}
        
        # Count fertility ratings
        rating_counts = {}
        for region in regional_data:
            rating = region['fertility_rating']
            rating_counts[rating] = rating_counts.get(rating, 0) + 1
        
        # Most fertile region
        fertile_regions = [r for r in regional_data if r['fertility_rating'] == 'Excellent']
        most_fertile = fertile_regions[0]['region_name'] if fertile_regions else 'None'
        
        return {
            'total_regions': len(regional_data),
            'fertility_distribution': rating_counts,
            'most_fertile_region': most_fertile,
            'average_samples_per_region': round(sum(r['sample_count'] for r in regional_data) / len(regional_data), 1)
        }
    
    def _analyze_crop_fertilizer_combinations(self):
        """Analyze popular crop-fertilizer combinations"""
        try:
            combinations = db.session.query(
                CropDim.crop_name,
                FertilizerDim.fertilizer_name,
                func.count(SoilTestFact.id).label('combination_count')
            ).join(
                SoilTestFact, CropDim.crop_id == SoilTestFact.crop_id
            ).join(
                FertilizerDim, FertilizerDim.fertilizer_id == SoilTestFact.fertilizer_id
            ).group_by(
                CropDim.crop_name, FertilizerDim.fertilizer_name
            ).order_by(
                func.count(SoilTestFact.id).desc()
            ).limit(10).all()
            
            return [
                {
                    'crop': combo.crop_name,
                    'fertilizer': combo.fertilizer_name,
                    'usage_count': combo.combination_count
                } for combo in combinations
            ]
            
        except Exception as e:
            return []
    
    def _analyze_seasonal_crop_preferences(self):
        """Analyze seasonal crop preferences"""
        try:
            seasonal_data = db.session.query(
                CropDim.season,
                CropDim.crop_name,
                func.count(SoilTestFact.id).label('crop_count')
            ).join(
                SoilTestFact, CropDim.crop_id == SoilTestFact.crop_id
            ).group_by(
                CropDim.season, CropDim.crop_name
            ).order_by(
                CropDim.season, func.count(SoilTestFact.id).desc()
            ).all()
            
            seasons = {}
            for data in seasonal_data:
                if data.season not in seasons:
                    seasons[data.season] = []
                seasons[data.season].append({
                    'crop_name': data.crop_name,
                    'usage_count': data.crop_count
                })
            
            return seasons
            
        except Exception as e:
            return {}
    
    def _generate_seasonal_insights(self, seasonal_patterns):
        """Generate insights from seasonal patterns"""
        if not seasonal_patterns:
            return []
        
        insights = []
        
        # Find peak testing months
        test_counts = [p['test_count'] for p in seasonal_patterns]
        if test_counts:
            max_tests = max(test_counts)
            peak_months = [p['month_name'] for p in seasonal_patterns if p['test_count'] == max_tests]
            insights.append(f"Peak soil testing occurs in: {', '.join(peak_months)}")
        
        # Temperature trends
        temps = [p['averages']['temperature'] for p in seasonal_patterns if p['averages']['temperature'] > 0]
        if temps:
            avg_temp = sum(temps) / len(temps)
            insights.append(f"Average temperature across seasons: {avg_temp:.1f}°C")
        
        return insights
    
    def _analyze_clustering_performance(self):
        """Analyze clustering performance"""
        try:
            cluster_stats = db.session.query(
                ClusterResult.clustering_algorithm,
                func.avg(ClusterResult.silhouette_score).label('avg_silhouette'),
                func.count(ClusterResult.id).label('cluster_count')
            ).group_by(
                ClusterResult.clustering_algorithm
            ).all()
            
            return [
                {
                    'algorithm': stat.clustering_algorithm,
                    'average_silhouette_score': round(stat.avg_silhouette or 0, 4),
                    'cluster_count': stat.cluster_count
                } for stat in cluster_stats
            ]
            
        except Exception as e:
            return []
    
    def _generate_model_recommendations(self, performance_data):
        """Generate model recommendations based on performance"""
        if not performance_data:
            return []
        
        recommendations = []
        
        # Find best performing model
        best_model = max(performance_data, key=lambda x: x['performance_metrics']['f1_score'])
        recommendations.append(f"Best performing model: {best_model['model_name']} (F1: {best_model['performance_metrics']['f1_score']})")
        
        # Check for models needing improvement
        poor_models = [m for m in performance_data if m['performance_metrics']['accuracy'] < 0.7]
        if poor_models:
            recommendations.append(f"Models needing improvement: {', '.join([m['model_name'] for m in poor_models])}")
        
        return recommendations
    
    def _get_month_name(self, month_num):
        """Get month name from number"""
        months = {
            1: 'January', 2: 'February', 3: 'March', 4: 'April',
            5: 'May', 6: 'June', 7: 'July', 8: 'August',
            9: 'September', 10: 'October', 11: 'November', 12: 'December'
        }
        return months.get(month_num, 'Unknown')