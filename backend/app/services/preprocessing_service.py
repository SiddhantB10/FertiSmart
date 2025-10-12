"""
Preprocessing Service for FertiSmart
Handles data cleaning, normalization, and quality assessment (Experiment 2)
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import joblib
import os
from datetime import datetime
from app.models.database_models import DataQualityMetrics, PreprocessedData, SoilTestFact
from app import db

class PreprocessingService:
    """Data preprocessing and quality management service"""
    
    def __init__(self):
        self.scaler = None
        self.label_encoders = {}
        self.preprocessing_steps = []
    
    def process_file(self, file_path):
        """Main preprocessing pipeline"""
        try:
            # Load data
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith('.xlsx'):
                df = pd.read_excel(file_path)
            else:
                raise ValueError("Unsupported file format")
            
            # Initial data assessment
            initial_metrics = self._assess_data_quality(df, "raw_upload")
            
            # Preprocessing pipeline
            df_cleaned = self._handle_missing_values(df.copy())
            df_cleaned = self._handle_outliers(df_cleaned)
            df_cleaned = self._handle_duplicates(df_cleaned)
            df_normalized = self._normalize_features(df_cleaned)
            df_encoded = self._encode_categorical_features(df_normalized)
            
            # Final data assessment
            final_metrics = self._assess_data_quality(df_encoded, "processed")
            
            # Store processed data
            self._store_processed_data(df_encoded)
            
            # Prepare response
            result = {
                'original_shape': df.shape,
                'processed_shape': df_encoded.shape,
                'preprocessing_steps': self.preprocessing_steps,
                'quality_improvement': {
                    'before': initial_metrics,
                    'after': final_metrics
                },
                'sample_data': df_encoded.head(5).to_dict('records'),
                'feature_summary': self._get_feature_summary(df_encoded)
            }
            
            return result
            
        except Exception as e:
            raise Exception(f"Preprocessing failed: {str(e)}")
    
    def _assess_data_quality(self, df, dataset_name):
        """Assess and store data quality metrics"""
        total_records = len(df)
        missing_values = df.isnull().sum().sum()
        duplicate_records = df.duplicated().sum()
        
        # Detect outliers using IQR method
        outliers_count = 0
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = ((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))).sum()
            outliers_count += outliers
        
        # Calculate quality score (0-1)
        quality_score = 1.0 - (missing_values + duplicate_records + outliers_count) / (total_records * len(df.columns))
        quality_score = max(0, min(1, quality_score))
        
        # Store in database
        metrics = DataQualityMetrics(
            dataset_name=dataset_name,
            total_records=total_records,
            missing_values=missing_values,
            duplicate_records=duplicate_records,
            outliers_detected=outliers_count,
            preprocessing_steps=str(self.preprocessing_steps),
            quality_score=quality_score
        )
        db.session.add(metrics)
        db.session.commit()
        
        return {
            'total_records': total_records,
            'missing_values': missing_values,
            'duplicate_records': duplicate_records,
            'outliers_detected': outliers_count,
            'quality_score': round(quality_score, 3)
        }
    
    def _handle_missing_values(self, df):
        """Handle missing values in the dataset"""
        self.preprocessing_steps.append("Missing value imputation")
        
        # For numeric columns, use median imputation
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if df[col].isnull().any():
                median_value = df[col].median()
                df[col].fillna(median_value, inplace=True)
        
        # For categorical columns, use mode imputation
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if df[col].isnull().any():
                mode_value = df[col].mode()[0] if not df[col].mode().empty else 'Unknown'
                df[col].fillna(mode_value, inplace=True)
        
        return df
    
    def _handle_outliers(self, df):
        """Handle outliers using IQR method"""
        self.preprocessing_steps.append("Outlier detection and treatment")
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            # Define outlier bounds
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            # Cap outliers instead of removing them
            df[col] = df[col].clip(lower=lower_bound, upper=upper_bound)
        
        return df
    
    def _handle_duplicates(self, df):
        """Remove duplicate records"""
        initial_count = len(df)
        df_dedupe = df.drop_duplicates()
        final_count = len(df_dedupe)
        
        if initial_count != final_count:
            self.preprocessing_steps.append(f"Removed {initial_count - final_count} duplicate records")
        
        return df_dedupe
    
    def _normalize_features(self, df):
        """Normalize numerical features"""
        self.preprocessing_steps.append("Feature normalization using StandardScaler")
        
        # Identify numerical columns (assuming standard soil test columns)
        numerical_features = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
        
        # Check if columns exist in the dataframe
        available_features = [col for col in numerical_features if col in df.columns]
        
        if available_features:
            self.scaler = StandardScaler()
            df_scaled = df.copy()
            
            # Fit and transform the features
            scaled_values = self.scaler.fit_transform(df[available_features])
            
            # Create new column names for scaled features
            for i, feature in enumerate(available_features):
                df_scaled[f'{feature}_scaled'] = scaled_values[:, i]
        
            # Save the scaler for future use
            os.makedirs('trained_models', exist_ok=True)
            joblib.dump(self.scaler, 'trained_models/feature_scaler.pkl')
            
            return df_scaled
        
        return df
    
    def _encode_categorical_features(self, df):
        """Encode categorical features"""
        self.preprocessing_steps.append("Categorical feature encoding")
        
        # Common categorical columns in crop recommendation datasets
        categorical_features = ['label', 'crop', 'fertilizer']
        
        # Check which categorical features exist
        available_categorical = [col for col in categorical_features if col in df.columns]
        
        df_encoded = df.copy()
        
        for feature in available_categorical:
            self.label_encoders[feature] = LabelEncoder()
            df_encoded[f'{feature}_encoded'] = self.label_encoders[feature].fit_transform(df[feature])
            
            # Save the encoder
            os.makedirs('trained_models', exist_ok=True)
            joblib.dump(self.label_encoders[feature], f'trained_models/{feature}_encoder.pkl')
        
        return df_encoded
    
    def _store_processed_data(self, df):
        """Store preprocessed data in database"""
        try:
            # Assuming the dataframe has the required columns
            scaled_features = ['N_scaled', 'P_scaled', 'K_scaled', 'temperature_scaled', 
                             'humidity_scaled', 'ph_scaled', 'rainfall_scaled']
            
            encoded_features = ['crop_encoded', 'fertilizer_encoded']
            
            # Check if required columns exist
            if all(col in df.columns for col in scaled_features):
                for index, row in df.iterrows():
                    processed_record = PreprocessedData(
                        nitrogen_scaled=row.get('N_scaled', 0),
                        phosphorus_scaled=row.get('P_scaled', 0),
                        potassium_scaled=row.get('K_scaled', 0),
                        temperature_scaled=row.get('temperature_scaled', 0),
                        humidity_scaled=row.get('humidity_scaled', 0),
                        ph_scaled=row.get('ph_scaled', 0),
                        rainfall_scaled=row.get('rainfall_scaled', 0),
                        crop_encoded=row.get('crop_encoded', 0),
                        fertilizer_encoded=row.get('fertilizer_encoded', 0),
                        scaling_method='StandardScaler'
                    )
                    db.session.add(processed_record)
                
                db.session.commit()
        
        except Exception as e:
            print(f"Warning: Could not store processed data in database: {str(e)}")
    
    def _get_feature_summary(self, df):
        """Generate feature summary statistics"""
        summary = {}
        
        # Numerical features summary
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            summary[col] = {
                'type': 'numerical',
                'mean': round(df[col].mean(), 3),
                'std': round(df[col].std(), 3),
                'min': round(df[col].min(), 3),
                'max': round(df[col].max(), 3),
                'missing_count': df[col].isnull().sum()
            }
        
        # Categorical features summary
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            summary[col] = {
                'type': 'categorical',
                'unique_values': df[col].nunique(),
                'most_frequent': df[col].mode().iloc[0] if not df[col].mode().empty else None,
                'missing_count': df[col].isnull().sum()
            }
        
        return summary
    
    def get_train_test_split(self, test_size=0.2, random_state=42):
        """Get train-test split of processed data"""
        try:
            # Get preprocessed data from database
            preprocessed_data = PreprocessedData.query.all()
            
            if not preprocessed_data:
                raise ValueError("No preprocessed data found")
            
            # Convert to DataFrame
            data_list = []
            for record in preprocessed_data:
                data_list.append({
                    'nitrogen_scaled': record.nitrogen_scaled,
                    'phosphorus_scaled': record.phosphorus_scaled,
                    'potassium_scaled': record.potassium_scaled,
                    'temperature_scaled': record.temperature_scaled,
                    'humidity_scaled': record.humidity_scaled,
                    'ph_scaled': record.ph_scaled,
                    'rainfall_scaled': record.rainfall_scaled,
                    'crop_encoded': record.crop_encoded,
                    'fertilizer_encoded': record.fertilizer_encoded
                })
            
            df = pd.DataFrame(data_list)
            
            # Features and targets
            feature_cols = ['nitrogen_scaled', 'phosphorus_scaled', 'potassium_scaled', 
                           'temperature_scaled', 'humidity_scaled', 'ph_scaled', 'rainfall_scaled']
            
            X = df[feature_cols]
            y_crop = df['crop_encoded']
            y_fertilizer = df['fertilizer_encoded']
            
            # Split the data
            X_train, X_test, y_crop_train, y_crop_test = train_test_split(
                X, y_crop, test_size=test_size, random_state=random_state
            )
            
            _, _, y_fert_train, y_fert_test = train_test_split(
                X, y_fertilizer, test_size=test_size, random_state=random_state
            )
            
            return {
                'X_train': X_train,
                'X_test': X_test,
                'y_crop_train': y_crop_train,
                'y_crop_test': y_crop_test,
                'y_fertilizer_train': y_fert_train,
                'y_fertilizer_test': y_fert_test
            }
        
        except Exception as e:
            raise Exception(f"Failed to create train-test split: {str(e)}")
    
    def load_sample_data(self):
        """Load or create sample crop recommendation data for demonstration"""
        try:
            # Create sample data if no data exists
            sample_data = {
                'N': [90, 42, 74, 78, 65, 60, 55, 25, 20, 10],
                'P': [42, 43, 35, 42, 58, 55, 44, 21, 28, 26],
                'K': [43, 21, 40, 21, 41, 44, 42, 23, 30, 15],
                'temperature': [20.9, 21.8, 26.5, 23.2, 24.5, 26.1, 24.7, 26.9, 27.0, 21.8],
                'humidity': [82.0, 80.3, 80.2, 82.3, 66.9, 71.5, 78.5, 64.9, 60.3, 76.4],
                'ph': [6.5, 7.8, 6.4, 7.5, 6.8, 7.2, 6.9, 6.4, 6.2, 7.0],
                'rainfall': [202.9, 226.7, 94.9, 127.2, 262.7, 151.8, 132.0, 127.2, 132.4, 114.8],
                'label': ['rice', 'maize', 'chickpea', 'kidneybeans', 'pigeonpeas', 
                         'mothbeans', 'mungbean', 'blackgram', 'lentil', 'pomegranate']
            }
            
            df = pd.DataFrame(sample_data)
            return self.process_file_from_dataframe(df)
        
        except Exception as e:
            raise Exception(f"Failed to load sample data: {str(e)}")
    
    def process_file_from_dataframe(self, df):
        """Process data from pandas DataFrame"""
        try:
            # Initial data assessment
            initial_metrics = self._assess_data_quality(df, "sample_data")
            
            # Preprocessing pipeline
            df_cleaned = self._handle_missing_values(df.copy())
            df_cleaned = self._handle_outliers(df_cleaned)
            df_cleaned = self._handle_duplicates(df_cleaned)
            df_normalized = self._normalize_features(df_cleaned)
            df_encoded = self._encode_categorical_features(df_normalized)
            
            # Final data assessment
            final_metrics = self._assess_data_quality(df_encoded, "processed_sample")
            
            # Store processed data
            self._store_processed_data(df_encoded)
            
            # Prepare response
            result = {
                'original_shape': df.shape,
                'processed_shape': df_encoded.shape,
                'preprocessing_steps': self.preprocessing_steps,
                'quality_improvement': {
                    'before': initial_metrics,
                    'after': final_metrics
                },
                'sample_data': df_encoded.head(5).to_dict('records'),
                'feature_summary': self._get_feature_summary(df_encoded)
            }
            
            return result
            
        except Exception as e:
            raise Exception(f"DataFrame processing failed: {str(e)}")