# 🚀 FertiSmart Deployment Checklist

## ✅ Pre-Deployment Checklist

### Backend (Railway)
- [x] ✅ Created `Procfile` with gunicorn configuration
- [x] ✅ Added environment variables template (`.env.example`)
- [x] ✅ Updated Flask app for production (CORS, PORT, debug mode)
- [x] ✅ Created `railway.json` deployment configuration
- [x] ✅ Added health check endpoint (`/api/health`)
- [x] ✅ Updated requirements.txt with production dependencies
- [x] ✅ Created `.gitignore` for backend

### Frontend (Vercel)
- [x] ✅ Created `vercel.json` with rewrites and security headers
- [x] ✅ Updated API service for production environment
- [x] ✅ Created `.gitignore` for frontend
- [x] ✅ Package.json has correct build scripts

### Documentation
- [x] ✅ Created comprehensive `DEPLOYMENT_GUIDE.md`
- [x] ✅ Created deployment checklist

## 📋 Deployment Steps

### Step 1: Deploy Backend to Railway
1. [ ] Create Railway account and new project
2. [ ] Connect GitHub repository
3. [ ] Set root directory to `backend`
4. [ ] Add PostgreSQL database service
5. [ ] Configure environment variables:
   - [ ] `FLASK_ENV=production`
   - [ ] `SECRET_KEY=your-secret-key`
   - [ ] `FRONTEND_URL=https://your-app.vercel.app`
   - [ ] `DEBUG=False`
6. [ ] Deploy and test health endpoint
7. [ ] Note backend URL for frontend configuration

### Step 2: Deploy Frontend to Vercel
1. [ ] Create Vercel account and new project
2. [ ] Connect GitHub repository
3. [ ] Set root directory to `frontend`
4. [ ] Update `vercel.json` with actual backend URL
5. [ ] Add environment variable:
   - [ ] `NEXT_PUBLIC_API_URL=https://your-backend.railway.app`
6. [ ] Deploy and test frontend

### Step 3: Final Configuration
1. [ ] Update Railway `FRONTEND_URL` with actual Vercel URL
2. [ ] Redeploy backend to apply CORS changes
3. [ ] Test full application functionality

## 🧪 Testing Checklist

### Backend Tests
- [ ] Health check: `GET https://your-backend.railway.app/api/health`
- [ ] Model info: `GET https://your-backend.railway.app/api/model/info`
- [ ] Crop prediction: `POST https://your-backend.railway.app/api/predict`
- [ ] All crops: `GET https://your-backend.railway.app/api/crops`

### Frontend Tests
- [ ] Homepage loads correctly
- [ ] Navigation works
- [ ] Crop recommendation form works
- [ ] API calls to backend successful
- [ ] No CORS errors in browser console

### Full Integration Tests
- [ ] Submit crop recommendation form
- [ ] Receive prediction results
- [ ] Check analytics page
- [ ] Verify all features work end-to-end

## 🔧 Environment Variables Reference

### Railway (Backend)
```
FLASK_ENV=production
SECRET_KEY=generate-a-strong-secret-key
FRONTEND_URL=https://your-app-name.vercel.app
DEBUG=False
LOG_LEVEL=INFO
DATABASE_URL=postgresql://... (auto-set by Railway)
PORT=auto-set by Railway
```

### Vercel (Frontend)
```
NEXT_PUBLIC_API_URL=https://your-backend-name.railway.app
```

## 🎯 Success Criteria
- [ ] Both services deploy without errors
- [ ] Health checks pass
- [ ] Frontend can communicate with backend
- [ ] ML model trains and makes predictions
- [ ] All application features work in production
- [ ] No console errors or warnings

## 🆘 Troubleshooting
- Check deployment logs in both platforms
- Verify environment variables are set correctly
- Ensure CORS configuration allows frontend domain
- Test API endpoints individually if frontend fails
- Check that ML model data file is included in deployment

---
**Ready to deploy!** 🚀 Follow the `DEPLOYMENT_GUIDE.md` for detailed instructions.