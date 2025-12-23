# Deploying Hardscapes Backend to Railway

## Prerequisites
- GitHub repository with the code pushed
- Railway account (sign up at https://railway.app)

## Deployment Steps

### 1. Create New Project on Railway
1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Authorize Railway to access your GitHub
5. Select the hardscapes_back repository

### 2. Configure the Service
Railway will automatically detect this as a Python project and use the configuration from `railway.json`.

The deployment process will:
- Install Python dependencies from `requirements.txt`
- Run `build_words.py` to create the word database
- Start the API server using uvicorn

### 3. Add Environment Variables (if needed)
Currently no environment variables are required, but if you add database URLs or API keys later:
1. In Railway dashboard, go to your service
2. Click "Variables" tab
3. Add your environment variables

### 4. Configure Domain
1. In Railway dashboard, click "Settings"
2. Under "Domains", click "Generate Domain"
3. Railway will provide a URL like `https://your-app.up.railway.app`

### 5. Update CORS in api.py
Once you have your Railway domain, update the CORS configuration in `api.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "https://*.vercel.app",
        "https://your-app.up.railway.app",  # Add your Railway domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 6. Update Frontend API URL
In your portfolio frontend, update the environment variable to point to your Railway API:
```
VITE_HARDSCAPES_API_URL=https://your-app.up.railway.app
```

## Monitoring
- View logs in Railway dashboard under "Deployments" → "View Logs"
- Check metrics under "Metrics" tab
- Railway will automatically redeploy when you push to GitHub

## Troubleshooting

### Build Fails
- Check the build logs in Railway dashboard
- Ensure `build_words.py` completes successfully
- Verify all dependencies in `requirements.txt` are correct

### Database Not Found
- Ensure `build_words.py` is running during the build phase
- Check that `data/cefr.csv` exists in the repository
- Verify the build command in `railway.json`

### CORS Errors
- Add your frontend domain to the `allow_origins` list in `api.py`
- Ensure the domain is using HTTPS (Railway provides this automatically)

## Cost
Railway offers:
- $5/month free tier (with verification)
- Pay-as-you-go pricing after that
- This small API should easily fit within the free tier

## Manual Deployment Commands (Alternative)
If you prefer to deploy manually:
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize and deploy
railway init
railway up
```
