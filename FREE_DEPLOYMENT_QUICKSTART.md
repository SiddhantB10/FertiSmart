# 🚀 FREE Deployment Quick Start

## Total Cost: $0/month ✅

### Services Used:
- **Vercel** (Frontend) - FREE Hobby Plan
- **Render** (Backend) - FREE Plan  
- **Neon** (Database) - FREE Plan

### Deployment Steps:

#### 1. Database Setup (2 minutes)
1. Go to [neon.tech](https://neon.tech) → Sign up → Create project "FertiSmart"
2. Copy the connection string: `postgresql://username:password@host/database`

#### 2. Backend Deployment (5 minutes)  
1. Go to [render.com](https://render.com) → Sign up → New Web Service
2. Connect GitHub → Select FertiSmart repo
3. Settings:
   - Root Directory: `backend`
   - Build: `pip install -r requirements.txt` 
   - Start: `gunicorn simple_app:app --bind 0.0.0.0:$PORT`
4. Environment Variables:
   ```
   DATABASE_URL=your-neon-connection-string
   FLASK_ENV=production
   SECRET_KEY=any-random-string-here
   FRONTEND_URL=https://fertismart.vercel.app
   ```
5. Deploy → Copy your Render URL

#### 3. Frontend Deployment (2 minutes)
1. Update `vercel.json` with your Render URL
2. Go to [vercel.com](https://vercel.com) → New Project → Import FertiSmart
3. Root Directory: `frontend`
4. Environment Variable: `NEXT_PUBLIC_API_URL=https://fertismart-backend.onrender.com`
5. Deploy → Copy your Vercel URL

#### 4. Final Step (1 minute)
1. Go back to Render → Update `FRONTEND_URL` with your Vercel URL
2. Redeploy backend

### ⚠️ Free Tier Limitations:
- **Render**: Sleeps after 15 min → 30s wake-up time
- **Neon**: Pauses after 7 days inactivity  
- **Vercel**: 100 deployments/month limit

### 🎯 Perfect For:
- Portfolio projects
- Demos and prototypes  
- Learning and development
- Low-traffic personal use

**Ready to deploy? Follow the detailed guide!** 📖