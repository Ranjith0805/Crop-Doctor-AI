# FarmAI

AI-powered crop disease detector for Indian farmers — upload a crop photo, answer a few questions, and get an instant diagnosis with treatment advice.

## Run & Operate

- `cd artifacts/farm-ai && streamlit run app.py --server.port 8000` — run FarmAI (port 8000)
- Workflow name: `FarmAI`
- Required env: `AI_INTEGRATIONS_GEMINI_BASE_URL`, `AI_INTEGRATIONS_GEMINI_API_KEY` — auto-provisioned via Replit AI Integrations

## Stack

- Python 3 + Streamlit 1.45
- Google Gemini AI (`google-genai` SDK, model: `gemini-2.5-flash`)
- Pillow for image handling
- Replit AI Integrations (Gemini proxy — no user API key needed)

## Where things live

- `artifacts/farm-ai/app.py` — main Streamlit application
- `artifacts/farm-ai/.streamlit/config.toml` — Streamlit server + green theme config
- `artifacts/farm-ai/requirements.txt` — Python dependencies

## Architecture decisions

- Uses Replit AI Integrations proxy for Gemini — no user API key required, billed to Replit credits
- Google Gemini `gemini-2.5-flash` model used instead of `gemini-1.5-flash` (1.5-flash not available via Replit proxy)
- AI response is requested as strict JSON for reliable parsing, with markdown fence stripping as fallback
- Image passed inline as base64 bytes (Gemini inline data); no Files API used (unsupported by proxy)
- Multilingual UI via a static translations dict — language selection triggers instant re-render via session state

## Product

- Upload a photo of an affected crop
- Select crop type, soil type, water level, recent weather, stem feel, leaf feel, when problem started, insect visibility
- Receive: disease name, cause, treatment steps, pesticide/fertilizer recommendation, prevention tips
- Supported languages: English, Hindi, Tamil, Telugu, Kannada
- Green-themed mobile-friendly UI with disclaimer

## User preferences

- Language: Tamil, Hindi, Telugu, Kannada, English — all supported
- Design: clean, green themed, farmer-friendly, mobile-first
- Model: Gemini (gemini-2.5-flash via Replit AI Integrations)

## Gotchas

- `AI_INTEGRATIONS_GEMINI_BASE_URL` and `AI_INTEGRATIONS_GEMINI_API_KEY` must be set — run `setupReplitAIIntegrations` in code_execution if missing
- Streamlit runs in `artifacts/farm-ai/` — run the command from that directory or use the absolute path
- `google-genai==2.0.1` installed globally via pip (not in pnpm workspace)

## Pointers

- See the `pnpm-workspace` skill for workspace structure, TypeScript setup, and package details
