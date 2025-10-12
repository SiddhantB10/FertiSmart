# FertiSmart: Data-Driven Soil Analysis and Smart Fertilizer Recommendation System

A comprehensive full-stack web application that provides intelligent soil analysis and fertilizer recommendations using machine learning and data analytics.

## 🌾 Project Overview

FertiSmart is a data-driven platform designed for farmers and agricultural researchers to:
- Analyze soil composition and properties
- Get personalized fertilizer recommendations
- Visualize soil data through interactive dashboards
- Explore clustering patterns in soil types
- Access comprehensive business intelligence insights

## 🧩 Core Features

### 1. Data Warehouse Design (Experiment 1)
- Star Schema and Snowflake Schema implementation
- Comprehensive database design for soil and fertilizer data
- OLAP-style business intelligence components

### 2. Data Preprocessing (Experiment 2)
- Advanced data cleaning and normalization
- Outlier detection and handling
- Feature engineering for ML models

### 3. Exploratory Data Analysis (Experiment 3)
- Interactive visualizations and dashboards
- Statistical analysis and insights
- Correlation analysis and trend identification

### 4. Classification Models (Experiments 4 & 5)
- Decision Tree and Naïve Bayes implementations
- Both Weka/RapidMiner and Python scikit-learn versions
- Comprehensive model evaluation metrics

### 5. Clustering Analysis (Experiments 6 & 7)
- K-Means, Agglomerative, and DBSCAN clustering
- Soil type identification and fertility zone mapping
- PCA and t-SNE dimensionality reduction

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask/FastAPI
- **ML Libraries**: scikit-learn, pandas, numpy
- **Visualization**: matplotlib, seaborn, plotly
- **Database**: SQLAlchemy ORM with PostgreSQL
- **API Endpoints**: RESTful services

### Frontend
- **Framework**: React.js with Next.js
- **Styling**: Tailwind CSS
- **Charts**: Chart.js and Plotly
- **UI Components**: Modern responsive design

### Database
- **Primary**: PostgreSQL
- **Schema**: Star and Snowflake implementations
- **Data**: Raw and processed soil data, model outputs

## 📊 Project Structure

```
fertismart/
├── backend/                    # Python Flask/FastAPI backend
│   ├── app/
│   │   ├── api/               # API endpoints
│   │   ├── models/            # Database models
│   │   ├── services/          # Business logic
│   │   └── utils/            # Utility functions
│   ├── ml/                   # Machine learning components
│   │   ├── preprocessing/    # Data preprocessing
│   │   ├── classification/   # Classification models
│   │   ├── clustering/      # Clustering algorithms
│   │   └── visualization/   # ML visualizations
│   ├── data/                # Dataset and processed data
│   ├── models/              # Trained model files
│   └── requirements.txt
├── frontend/                 # React.js frontend
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/          # Application pages
│   │   ├── services/       # API services
│   │   └── utils/          # Utility functions
│   ├── public/             # Static assets
│   └── package.json
├── database/                # Database schemas and scripts
│   ├── schemas/            # Star and Snowflake schemas
│   ├── migrations/         # Database migrations
│   └── seeds/              # Sample data
├── docs/                   # Documentation
├── docker/                 # Docker configuration
└── README.md
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL 12+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/fertismart.git
   cd fertismart
   ```

2. **Set up the backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up the frontend**
   ```bash
   cd frontend
   npm install
   ```

4. **Configure the database**
   ```bash
   # Create PostgreSQL database
   createdb fertismart_db
   
   # Run migrations
   cd backend
   flask db upgrade
   ```

5. **Start the development servers**
   ```bash
   # Terminal 1: Backend
   cd backend
   python app.py
   
   # Terminal 2: Frontend
   cd frontend
   npm run dev
   ```

## 📈 API Endpoints

- `POST /api/preprocess` - Data preprocessing
- `POST /api/classify` - Crop/fertilizer classification
- `POST /api/cluster` - Soil clustering analysis
- `GET /api/visualize` - Data visualizations
- `POST /api/recommend` - Fertilizer recommendations
- `GET /api/analytics` - Business intelligence insights

## 🧪 Experiments Implementation

All 7 DMBI experiments are fully implemented:

1. **Data Warehouse Design** - Complete schema design with ER diagrams
2. **Data Preprocessing** - Comprehensive data cleaning pipeline
3. **EDA** - Interactive exploratory data analysis
4. **Classification (Weka/RapidMiner)** - External tool integration
5. **Classification (Python)** - Native ML implementation
6. **Clustering (Weka/RapidMiner)** - External clustering analysis
7. **Clustering (Python)** - Advanced clustering with visualization

## 📊 Dashboard Features

- **Soil Analysis Dashboard** - Comprehensive nutrient analysis
- **Fertilizer Recommendation** - AI-powered recommendations
- **Clustering Visualization** - Interactive soil type mapping
- **Business Intelligence** - Data warehouse insights
- **Schema Visualization** - Database design diagrams

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

Your Name - your.email@example.com
Project Link: [https://github.com/your-username/fertismart](https://github.com/your-username/fertismart)

## 🙏 Acknowledgments

- Agricultural research community
- Open-source ML libraries
- Data science community
- Modern web development frameworks