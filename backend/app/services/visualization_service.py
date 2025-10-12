"""
Visualization Service for FertiSmart
Handles EDA visualizations and data insights (Experiment 3)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
import base64
from io import BytesIO
import os
from datetime import datetime

from app.models.database_models import SoilTestFact, RegionDim, CropDim, FertilizerDim
from app.services.preprocessing_service import PreprocessingService
from app import db

class VisualizationService:
    """Data Visualization and EDA Service"""
    
    def __init__(self):
        self.preprocessing_service = PreprocessingService()
        self.viz_path = 'static/visualizations'
        os.makedirs(self.viz_path, exist_ok=True)
        
        # Set style for matplotlib
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
    
    def generate_correlation_matrix(self):
        """Generate correlation matrix heatmap"""
        try:
            # Get soil test data
            df = self._get_soil_data()
            
            if df.empty:
                return {'error': 'No data available for correlation analysis'}
            
            # Select numerical columns
            numerical_cols = ['nitrogen', 'phosphorus', 'potassium', 'temperature', 
                            'humidity', 'ph', 'rainfall']
            
            # Filter existing columns
            available_cols = [col for col in numerical_cols if col in df.columns]
            
            if len(available_cols) < 2:
                return {'error': 'Insufficient numerical columns for correlation analysis'}
            
            # Calculate correlation matrix
            corr_matrix = df[available_cols].corr()
            
            # Create matplotlib heatmap
            plt.figure(figsize=(10, 8))
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                       square=True, linewidths=0.5)
            plt.title('Soil Nutrient Correlation Matrix')
            plt.tight_layout()
            
            # Save matplotlib plot
            img_path = os.path.join(self.viz_path, 'correlation_matrix.png')
            plt.savefig(img_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            # Create Plotly interactive heatmap
            fig = go.Figure(data=go.Heatmap(
                z=corr_matrix.values,
                x=corr_matrix.columns,
                y=corr_matrix.columns,
                colorscale='RdBu',
                zmid=0,
                text=corr_matrix.round(3).values,
                texttemplate="%{text}",
                textfont={"size": 10},
                hoverongaps=False
            ))
            
            fig.update_layout(
                title='Soil Nutrient Correlation Matrix',
                xaxis_title='Features',
                yaxis_title='Features',
                width=600,
                height=500
            )
            
            # Convert to JSON
            plotly_json = json.loads(fig.to_json())
            
            return {
                'correlation_matrix': corr_matrix.to_dict(),
                'plotly_chart': plotly_json,
                'static_image_path': img_path,
                'insights': self._analyze_correlations(corr_matrix)
            }
            
        except Exception as e:
            return {'error': f'Correlation analysis failed: {str(e)}'}
    
    def generate_nutrient_distribution(self):
        """Generate nutrient distribution plots"""
        try:
            df = self._get_soil_data()
            
            if df.empty:
                return {'error': 'No data available for distribution analysis'}
            
            nutrients = ['nitrogen', 'phosphorus', 'potassium']
            available_nutrients = [n for n in nutrients if n in df.columns]
            
            if not available_nutrients:
                return {'error': 'No nutrient data available'}
            
            # Create distribution plots
            distributions = {}
            
            for nutrient in available_nutrients:
                # Statistical summary
                stats = {
                    'mean': df[nutrient].mean(),
                    'median': df[nutrient].median(),
                    'std': df[nutrient].std(),
                    'min': df[nutrient].min(),
                    'max': df[nutrient].max(),
                    'quartiles': df[nutrient].quantile([0.25, 0.5, 0.75]).to_dict()
                }
                
                # Create Plotly histogram
                fig = go.Figure()
                
                fig.add_trace(go.Histogram(
                    x=df[nutrient],
                    nbinsx=30,
                    name=f'{nutrient.title()} Distribution',
                    opacity=0.7
                ))
                
                # Add mean line
                fig.add_vline(
                    x=stats['mean'],
                    line_dash="dash",
                    line_color="red",
                    annotation_text=f"Mean: {stats['mean']:.2f}"
                )
                
                fig.update_layout(
                    title=f'{nutrient.title()} Distribution',
                    xaxis_title=f'{nutrient.title()} Content',
                    yaxis_title='Frequency',
                    showlegend=False,
                    width=400,
                    height=300
                )
                
                distributions[nutrient] = {
                    'statistics': stats,
                    'plotly_chart': json.loads(fig.to_json())
                }
            
            # Create combined box plot
            fig_box = go.Figure()
            
            for nutrient in available_nutrients:
                fig_box.add_trace(go.Box(
                    y=df[nutrient],
                    name=nutrient.title(),
                    boxpoints='outliers'
                ))
            
            fig_box.update_layout(
                title='Nutrient Content Box Plot Comparison',
                yaxis_title='Content Level',
                width=600,
                height=400
            )
            
            return {
                'distributions': distributions,
                'combined_boxplot': json.loads(fig_box.to_json()),
                'summary_insights': self._analyze_distributions(df, available_nutrients)
            }
            
        except Exception as e:
            return {'error': f'Distribution analysis failed: {str(e)}'}
    
    def generate_trend_analysis(self):
        """Generate trend analysis plots"""
        try:
            df = self._get_soil_data_with_time()
            
            if df.empty:
                return {'error': 'No temporal data available for trend analysis'}
            
            # Create trend plots
            trends = {}
            
            # Nutrient trends over time
            nutrients = ['nitrogen', 'phosphorus', 'potassium']
            available_nutrients = [n for n in nutrients if n in df.columns]
            
            if available_nutrients and 'date' in df.columns:
                # Monthly aggregation
                df['month'] = pd.to_datetime(df['date']).dt.to_period('M')
                monthly_data = df.groupby('month')[available_nutrients].mean()
                
                fig = go.Figure()
                
                for nutrient in available_nutrients:
                    fig.add_trace(go.Scatter(
                        x=monthly_data.index.astype(str),
                        y=monthly_data[nutrient],
                        mode='lines+markers',
                        name=nutrient.title(),
                        line=dict(width=2)
                    ))
                
                fig.update_layout(
                    title='Nutrient Trends Over Time',
                    xaxis_title='Month',
                    yaxis_title='Average Content',
                    width=800,
                    height=400,
                    hovermode='x unified'
                )
                
                trends['nutrient_trends'] = json.loads(fig.to_json())
            
            # Environmental factor analysis
            environmental_factors = ['temperature', 'humidity', 'ph', 'rainfall']
            available_env = [f for f in environmental_factors if f in df.columns]
            
            if available_env:
                # Create environmental correlation with nutrients
                correlations = {}
                
                for env_factor in available_env:
                    for nutrient in available_nutrients:
                        if env_factor in df.columns and nutrient in df.columns:
                            corr = df[env_factor].corr(df[nutrient])
                            correlations[f'{env_factor}_{nutrient}'] = corr
                
                trends['environmental_correlations'] = correlations
            
            return {
                'trends': trends,
                'insights': self._analyze_trends(df)
            }
            
        except Exception as e:
            return {'error': f'Trend analysis failed: {str(e)}'}
    
    def generate_summary_stats(self):
        """Generate comprehensive summary statistics"""
        try:
            df = self._get_soil_data()
            
            if df.empty:
                return {'error': 'No data available for summary statistics'}
            
            # Overall dataset summary
            summary = {
                'dataset_info': {
                    'total_samples': len(df),
                    'features': len(df.columns),
                    'numerical_features': len(df.select_dtypes(include=[np.number]).columns),
                    'categorical_features': len(df.select_dtypes(include=['object']).columns)
                }
            }
            
            # Numerical summary
            numerical_cols = df.select_dtypes(include=[np.number]).columns
            if len(numerical_cols) > 0:
                summary['numerical_summary'] = df[numerical_cols].describe().to_dict()
            
            # Categorical summary
            categorical_cols = df.select_dtypes(include=['object']).columns
            if len(categorical_cols) > 0:
                cat_summary = {}
                for col in categorical_cols:
                    cat_summary[col] = {
                        'unique_values': df[col].nunique(),
                        'most_frequent': df[col].mode().iloc[0] if not df[col].mode().empty else None,
                        'value_counts': df[col].value_counts().head().to_dict()
                    }
                summary['categorical_summary'] = cat_summary
            
            # Missing values analysis
            missing_data = df.isnull().sum()
            if missing_data.sum() > 0:
                summary['missing_data'] = missing_data.to_dict()
            
            # Data quality indicators
            summary['quality_indicators'] = {
                'completeness': (1 - df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100,
                'duplicates': df.duplicated().sum(),
                'unique_samples': len(df.drop_duplicates())
            }
            
            return summary
            
        except Exception as e:
            return {'error': f'Summary statistics failed: {str(e)}'}
    
    def create_dashboard_charts(self):
        """Create comprehensive dashboard charts"""
        try:
            df = self._get_soil_data()
            
            if df.empty:
                return {'error': 'No data available for dashboard'}
            
            charts = {}
            
            # 1. Nutrient Level Gauge Charts
            nutrients = ['nitrogen', 'phosphorus', 'potassium']
            for nutrient in nutrients:
                if nutrient in df.columns:
                    avg_value = df[nutrient].mean()
                    max_value = df[nutrient].max()
                    
                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number+delta",
                        value = avg_value,
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        title = {'text': f"Average {nutrient.title()}"},
                        delta = {'reference': max_value * 0.7},
                        gauge = {
                            'axis': {'range': [None, max_value]},
                            'bar': {'color': "darkblue"},
                            'steps': [
                                {'range': [0, max_value * 0.5], 'color': "lightgray"},
                                {'range': [max_value * 0.5, max_value * 0.8], 'color': "gray"}],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': max_value * 0.9}
                        }
                    ))
                    
                    fig.update_layout(width=300, height=250)
                    charts[f'{nutrient}_gauge'] = json.loads(fig.to_json())
            
            # 2. pH Distribution Pie Chart
            if 'ph' in df.columns:
                # Categorize pH levels
                df['ph_category'] = pd.cut(df['ph'], 
                                         bins=[0, 6.0, 7.0, 8.0, 14], 
                                         labels=['Acidic', 'Slightly Acidic', 'Neutral', 'Alkaline'])
                
                ph_counts = df['ph_category'].value_counts()
                
                fig = go.Figure(data=[go.Pie(
                    labels=ph_counts.index,
                    values=ph_counts.values,
                    hole=.3
                )])
                
                fig.update_layout(
                    title='Soil pH Distribution',
                    width=400,
                    height=400
                )
                
                charts['ph_distribution'] = json.loads(fig.to_json())
            
            # 3. Environmental Factors Radar Chart
            env_factors = ['temperature', 'humidity', 'rainfall']
            available_env = [f for f in env_factors if f in df.columns]
            
            if len(available_env) >= 3:
                # Normalize values to 0-1 scale for radar chart
                normalized_values = []
                for factor in available_env:
                    normalized_values.append(
                        (df[factor].mean() - df[factor].min()) / 
                        (df[factor].max() - df[factor].min())
                    )
                
                fig = go.Figure()
                
                fig.add_trace(go.Scatterpolar(
                    r=normalized_values + [normalized_values[0]],  # Close the shape
                    theta=available_env + [available_env[0]],
                    fill='toself',
                    name='Average Conditions'
                ))
                
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 1]
                        )
                    ),
                    showlegend=True,
                    title='Environmental Factors Radar',
                    width=400,
                    height=400
                )
                
                charts['environmental_radar'] = json.loads(fig.to_json())
            
            return {
                'dashboard_charts': charts,
                'chart_count': len(charts)
            }
            
        except Exception as e:
            return {'error': f'Dashboard creation failed: {str(e)}'}
    
    def _get_soil_data(self):
        """Get soil test data from database or sample data"""
        try:
            # Try to get data from database
            soil_tests = db.session.query(
                SoilTestFact.nitrogen,
                SoilTestFact.phosphorus,
                SoilTestFact.potassium,
                SoilTestFact.temperature,
                SoilTestFact.humidity,
                SoilTestFact.ph,
                SoilTestFact.rainfall
            ).all()
            
            if soil_tests:
                df = pd.DataFrame(soil_tests)
                return df
            else:
                # Use sample data if no database data
                return self._create_sample_data()
                
        except Exception as e:
            print(f"Error getting soil data: {str(e)}")
            return self._create_sample_data()
    
    def _get_soil_data_with_time(self):
        """Get soil test data with time information"""
        try:
            # Join with time dimension
            query = db.session.query(
                SoilTestFact.nitrogen,
                SoilTestFact.phosphorus,
                SoilTestFact.potassium,
                SoilTestFact.temperature,
                SoilTestFact.humidity,
                SoilTestFact.ph,
                SoilTestFact.rainfall,
                SoilTestFact.created_at
            ).all()
            
            if query:
                df = pd.DataFrame(query)
                df['date'] = df['created_at']
                return df
            else:
                return self._create_sample_temporal_data()
                
        except Exception as e:
            print(f"Error getting temporal data: {str(e)}")
            return self._create_sample_temporal_data()
    
    def _create_sample_data(self):
        """Create sample data for visualization"""
        np.random.seed(42)
        n_samples = 100
        
        data = {
            'nitrogen': np.random.normal(50, 15, n_samples),
            'phosphorus': np.random.normal(30, 10, n_samples),
            'potassium': np.random.normal(40, 12, n_samples),
            'temperature': np.random.normal(25, 5, n_samples),
            'humidity': np.random.normal(70, 15, n_samples),
            'ph': np.random.normal(6.5, 1, n_samples),
            'rainfall': np.random.normal(150, 50, n_samples)
        }
        
        return pd.DataFrame(data)
    
    def _create_sample_temporal_data(self):
        """Create sample temporal data"""
        df = self._create_sample_data()
        
        # Add date column
        dates = pd.date_range(start='2023-01-01', periods=len(df), freq='D')
        df['date'] = dates
        df['created_at'] = dates
        
        return df
    
    def _analyze_correlations(self, corr_matrix):
        """Analyze correlation patterns"""
        insights = []
        
        # Find strong correlations
        strong_correlations = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_val = corr_matrix.iloc[i, j]
                if abs(corr_val) > 0.7:  # Strong correlation threshold
                    strong_correlations.append({
                        'feature1': corr_matrix.columns[i],
                        'feature2': corr_matrix.columns[j],
                        'correlation': round(corr_val, 3),
                        'strength': 'strong positive' if corr_val > 0 else 'strong negative'
                    })
        
        if strong_correlations:
            insights.append({
                'type': 'strong_correlations',
                'message': f'Found {len(strong_correlations)} strong correlations',
                'details': strong_correlations
            })
        
        return insights
    
    def _analyze_distributions(self, df, nutrients):
        """Analyze distribution patterns"""
        insights = []
        
        for nutrient in nutrients:
            # Check for normal distribution (simplified)
            skewness = df[nutrient].skew()
            
            if abs(skewness) < 0.5:
                distribution_type = 'approximately normal'
            elif skewness > 0.5:
                distribution_type = 'right-skewed'
            else:
                distribution_type = 'left-skewed'
            
            insights.append({
                'nutrient': nutrient,
                'distribution_type': distribution_type,
                'skewness': round(skewness, 3),
                'outlier_count': len(df[df[nutrient] > df[nutrient].quantile(0.75) + 1.5 * 
                                    (df[nutrient].quantile(0.75) - df[nutrient].quantile(0.25))])
            })
        
        return insights
    
    def _analyze_trends(self, df):
        """Analyze temporal trends"""
        insights = []
        
        if 'date' in df.columns:
            # Simple trend analysis
            numerical_cols = df.select_dtypes(include=[np.number]).columns
            
            for col in numerical_cols:
                if col in df.columns:
                    # Calculate correlation with time (as ordinal)
                    df['time_ordinal'] = pd.to_datetime(df['date']).astype('int64')
                    time_corr = df['time_ordinal'].corr(df[col])
                    
                    if abs(time_corr) > 0.3:
                        trend_type = 'increasing' if time_corr > 0 else 'decreasing'
                        insights.append({
                            'feature': col,
                            'trend': trend_type,
                            'correlation_with_time': round(time_corr, 3)
                        })
        
        return insights