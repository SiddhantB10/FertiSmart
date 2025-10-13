# Keep Your Free App Awake 🏃‍♂️

Since Render free tier sleeps after 15 minutes, here are ways to keep your app awake:

## Option 1: UptimeRobot (Recommended)

1. Go to [uptimerobot.com](https://uptimerobot.com) - FREE account
2. Add New Monitor:
   - Monitor Type: HTTP(s)
   - URL: `https://your-app.onrender.com/api/health`
   - Monitoring Interval: 5 minutes
   - Monitor Timeout: 30 seconds

## Option 2: Cron Job Service

Use [cron-job.org](https://cron-job.org) (free):
- URL: `https://your-app.onrender.com/api/health`
- Schedule: Every 14 minutes

## Option 3: GitHub Actions (Advanced)

Create `.github/workflows/keep-alive.yml`:

```yaml
name: Keep Alive

on:
  schedule:
    - cron: '*/14 * * * *'  # Every 14 minutes

jobs:
  ping:
    runs-on: ubuntu-latest
    steps:
      - name: Ping API
        run: curl https://your-app.onrender.com/api/health
```

## Why Keep It Awake?

- **Without**: 30+ second delay on first request after 15 min
- **With**: Always responsive, better user experience
- **Trade-off**: Slightly more resource usage (still free)

## Alternative: Accept Cold Starts

For demo/portfolio use, cold starts are acceptable:
- Add loading message: "Waking up server (30s)..."
- Perfect for showcasing to employers
- Zero maintenance required

Choose what works for your use case! 🎯