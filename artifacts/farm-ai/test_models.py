import os
import requests

key = os.environ.get("GEMINI_API_KEY") or os.environ.get("AI_INTEGRATIONS_GEMINI_API_KEY")
resp = requests.get("https://generativelanguage.googleapis.com/v1beta/models", headers={"x-goog-api-key": key}, timeout=30)
resp.raise_for_status()

print("Available Gemini models:\n")
for m in resp.json().get("models", []):
    print(f"  {m['name']}  ({m.get('displayName', '')})")
