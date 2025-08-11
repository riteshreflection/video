# Deployment Guide

## Quick Start

### 1. GitHub Setup
1. Create a new repository on GitHub
2. Push this code to your repository:
```bash
git init
git add .
git commit -m "Initial commit: YouTube video extraction API"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

### 2. Deploy to Render
1. Go to [render.com](https://render.com) and sign up/login
2. Click "New +" and select "Web Service"
3. Connect your GitHub account and select your repository
4. Render will automatically detect the `render.yaml` configuration
5. Click "Deploy"

### 3. Your API is Live!
Once deployed, your API will be available at:
- `https://your-app-name.onrender.com/`
- `https://your-app-name.onrender.com/video?url=YOUTUBE_URL`

## Manual Render Setup (if render.yaml doesn't work)

If the automatic setup doesn't work, configure manually:

- **Environment**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn --bind 0.0.0.0:$PORT main:app`
- **Environment Variables**: 
  - `SESSION_SECRET`: Generate a random value

## Testing Your Deployed API

Test with these URLs in your browser:
- Service info: `https://your-app.onrender.com/`
- Extract video: `https://your-app.onrender.com/video?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ`
- Health check: `https://your-app.onrender.com/health`

## Troubleshooting

**Common Issues:**
1. **App won't start**: Check the logs in Render dashboard
2. **yt-dlp errors**: YouTube sometimes blocks requests - this is normal
3. **Slow responses**: First request after inactivity may take longer (Render free tier sleeps)

**Performance Tips:**
- Render free tier has limitations
- For production use, consider upgrading to paid plan
- Add error handling for rate limiting

## Alternative Deployment Options

### Heroku
Create `Procfile`:
```
web: gunicorn --bind 0.0.0.0:$PORT main:app
```

### Railway
Works with the same `requirements.txt` and start command.

### Local Development
```bash
pip install -r requirements.txt
python main.py
```
Access at `http://localhost:5000`