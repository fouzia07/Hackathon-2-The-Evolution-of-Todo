# Vercel Deployment Configuration for Frontend

This frontend is deployed on Vercel at: https://vercel.com/fouzia-alees-projects/hackathon-2-the-evolution-of-todo

## Important: Backend Deployment Required

⚠️ **The frontend CANNOT work without a deployed backend.** The backend is currently only running on `localhost:8001`, which is not accessible from Vercel.

## Steps to Fix 404 Error and Deploy Successfully

### Step 1: Configure Vercel Project Settings

1. Go to your Vercel project: https://vercel.com/fouzia-alees-projects/hackathon-2-the-evolution-of-todo
2. Go to **Settings** → **General**
3. Set **Root Directory** to: `phase-02-fullstack-app/frontend`
4. Set **Framework Preset** to: `Next.js`
5. Click **Save**

### Step 2: Deploy Backend First

You need to deploy your backend to a cloud service. Options:

**Option A: Railway (Recommended)**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Deploy backend
cd phase-02-fullstack-app/backend
railway init
railway up
```

**Option B: Render**
1. Go to https://render.com
2. Create new Web Service
3. Connect your GitHub repo
4. Set Root Directory: `phase-02-fullstack-app/backend`
5. Build Command: `pip install -r requirements.txt`
6. Start Command: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`

**Option C: Heroku**
```bash
# Install Heroku CLI and login
heroku login

# Create app and deploy
cd phase-02-fullstack-app/backend
heroku create your-todo-backend
git push heroku main
```

### Step 3: Configure Environment Variables in Vercel

Once your backend is deployed, you'll have a URL (e.g., `https://your-backend.railway.app`).

1. Go to Vercel project → **Settings** → **Environment Variables**
2. Add these variables:

```
NEXT_PUBLIC_API_URL=https://your-backend-url.com
NEXT_PUBLIC_BETTER_AUTH_URL=https://your-vercel-app.vercel.app
BETTER_AUTH_SECRET=zSbfPlGje2OWZ2I4Bvvugd91zE0TT6lv
```

### Step 4: Update Backend CORS Settings

After deploying backend, update `phase-02-fullstack-app/backend/src/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.frontend_url,
        "http://localhost:3000",
        "https://your-vercel-app.vercel.app"  # Add your Vercel URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Step 5: Redeploy Frontend

After completing steps 1-4:
1. Go to Vercel project → **Deployments**
2. Click **Redeploy** on the latest deployment
3. Or push a new commit to trigger automatic deployment

## Current Status

- ❌ Backend: Not deployed (running only on localhost)
- ❌ Frontend: Deployed but getting 404 (wrong root directory)
- ❌ Environment Variables: Not configured for production

## Quick Fix for Testing

If you just want to test locally:
1. Keep backend running on `localhost:8001`
2. Keep frontend running on `localhost:3000`
3. Don't use Vercel deployment yet

## Database Configuration

Make sure your backend's `.env` file has the production database URL:
```
DATABASE_URL=postgresql://user:password@host:5432/database
```

Your Neon database should work in production.
