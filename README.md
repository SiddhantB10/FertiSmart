# 🌾 FertiSmart - AI-Powered Crop Recommendation System

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/fertismart)
[![Live Demo](https://img.shields.io/badge/Live-Demo-green)](https://fertismart.vercel.app/)
[![Backend API](https://img.shields.io/badge/API-Live-blue)](https://fertismart-backend.onrender.com)

## 🚀 Overview

FertiSmart is an intelligent crop recommendation system that leverages machine learning to help farmers make data-driven decisions about crop selection. Using advanced Random Forest algorithms, the system analyzes soil conditions and environmental factors to provide accurate crop recommendations with confidence scores.

### ✨ Key Features

- 🤖 **AI-Powered Predictions**: Random Forest ML algorithm with 95%+ accuracy
- 🌱 **22 Crop Support**: Comprehensive database of agricultural crops
- 📱 **Fully Responsive**: Optimized for mobile, tablet, and desktop devices
- 🎨 **Modern UI**: Clean, professional interface with dark/light theme support
- ⚡ **Real-time Analysis**: Instant crop recommendations with confidence scores
- 📊 **Sample Data**: Pre-loaded test data for easy experimentation

## 🛠️ Technology Stack

### Frontend
- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: Custom responsive components
- **Deployment**: Vercel

### Backend
- **Framework**: Flask (Python)
- **ML Library**: scikit-learn (Random Forest)
- **Data Processing**: pandas, numpy
- **Database**: PostgreSQL (Neon)
- **Deployment**: Render

### Machine Learning
- **Algorithm**: Random Forest Classifier
- **Features**: 7 input parameters (N, P, K, Temperature, Humidity, pH, Rainfall)
- **Training Data**: 2,200+ crop samples
- **Accuracy**: 95%+ prediction accuracy
- **Supported Crops**: 22 different agricultural crops

## 🌐 Live Demo

- **Frontend**: [https://fertismart.vercel.app/](https://fertismart.vercel.app/)
- **Backend API**: [https://fertismart-backend.onrender.com](https://fertismart-backend.onrender.com)
- **Health Check**: [API Status](https://fertismart-backend.onrender.com/api/health)

## 📋 Prerequisites

- Node.js 18+ and npm
- Python 3.8+
- PostgreSQL database (optional for local development)

## 🔧 Local Development Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/fertismart.git
cd fertismart
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
The frontend will be available at `http://localhost:3000`

### 3. Backend Setup
```bash
cd backend
pip install -r requirements.txt
python simple_app.py
```
The backend will be available at `http://localhost:5001`

### 4. Environment Variables

Create `.env.local` in the frontend directory:
```env
NEXT_PUBLIC_API_URL=http://localhost:5001
```

Create `.env` in the backend directory:
```env
DATABASE_URL=your_postgresql_connection_string
FLASK_ENV=development
```

## 🎯 How to Use

1. **Visit the Application**: Navigate to the live demo or run locally
2. **Load Sample Data**: Click the "📋 Load Sample" button to fill the form with test data
3. **Enter Soil Parameters**:
   - Nitrogen (N), Phosphorus (P), Potassium (K) levels
   - Temperature, Humidity, pH levels
   - Rainfall measurements
4. **Get Recommendation**: Click "🌾 Get Crop Recommendation" 
5. **View Results**: See the recommended crop with confidence score and explanation

## 🔄 API Endpoints

### Health Check
```http
GET /api/health
```

### Model Information
```http
GET /api/model/info
```

### Crop Prediction
```http
POST /api/predict
Content-Type: application/json

{
  "N": 90,
  "P": 42,
  "K": 43,
  "temperature": 20.879744,
  "humidity": 82.002744,
  "ph": 6.502985,
  "rainfall": 202.935536
}
```

### Supported Crops List
```http
GET /api/crops
```

## 🤖 Machine Learning Model

### Algorithm Details
- **Type**: Random Forest Classifier
- **Trees**: 100 estimators
- **Max Depth**: 15
- **Features**: 7 environmental parameters
- **Classes**: 22 crop types

### Supported Crops
Rice, Maize, Chickpea, Kidneybeans, Pigeonpeas, Mothbeans, Mungbean, Blackgram, Lentil, Pomegranate, Banana, Mango, Grapes, Watermelon, Muskmelon, Apple, Orange, Papaya, Coconut, Cotton, Jute, Coffee

### Model Performance
- **Accuracy**: 95%+ on test data
- **Training Samples**: 2,200+ agricultural records
- **Validation**: Cross-validated performance metrics

## 📱 Responsive Design

FertiSmart is fully optimized for all devices:

- **📱 Mobile**: Touch-friendly interface, full-width buttons
- **📱 Tablet**: Two-column layouts, optimized touch targets
- **💻 Desktop**: Three-column grids, hover effects, spacious design
- **🖥️ Large Screens**: Enhanced typography and generous spacing

## 🎨 Features

### User Interface
- Clean, modern design with professional typography
- Dark/Light theme toggle
- Smooth animations and transitions
- Loading states and error handling
- Form validation with user-friendly messages

### Technical Features
- Server-side rendering with Next.js
- API-first architecture
- Cross-Origin Resource Sharing (CORS) enabled
- Production-ready deployment configuration
- Comprehensive error handling and logging

## 🚀 Deployment

### Frontend (Vercel)
1. Connect your GitHub repository to Vercel
2. Set environment variable: `NEXT_PUBLIC_API_URL=https://fertismart-backend.onrender.com`
3. Deploy automatically on push to main branch

### Backend (Render)
1. Connect your GitHub repository to Render
2. Set up environment variables for database connection
3. Deploy with automatic builds

### Database (Neon)
- PostgreSQL database with SSL enabled
- Connection pooling for optimal performance
- Automatic backups and monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Developer

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)

## 🙏 Acknowledgments

- Machine Learning dataset from agricultural research
- UI inspiration from modern web applications
- Open source community for excellent libraries and tools

## 📞 Support

If you have any questions or need support, please:
1. Check the [Issues](https://github.com/yourusername/fertismart/issues) page
2. Create a new issue with detailed information
3. Contact the developer directly

---

<div align="center">
  <strong>🌾 Making Agriculture Smarter with AI 🌾</strong>
</div>