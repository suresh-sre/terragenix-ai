# Deploy Frontend On Vercel

This repository contains two separate apps:

- `frontend/` is the public Next.js website and Vercel frontend.
- `backend/` is the Flask API and should be deployed separately.

## What should be deployed to Vercel

Deploy the Next.js app from `frontend/`.

If you import the repository root into Vercel, make sure the project is configured to build the frontend app:

- Root Directory: `frontend` is the safest option
- Framework Preset: `Next.js`
- Environment Variable: `NEXT_PUBLIC_API_URL=https://your-backend-url`

The root-level `vercel.json` is included to guide Vercel toward the `frontend` app, but the Vercel dashboard Root Directory setting still takes priority when the project is already linked.

## Recommended setup

1. Create one Vercel project for `frontend/`
2. Create one backend deployment for `backend/` on Heroku, Railway, Render, or AWS
3. Set `NEXT_PUBLIC_API_URL` in Vercel to your deployed backend URL
4. Redeploy the Vercel project

## Why the wrong page appeared

The repository root also contains a Python entrypoint at `index.py`, which imports `backend/index.py`. If Vercel deploys the repository root as a Python app, it serves the older Flask HTML page instead of the newer Next.js landing page.
