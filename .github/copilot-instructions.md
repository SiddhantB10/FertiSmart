# FertiSmart Project Instructions for GitHub Copilot

## Project Overview
FertiSmart is a full-stack Smart Crop Recommendation System using Machine Learning for data-driven agricultural analysis.

## Technology Stack
- **Frontend**: Next.js 14, React 18, TypeScript, Tailwind CSS
- **Backend**: Flask, Python 3.8+
- **ML Libraries**: scikit-learn, pandas, numpy, matplotlib, plotly
- **Data Storage**: CSV-based dataset (55,500 samples)
- **Model**: Random Forest Classifier with 97.32% accuracy

## Project Status
- [x] Verify that the copilot-instructions.md file in the .github directory is created.
- [x] Clarify Project Requirements
- [x] Scaffold the Project
- [x] Customize the Project
- [x] Install Required Extensions
- [x] Compile the Project
- [x] Create and Run Task
- [x] Launch the Project
- [x] Ensure Documentation is Complete

## Development Guidelines
1. Frontend components use TypeScript and Tailwind CSS
2. Backend services follow Flask REST API patterns
3. ML model uses Random Forest with CSV data
4. All predictions are real-time using trained model
5. API endpoints follow RESTful conventions
6. All code includes proper error handling and logging

## Key Components
- **ML Model**: Random Forest trained on CSV dataset (`backend/crop_model.pkl`)
- **Dataset**: Crop recommendation data (`backend/Crop_recommendation.csv`)
- **API Routes**: RESTful endpoints in `backend/simple_app.py`
- **React Components**: Responsive UI components with TypeScript
- **Pages**: Home, Crop Recommendation with Feature Importance Analysis

## Running the Project
- Frontend: `npm run dev` (http://localhost:3000)
- Backend: `python simple_app.py` (http://localhost:5001)
- Model auto-trains from CSV if pkl files are missing