# Environment Management

This repo keeps environment values out of source control and uses the same names across local development, GitHub Actions, and Render.

## Local development

Copy `.env.example` to `.env` for local values. The root `.gitignore` already excludes `.env` and `.env.local`.

| Variable | Used by | Purpose |
| --- | --- | --- |
| `VITE_API_BASE_URL` | React | Base URL for the analytics API. Vite exposes only variables prefixed with `VITE_`. |
| `FRONTEND_ORIGINS` | Java, Python | Comma-separated origins allowed through CORS. |
| `DATABASE_URL` | Python | Optional Postgres connection string. If unset, the analytics service uses local JSON fallback data. |
| `CREATOR_METRICS_API_URL` | Python | Optional remote JSON metrics source used before local fallback data. |

## GitHub Actions

The workflows use GitHub Actions variables for non-secret build-time values:

- `VITE_API_BASE_URL`
- `FRONTEND_ORIGINS`

Set them in GitHub under `Settings > Secrets and variables > Actions > Variables`.

Use GitHub Actions secrets only for sensitive values. The current CI jobs do not require `DATABASE_URL` or API credentials.

## Render

`render.yaml` defines Render services for the React frontend, Java backend, and Python analytics API. Each service uses `autoDeployTrigger: commit`, so Render deploys commits pushed to the linked branch.

The Blueprint marks runtime values with `sync: false`. Render asks for these values when the Blueprint is first created, and they should be managed in the Render dashboard after that:

- Frontend `VITE_API_BASE_URL`: public URL for `creatoriq-analytics-python`, for example `https://creatoriq-analytics-python.onrender.com`.
- Java `FRONTEND_ORIGINS`: public frontend origin, for example `https://creatoriq-react-frontend.onrender.com`.
- Python `FRONTEND_ORIGINS`: public frontend origin, for example `https://creatoriq-react-frontend.onrender.com`.
- Python `DATABASE_URL`: optional Postgres connection string.
- Python `CREATOR_METRICS_API_URL`: optional remote metrics JSON URL.

Because `VITE_API_BASE_URL` is compiled into the React bundle, redeploy the frontend after changing it.
