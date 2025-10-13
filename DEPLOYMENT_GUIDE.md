# FertiSmart Deployment Guide - 100% FREE

## Overview
This guide will help you deploy FertiSmart using completely FREE services:
- **Vercel** (Free Hobby Plan) - Next.js frontend
- **Render** (Free Plan) - Flask backend 
- **Neon** (Free Plan) - PostgreSQL database

## Prerequisites
- GitHub account (free)
- Vercel account (free)
- Render account (free) 
- Neon account (free)

## Step 1: Setup Free Database (Neon)

### 1.1 Create Neon Database
1. Go to [neon.tech](https://neon.tech) and sign up (free)
2. Click "Create Project"
3. Name your project "FertiSmart"
4. Select region closest to you
5. Copy the connection string (starts with `postgresql://`)

## Step 2: Deploy Backend to Render (Free)

### 2.1 Create Render Web Service
1. Go to [render.com](https://render.com) and sign up (free)
2. Click "New" → "Web Service"
3. Connect your GitHub account and select FertiSmart repository
4. Configure the service:
   - **Name**: `fertismart-backend`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn simple_app:app --bind 0.0.0.0:$PORT`

### 2.2 Add Environment Variables
In Render dashboard, add these environment variables:
```
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-change-this
FRONTEND_URL=https://fertismart.vercel.app
DEBUG=False
LOG_LEVEL=INFO
DATABASE_URL=postgresql://your-neon-connection-string
```

### 2.3 Deploy
1. Click "Create Web Service"
2. Render will build and deploy (takes 5-10 minutes first time)
3. Note your backend URL (e.g., `https://fertismart-backend.onrender.com`)
4. Test health endpoint: `https://your-backend-url.onrender.com/api/health`

**Important**: Free Render services sleep after 15 minutes of inactivity and take 30+ seconds to wake up.

## Step 3: Deploy Frontend to Vercel

### 3.1 Update Vercel Configuration
1. Update the `vercel.json` file with your actual backend URL:
   ```json
   {
     "rewrites": [
       {
         "source": "/api/(.*)",
         "destination": "https://fertismart-backend.onrender.com"
       }
     ]
   }
   ```

### 3.2 Deploy to Vercel
1. Go to [vercel.com](https://vercel.com) and sign in
2. Click "New Project" → "Import Git Repository"
3. Select your FertiSmart repository
4. **DO NOT** set Root Directory (leave empty - deploy from root)
5. Add environment variable:
   ```
   NEXT_PUBLIC_API_URL=https://fertismart-backend.onrender.com
   ```
6. Click "Deploy"

### 3.3 Update CORS (Important!)
1. Go back to Render dashboard
2. Update the `FRONTEND_URL` environment variable with your actual Vercel URL:
   ```
   FRONTEND_URL=https://fertismart.vercel.app
   ```
3. Redeploy the backend service

## Step 4: Test Your Deployment

1. **Frontend**: Visit your Vercel URL
2. **Backend Health**: Check `https://your-backend-url.onrender.com/api/health`
3. **API Connection**: Test the crop recommendation feature on your frontend

## Environment Variables Reference

### Render (Backend)
```
FLASK_ENV=production
SECRET_KEY=your-super-secret-key
FRONTEND_URL=https://fertismart.vercel.app
DEBUG=False
DATABASE_URL=postgresql://your-neon-connection-string
PORT=auto-set by Render
```

### Vercel (Frontend)
```
NEXT_PUBLIC_API_URL=https://fertismart-backend.onrender.com
```

## Free Tier Limitations

### Render Free Tier
- ✅ 750 hours/month (enough for full-time usage)
- ❌ Sleeps after 15 minutes of inactivity 
- ❌ 30+ second wake-up time (cold starts)
- ✅ 500MB memory, sufficient for ML model
- ✅ No credit card required

### Neon Free Tier  
- ✅ 3GB storage (plenty for your data)
- ✅ 1 database
- ✅ No credit card required
- ❌ Database may pause after 7 days of inactivity

### Vercel Free Tier
- ✅ 100 deployments/month 
- ✅ 100GB bandwidth/month
- ✅ Custom domain support
- ✅ No credit card required

## Common Issues & Solutions

### 1. Cold Starts (Render)
- First request after inactivity takes 30+ seconds
- Solution: Use a service like UptimeRobot to ping your app every 14 minutes
- Or accept cold starts for demo/personal use

### 2. CORS Errors
- Ensure `FRONTEND_URL` in Render matches your Vercel domain exactly
- Check that CORS is properly configured in Flask app

### 3. Model Training Timeout
- Render free tier has build timeout limits
- The scikit-learn model should train quickly with your dataset
- Consider pre-training and uploading model files if needed

### 4. Database Connection Issues
- Verify Neon `DATABASE_URL` is correct in Render environment variables
- Ensure Neon database is not paused

### 5. Build Failures
- Check build logs in both Vercel and Render dashboards
- Ensure all dependencies are in requirements.txt
- Verify Python version compatibility

## Keeping Your App Awake (Optional)

### Free Monitoring Services:
1. **UptimeRobot** (free) - ping your Render app every 5 minutes
2. **Cronitor** (free tier) - health check monitoring  
3. **BetterUptime** (free tier) - uptime monitoring

Set up a ping to `https://your-backend.onrender.com/api/health` every 14 minutes.

## Monitoring & Logs
- **Render**: View logs in the Render dashboard
- **Vercel**: View function logs in Vercel dashboard  
- **Neon**: Monitor database usage in Neon console

## Alternative Free Options

If Render doesn't work for you:
- **Fly.io** - Free tier with 3 shared VMs
- **Railway** - $5 trial credits (not permanently free)
- **Cyclic** - Serverless deployment (may have cold starts)

## Support
If you encounter issues:
1. Check the logs in both Render and Vercel dashboards
2. Verify all environment variables are set correctly
3. Test API endpoints directly using the browser or Postman
4. Join the Render/Vercel Discord communities for help

---
**Total Cost: $0/month** 🎉 Perfect for demos, portfolios, and learning!