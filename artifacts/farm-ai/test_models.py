import os
import google.generativeai as genai

genai.configure(api_key=os.environ.get("AI_INTEGRATIONS_GEMINI_API_KEY"))

print("Available Gemini models:\n")
for model in genai.list_models():
    print(f"  Name:               {model.name}")
    print(f"  Display name:       {model.display_name}")
    print(f"  Supported methods:  {model.supported_generation_methods}")
    print()
