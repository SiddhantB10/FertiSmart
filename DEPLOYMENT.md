# 🚀 FertiSmart Deployment Guide

Complete guide for deploying FertiSmart to production using Vercel (Frontend) and Render (Backend).

## 📋 Table of Contents
- [Prerequisites](#prerequisites)
- [Backend Deployment (Render)](#backend-deployment-render)
- [Frontend Deployment (Vercel)](#frontend-deployment-vercel)
- [Environment Variables](#environment-variables)
- [Performance Optimization](#performance-optimization)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Accounts
- GitHub account with your FertiSmart repository
- [Render](https://render.com) account (Free tier available)
- [Vercel](https://vercel.com) account (Free tier available)

### Repository Setup
Ensure your repository is pushed to GitHub:
```bash
git add .
git commit -m "Ready for deployment"
git push origin master
```

## Backend Deployment (Render)

### Step 1: Create Web Service

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Select your `FertiSmart` repository

### Step 2: Configure Service

**Basic Settings:**
- **Name**: `fertismart-backend` (or your preferred name)
- **Region**: Choose closest to your users
- **Branch**: `master`
- **Root Directory**: `backend`
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn simple_app:app`

### Step 3: Environment Variables

Add these in the **Environment** section:

```env
PYTHON_VERSION=3.11.0
FLASK_ENV=production
PORT=5001
```

### Step 4: Deploy

1. Click **"Create Web Service"**
2. Wait for the build to complete (5-10 minutes)
3. Render will automatically deploy your backend
4. Note your backend URL: `https://fertismart-backend.onrender.com`

### Important Notes

**Free Tier Limitations:**
- ⚠️ Service spins down after 15 minutes of inactivity
- ⏱️ First request after spin-down takes 30-60 seconds
- 💡 Solution: Frontend includes auto-warming on page load

**Model Files:**
- Large `.pkl` files are in `.gitignore`
- Model auto-trains from CSV on first startup
- Takes ~2-3 minutes on first deploy

## Frontend Deployment (Vercel)

### Step 1: Import Project

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **"Add New..."** → **"Project"**
3. Import your GitHub repository
4. Select `FertiSmart`

### Step 2: Configure Project

**Framework Preset**: Next.js (auto-detected)

**Build Settings:**
- **Root Directory**: `frontend`
- **Build Command**: `npm run build` (auto-detected)
- **Output Directory**: `.next` (auto-detected)
- **Install Command**: `npm install` (auto-detected)

### Step 3: Environment Variables

Add in **Environment Variables** section:

```env
NEXT_PUBLIC_API_URL=https://fertismart-backend.onrender.com
```

Replace with your actual Render backend URL.

### Step 4: Deploy

1. Click **"Deploy"**
2. Wait for build (2-3 minutes)
3. Your site will be live at: `https://fertismart.vercel.app`

### Custom Domain (Optional)

1. Go to **Settings** → **Domains**
2. Add your custom domain
3. Update DNS records as instructed
4. SSL certificate auto-configured

## Environment Variables

### Backend (.env)
```env
# Flask Configuration
FLASK_ENV=production
PORT=5001

# Security
SECRET_KEY=your-super-secret-key-change-this

# Optional: Logging
LOG_LEVEL=INFO
```

### Frontend (.env.local)
```env
# API Configuration
NEXT_PUBLIC_API_URL=https://fertismart-backend.onrender.com
```

## Performance Optimization

### Backend (Render)

**1. Keep-Alive Strategy**
Our frontend automatically pings the backend to prevent sleep:
- Health check on page load
- Smart timeout handling
- User-friendly loading states

**2. Upgrade to Paid Plan (Optional)**
- No spin-down
- Always-on service
- Better performance
- Cost: $7/month

### Frontend (Vercel)

**1. Already Optimized**
- Edge network CDN
- Automatic caching
- Image optimization
- Zero config needed

**2. Performance Features**
- Server-side rendering
- Automatic code splitting
- Optimized builds

## Monitoring & Maintenance

### Backend Health Check
```bash
curl https://fertismart-backend.onrender.com/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "FertiSmart Crop Recommendation",
  "model_loaded": true,
  "model": "Random Forest Classifier",
  "timestamp": "2025-10-28T12:00:00Z"
}
```

### Frontend Health Check
Visit: `https://fertismart.vercel.app`

### Logs

**Render Logs:**
- Dashboard → Your Service → Logs tab
- Real-time log streaming
- Search and filter capabilities

**Vercel Logs:**
- Dashboard → Your Project → Deployments
- Click on deployment → View Logs

## Troubleshooting

### Backend Issues

**Problem: "Backend not responding"**
```
Solution: 
- First request after sleep takes 30-60s
- Frontend shows "Waking up backend" message
- Wait for warm-up to complete
```

**Problem: "Model not found"**
```
Solution:
- Model auto-trains on first startup
- Check Render logs for training progress
- Takes 2-3 minutes on initial deploy
```

**Problem: "Build failed"**
```
Solution:
- Check requirements.txt for errors
- Verify Python version (3.8+)
- Check Render build logs
```

### Frontend Issues

**Problem: "API connection failed"**
```
Solution:
- Verify NEXT_PUBLIC_API_URL is correct
- Check backend is deployed and running
- Ensure no CORS issues (already configured)
```

**Problem: "Slow predictions"**
```
Solution:
- Normal on first request (backend warm-up)
- Subsequent requests are fast
- Consider backend paid plan for always-on
```

### Common Deployment Errors

**Error: "Module not found"**
```bash
# Fix: Ensure all dependencies in requirements.txt
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update dependencies"
git push
```

**Error: "Port already in use"**
```bash
# Render automatically assigns ports
# Ensure app.run() uses os.getenv('PORT')
```

**Error: "Build timeout"**
```bash
# For large projects, increase timeout in Render settings
# Or optimize build process
```

## Rollback Strategy

### Render Rollback
1. Go to Dashboard → Your Service
2. Click **"Manual Deploy"** → **"Clear build cache & deploy"**
3. Or: Select previous deployment and redeploy

### Vercel Rollback
1. Go to Deployments tab
2. Find previous successful deployment
3. Click **"•••"** → **"Promote to Production"**

## Security Checklist

- ✅ Environment variables set correctly
- ✅ No secrets in code
- ✅ HTTPS enabled (automatic)
- ✅ CORS configured properly
- ✅ `.env` files in `.gitignore`
- ✅ API endpoints secured

## Post-Deployment Testing

### Test Checklist
1. ✅ Homepage loads correctly
2. ✅ Crop recommendation page accessible
3. ✅ Sample data button works
4. ✅ Predictions return results
5. ✅ Dark/light theme switches
6. ✅ Responsive on mobile
7. ✅ Backend health check passes
8. ✅ No console errors

### Performance Testing
```bash
# Test backend response time
curl -w "@-" -o /dev/null -s https://fertismart-backend.onrender.com/api/health << 'EOF'
time_total: %{time_total}s
EOF
```

## Cost Breakdown

### Free Tier (Current)
- **Render**: $0/month
  - 750 hours/month free
  - Sleeps after 15 min inactivity
  
- **Vercel**: $0/month
  - Unlimited deployments
  - 100GB bandwidth/month
  
- **Total**: $0/month

### Recommended Paid (For Production)
- **Render Starter**: $7/month
  - Always-on service
  - No sleep
  
- **Vercel Pro**: $20/month
  - Team collaboration
  - Analytics
  
- **Total**: $27/month

## Continuous Deployment

### Auto-Deploy on Push

**Render:**
- Automatically deploys on git push to master
- Can configure deploy hooks

**Vercel:**
- Automatically deploys on git push
- Preview deployments for branches
- Production deployment on master

### Deploy Workflow
```bash
# 1. Make changes
# 2. Test locally
npm run dev  # Frontend
python simple_app.py  # Backend

# 3. Commit and push
git add .
git commit -m "Your changes"
git push origin master

# 4. Automatic deployment
# Vercel: ~2 minutes
# Render: ~5 minutes
```

## Support & Resources

### Official Documentation
- [Render Docs](https://render.com/docs)
- [Vercel Docs](https://vercel.com/docs)
- [Next.js Docs](https://nextjs.org/docs)
- [Flask Docs](https://flask.palletsprojects.com/)

### FertiSmart Resources
- Repository: `https://github.com/SiddhantB10/FertiSmart`
- Issues: Report bugs and request features
- Discussions: Community support

---

**Last Updated**: October 28, 2025  
**Version**: 1.0.0

<div align="center">
  <strong>🌾 FertiSmart - Making Agriculture Smarter with AI 🌾</strong>
</div>
