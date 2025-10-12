"""
Database Models for FertiSmart
Implements Star Schema and Snowflake Schema designs
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from app import db

# =============================================================================
# STAR SCHEMA IMPLEMENTATION (Experiment 1)
# =============================================================================

class SoilTestFact(db.Model):
    """
    Fact table for soil test measurements
    Central table in the star schema containing all measurable facts
    """
    __tablename__ = 'soil_test_fact'
    
    id = Column(Integer, primary_key=True)
    
    # Soil Nutrient Measurements
    nitrogen = Column(Float, nullable=False, comment='Nitrogen content (N)')
    phosphorus = Column(Float, nullable=False, comment='Phosphorus content (P)')
    potassium = Column(Float, nullable=False, comment='Potassium content (K)')
    
    # Environmental Measurements
    temperature = Column(Float, nullable=False, comment='Temperature in Celsius')
    humidity = Column(Float, nullable=False, comment='Humidity percentage')
    ph = Column(Float, nullable=False, comment='pH level')
    rainfall = Column(Float, nullable=False, comment='Rainfall in mm')
    
    # Foreign Keys to Dimension Tables
    region_id = Column(Integer, ForeignKey('region_dim.region_id'), nullable=False)
    crop_id = Column(Integer, ForeignKey('crop_dim.crop_id'), nullable=False)
    fertilizer_id = Column(Integer, ForeignKey('fertilizer_dim.fertilizer_id'), nullable=False)
    time_id = Column(Integer, ForeignKey('time_dim.time_id'), nullable=False)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    region = relationship("RegionDim", back_populates="soil_tests")
    crop = relationship("CropDim", back_populates="soil_tests")
    fertilizer = relationship("FertilizerDim", back_populates="soil_tests")
    time = relationship("TimeDim", back_populates="soil_tests")
    
    def __repr__(self):
        return f'<SoilTest {self.id}: N={self.nitrogen}, P={self.phosphorus}, K={self.potassium}>'

class RegionDim(db.Model):
    """Region dimension table"""
    __tablename__ = 'region_dim'
    
    region_id = Column(Integer, primary_key=True)
    region_name = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    district = Column(String(100), nullable=False)
    country = Column(String(100), default='India')
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # Relationships
    soil_tests = relationship("SoilTestFact", back_populates="region")
    
    def __repr__(self):
        return f'<Region {self.region_name}, {self.state}>'

class CropDim(db.Model):
    """Crop dimension table"""
    __tablename__ = 'crop_dim'
    
    crop_id = Column(Integer, primary_key=True)
    crop_name = Column(String(100), nullable=False, unique=True)
    crop_type = Column(String(50), nullable=False)  # cereal, pulse, oilseed, etc.
    season = Column(String(50), nullable=False)  # kharif, rabi, summer
    growth_duration = Column(Integer, nullable=True, comment='Growth duration in days')
    water_requirement = Column(String(50), nullable=True)  # low, medium, high
    
    # Relationships
    soil_tests = relationship("SoilTestFact", back_populates="crop")
    
    def __repr__(self):
        return f'<Crop {self.crop_name} ({self.season})>'

class FertilizerDim(db.Model):
    """Fertilizer dimension table"""
    __tablename__ = 'fertilizer_dim'
    
    fertilizer_id = Column(Integer, primary_key=True)
    fertilizer_name = Column(String(100), nullable=False)
    npk_ratio = Column(String(20), nullable=False, comment='N:P:K ratio (e.g., 10:26:26)')
    fertilizer_type = Column(String(50), nullable=False)  # organic, chemical, bio
    nitrogen_percentage = Column(Float, nullable=True)
    phosphorus_percentage = Column(Float, nullable=True)
    potassium_percentage = Column(Float, nullable=True)
    price_per_kg = Column(Float, nullable=True)
    manufacturer = Column(String(100), nullable=True)
    
    # Relationships
    soil_tests = relationship("SoilTestFact", back_populates="fertilizer")
    
    def __repr__(self):
        return f'<Fertilizer {self.fertilizer_name} ({self.npk_ratio})>'

class TimeDim(db.Model):
    """Time dimension table"""
    __tablename__ = 'time_dim'
    
    time_id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    day = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    quarter = Column(Integer, nullable=False)
    season = Column(String(20), nullable=False)  # spring, summer, monsoon, winter
    is_weekend = Column(Boolean, default=False)
    
    # Relationships
    soil_tests = relationship("SoilTestFact", back_populates="time")
    
    def __repr__(self):
        return f'<Time {self.date.strftime("%Y-%m-%d")} ({self.season})>'

# =============================================================================
# SNOWFLAKE SCHEMA EXTENSIONS (Experiment 1)
# =============================================================================

class StateDim(db.Model):
    """State dimension for snowflake schema normalization"""
    __tablename__ = 'state_dim'
    
    state_id = Column(Integer, primary_key=True)
    state_name = Column(String(100), nullable=False, unique=True)
    state_code = Column(String(10), nullable=False)
    population = Column(Integer, nullable=True)
    area_sq_km = Column(Float, nullable=True)
    
    # Relationships
    districts = relationship("DistrictDim", back_populates="state")

class DistrictDim(db.Model):
    """District dimension for snowflake schema normalization"""
    __tablename__ = 'district_dim'
    
    district_id = Column(Integer, primary_key=True)
    district_name = Column(String(100), nullable=False)
    state_id = Column(Integer, ForeignKey('state_dim.state_id'), nullable=False)
    population = Column(Integer, nullable=True)
    area_sq_km = Column(Float, nullable=True)
    agricultural_area = Column(Float, nullable=True)
    
    # Relationships
    state = relationship("StateDim", back_populates="districts")

class CropTypeDim(db.Model):
    """Crop type dimension for snowflake schema normalization"""
    __tablename__ = 'crop_type_dim'
    
    crop_type_id = Column(Integer, primary_key=True)
    type_name = Column(String(50), nullable=False, unique=True)
    category = Column(String(50), nullable=False)  # food, cash, fodder
    description = Column(Text, nullable=True)

# =============================================================================
# ADDITIONAL MODELS FOR ML AND ANALYTICS
# =============================================================================

class PreprocessedData(db.Model):
    """Store preprocessed data for ML models"""
    __tablename__ = 'preprocessed_data'
    
    id = Column(Integer, primary_key=True)
    original_soil_test_id = Column(Integer, ForeignKey('soil_test_fact.id'))
    
    # Normalized/Scaled Features
    nitrogen_scaled = Column(Float, nullable=False)
    phosphorus_scaled = Column(Float, nullable=False)
    potassium_scaled = Column(Float, nullable=False)
    temperature_scaled = Column(Float, nullable=False)
    humidity_scaled = Column(Float, nullable=False)
    ph_scaled = Column(Float, nullable=False)
    rainfall_scaled = Column(Float, nullable=False)
    
    # Encoded Features
    crop_encoded = Column(Integer, nullable=False)
    fertilizer_encoded = Column(Integer, nullable=False)
    
    # Processing metadata
    scaling_method = Column(String(50), nullable=False)  # StandardScaler, MinMaxScaler
    processed_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<PreprocessedData {self.id}>'

class ModelPrediction(db.Model):
    """Store model predictions and results"""
    __tablename__ = 'model_predictions'
    
    id = Column(Integer, primary_key=True)
    soil_test_id = Column(Integer, ForeignKey('soil_test_fact.id'))
    model_name = Column(String(100), nullable=False)  # DecisionTree, NaiveBayes
    model_version = Column(String(20), nullable=False)
    
    # Predictions
    predicted_crop = Column(String(100), nullable=True)
    predicted_fertilizer = Column(String(100), nullable=True)
    confidence_score = Column(Float, nullable=True)
    
    # Model Performance
    accuracy = Column(Float, nullable=True)
    precision = Column(Float, nullable=True)
    recall = Column(Float, nullable=True)
    f1_score = Column(Float, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Prediction {self.id}: {self.model_name}>'

class ClusterResult(db.Model):
    """Store clustering analysis results"""
    __tablename__ = 'cluster_results'
    
    id = Column(Integer, primary_key=True)
    soil_test_id = Column(Integer, ForeignKey('soil_test_fact.id'))
    clustering_algorithm = Column(String(50), nullable=False)  # KMeans, Agglomerative, DBSCAN
    
    # Cluster Assignment
    cluster_id = Column(Integer, nullable=False)
    cluster_label = Column(String(100), nullable=True)
    
    # Cluster Characteristics
    silhouette_score = Column(Float, nullable=True)
    distance_to_centroid = Column(Float, nullable=True)
    
    # Metadata
    n_clusters = Column(Integer, nullable=True)
    algorithm_params = Column(Text, nullable=True)  # JSON string of parameters
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ClusterResult {self.id}: {self.clustering_algorithm}>'

class DataQualityMetrics(db.Model):
    """Store data quality metrics and preprocessing logs"""
    __tablename__ = 'data_quality_metrics'
    
    id = Column(Integer, primary_key=True)
    dataset_name = Column(String(100), nullable=False)
    
    # Quality Metrics
    total_records = Column(Integer, nullable=False)
    missing_values = Column(Integer, default=0)
    duplicate_records = Column(Integer, default=0)
    outliers_detected = Column(Integer, default=0)
    
    # Processing Steps
    preprocessing_steps = Column(Text, nullable=True)  # JSON array of steps
    quality_score = Column(Float, nullable=True)  # 0-1 quality score
    
    # Timestamps
    analyzed_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<DataQuality {self.dataset_name}: {self.quality_score}>'