# 🌾 FarmAI — Crop Disease Detector

An AI-powered crop disease detection app built for Indian farmers who have no access to agricultural experts.

## 🎯 Problem
Farmers in rural India struggle to identify crop diseases without expert help. Wrong diagnosis leads to wrong pesticides, wasted money, and crop loss.

## ✅ Solution
FarmAI allows farmers to upload a photo of their affected crop along with simple inputs, and get an instant AI-powered diagnosis.

### Farmer Provides:
- 📸 Photo of affected crop
- 🌱 Crop type (Rice, Wheat, Tomato, Cotton, etc.)
- 🪨 Soil type (Red, Black, Sandy, Loamy)
- 💧 Water level (Low, Medium, High)
- ⛅ Recent weather (Sunny, Rainy, Cloudy, Humid)
- 🌿 Stem feel (Hard, Soft, Rotting)
- 🍃 Leaf feel (Dry, Wet, Sticky, Falling)
- 📅 When problem started
- 🐛 Insects visible or not

### AI Responds With:
- 🦠 Disease name
- 🔍 Cause of the disease
- 💊 Treatment steps
- 🧴 Pesticide / Fertilizer recommendation
- 🛡️ Prevention tips

## 🌍 Target Users
Small and rural farmers in India with no access to agricultural experts.

## 💬 Languages Supported
- English
- Tamil (தமிழ்)
- Hindi (हिन्दी)
- Telugu (తెలుగు)
- Kannada (ಕನ್ನಡ)

## 🛠️ Tech Stack
- Python
- Streamlit
- Google Gemini API (gemini-3.5-flash-lite, via the REST API)
- Replit

## ▶️ Run it locally
```bash
cd artifacts/farm-ai
pip install -r requirements.txt
# get a free key at https://aistudio.google.com/api-keys
cp .streamlit/secrets.toml.example .streamlit/secrets.toml   # then paste your key in it
streamlit run app.py
```
You can also set the key as an environment variable: `GEMINI_API_KEY=your-key`.

## ⚠️ Disclaimer
FarmAI is not 100% accurate. Rare diseases might be missed. Always consult a certified agricultural expert for serious cases.

## 👨‍💻 Developer
Built by **Ranjith** — building technology for farmers! 🌱
