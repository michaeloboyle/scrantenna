# Scrantenna Deployment Guide

## Quick Start - Make It Live

Your Scrantenna daily news site is ready to deploy! Follow these steps to get it live on GitHub Pages:

### Step 1: Create GitHub Repository
```bash
# Option A: Using GitHub CLI (if you have it set up)
gh auth login
gh repo create scrantenna --public --description "Daily news aggregation for Greater Scranton area" --push

# Option B: Manual creation
# 1. Go to https://github.com/new
# 2. Repository name: scrantenna
# 3. Make it public
# 4. Don't initialize with README (we already have files)
# 5. Click "Create repository"
```

### Step 2: Push Your Code
```bash
# Add the GitHub remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/scrantenna.git

# Push the code
git branch -M main
git push -u origin main
```

### Step 3: Set Up Secrets
1. Go to your repository on GitHub
2. Click "Settings" tab
3. Click "Secrets and variables" → "Actions"
4. Click "New repository secret"
5. Name: `NEWSAPI_KEY`
6. Value: `be93936988fd4df185bd56e8a11125a0`
7. Click "Add secret"

### Step 4: Enable GitHub Pages
1. In repository "Settings"
2. Scroll to "Pages" section
3. Source: Select "GitHub Actions"
4. Click "Save"

### Step 5: Trigger First Deployment
1. Go to "Actions" tab in your repository
2. Click "Generate Daily Scranton News" workflow
3. Click "Run workflow" button
4. Click green "Run workflow"

## Your Live URL
Once deployed, your site will be available at:
```
https://YOUR_USERNAME.github.io/scrantenna
```

## Automation Schedule
The site will automatically update daily at:
- **6:00 AM EST** (11:00 AM UTC)
- Or trigger manually via GitHub Actions

## What Gets Deployed
- ✅ Static HTML news page
- ✅ 18+ daily local articles
- ✅ Times-Tribune coverage via RSS
- ✅ WNEP/WBRE local TV news
- ✅ Clean responsive design
- ✅ Mobile-friendly layout

## Troubleshooting
- **No articles showing**: Check that NEWSAPI_KEY secret is set correctly
- **Old articles**: RSS feeds may cache - wait for next automated run
- **Pages not updating**: GitHub Pages can take 5-10 minutes to deploy

## Manual Testing
To test locally:
```bash
source venv/bin/activate
export NEWSAPI_KEY=be93936988fd4df185bd56e8a11125a0
python3 src/daily_news.py
open static/index.html
```

---
Ready to serve the Greater Scranton community with data-driven local journalism!