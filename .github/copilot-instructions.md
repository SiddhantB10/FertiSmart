# FertiSmart Project Instructions for GitHub Copilot

## Project Overview
FertiSmart is a full-stack Data-Driven Soil Analysis and Smart Fertilizer Recommendation System implementing 7 DMBI (Data Mining and Business Intelligence) experiments.

## Technology Stack
- **Frontend**: Next.js 14, React 18, TypeScript, Tailwind CSS
- **Backend**: Flask, SQLAlchemy, Python 3.8+
- **Database**: PostgreSQL with Star/Snowflake schemas
- **ML Libraries**: scikit-learn, pandas, numpy, matplotlib, plotly

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
2. Backend services follow Flask blueprint patterns
3. Database models use SQLAlchemy ORM
4. ML services implement all 7 DMBI experiments
5. API endpoints follow RESTful conventions
6. All code includes proper error handling and logging

## Key Components
- **Database Models**: Star/Snowflake schema in `backend/app/models/database_models.py`
- **API Routes**: RESTful endpoints in `backend/app/api/routes.py`
- **ML Services**: 6 service files implementing DMBI experiments
- **React Components**: Responsive UI components with TypeScript
- **Dashboard Pages**: Analytics, Recommendations, Clustering, Schema views

## Running the Project
- Frontend: `npm run dev` (http://localhost:3000)
- Backend: `python app.py` (http://localhost:5000)
- Ensure PostgreSQL is running for full functionality