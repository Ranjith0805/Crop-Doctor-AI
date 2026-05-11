import streamlit as st
import os
import json
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.environ.get("AI_INTEGRATIONS_GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

st.set_page_config(
    page_title="FarmAI - Crop Disease Detector",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed",
)

TRANSLATIONS = {
    "English": {
        "title": "🌿 FarmAI",
        "subtitle": "AI-Powered Crop Disease Detector",
        "tagline": "Upload a photo of your crop and answer a few questions. FarmAI will help identify the disease and suggest treatment.",
        "lang_label": "Select Language / भाषा चुनें",
        "section_photo": "📷 Crop Photo",
        "upload_label": "Upload a photo of the affected crop",
        "section_details": "🌾 Crop Details",
        "crop_type": "Crop Type",
        "soil_type": "Soil Type",
        "water_level": "Water Level",
        "weather": "Recent Weather",
        "stem_feel": "Stem Feel",
        "leaf_feel": "Leaf Feel",
        "problem_start": "When Did the Problem Start?",
        "insects": "Are Insects Visible on the Crop?",
        "submit": "🔍 Analyze My Crop",
        "analyzing": "🔬 Analyzing your crop... Please wait.",
        "result_title": "🩺 Diagnosis Result",
        "disease_name": "Disease Name",
        "cause": "Cause",
        "treatment": "Treatment Steps",
        "pesticide": "Pesticide / Fertilizer Recommendation",
        "prevention": "Prevention Tips",
        "disclaimer": "⚠️ Disclaimer: This analysis is AI-generated and not 100% accurate. Please consult a qualified agricultural expert for serious crop issues.",
        "no_photo": "Please upload a photo of the affected crop before submitting.",
        "error_msg": "An error occurred while analyzing. Please try again.",
        "crops": ["Rice", "Wheat", "Tomato", "Cotton", "Maize", "Sugarcane", "Potato", "Soybean", "Groundnut", "Onion", "Other"],
        "soils": ["Red Soil", "Black Soil", "Sandy Soil", "Loamy Soil", "Clay Soil", "Other"],
        "water_levels": ["Low", "Medium", "High"],
        "weathers": ["Sunny", "Rainy", "Cloudy", "Humid"],
        "stems": ["Hard", "Soft", "Rotting"],
        "leaves": ["Dry", "Wet", "Sticky", "Falling"],
        "problem_times": ["Today", "2-3 days ago", "1 week ago", "More than 1 week"],
        "insects_opts": ["Yes", "No"],
    },
    "हिन्दी (Hindi)": {
        "title": "🌿 फार्मAI",
        "subtitle": "AI-आधारित फसल रोग पहचानकर्ता",
        "tagline": "अपनी फसल की एक फोटो अपलोड करें और कुछ सवालों के जवाब दें। FarmAI रोग पहचानने और उपचार सुझाने में मदद करेगा।",
        "lang_label": "Select Language / भाषा चुनें",
        "section_photo": "📷 फसल की फोटो",
        "upload_label": "प्रभावित फसल की एक फोटो अपलोड करें",
        "section_details": "🌾 फसल की जानकारी",
        "crop_type": "फसल का प्रकार",
        "soil_type": "मिट्टी का प्रकार",
        "water_level": "पानी का स्तर",
        "weather": "हाल का मौसम",
        "stem_feel": "तने का अहसास",
        "leaf_feel": "पत्ते का अहसास",
        "problem_start": "समस्या कब शुरू हुई?",
        "insects": "क्या फसल पर कीड़े दिख रहे हैं?",
        "submit": "🔍 मेरी फसल का विश्लेषण करें",
        "analyzing": "🔬 आपकी फसल का विश्लेषण हो रहा है... कृपया प्रतीक्षा करें।",
        "result_title": "🩺 निदान परिणाम",
        "disease_name": "रोग का नाम",
        "cause": "कारण",
        "treatment": "उपचार के चरण",
        "pesticide": "कीटनाशक / उर्वरक की सिफारिश",
        "prevention": "रोकथाम के टिप्स",
        "disclaimer": "⚠️ अस्वीकरण: यह विश्लेषण AI द्वारा उत्पन्न है और 100% सटीक नहीं है। गंभीर फसल समस्याओं के लिए कृपया किसी योग्य कृषि विशेषज्ञ से सलाह लें।",
        "no_photo": "सबमिट करने से पहले कृपया प्रभावित फसल की एक फोटो अपलोड करें।",
        "error_msg": "विश्लेषण के दौरान एक त्रुटि हुई। कृपया पुनः प्रयास करें।",
        "crops": ["चावल", "गेहूं", "टमाटर", "कपास", "मक्का", "गन्ना", "आलू", "सोयाबीन", "मूंगफली", "प्याज", "अन्य"],
        "soils": ["लाल मिट्टी", "काली मिट्टी", "रेतीली मिट्टी", "दोमट मिट्टी", "चिकनी मिट्टी", "अन्य"],
        "water_levels": ["कम", "मध्यम", "अधिक"],
        "weathers": ["धूप", "बारिश", "बादल", "उमस"],
        "stems": ["कठोर", "मुलायम", "सड़ा हुआ"],
        "leaves": ["सूखा", "गीला", "चिपचिपा", "झड़ रहा है"],
        "problem_times": ["आज", "2-3 दिन पहले", "1 सप्ताह पहले", "1 सप्ताह से अधिक"],
        "insects_opts": ["हाँ", "नहीं"],
    },
    "தமிழ் (Tamil)": {
        "title": "🌿 பண்ணைAI",
        "subtitle": "AI-இயக்கும் பயிர் நோய் கண்டுபிடிப்பான்",
        "tagline": "உங்கள் பயிரின் ஒரு புகைப்படத்தை பதிவேற்றி சில கேள்விகளுக்கு பதிலளிக்கவும். FarmAI நோயை கண்டறிந்து சிகிச்சை பரிந்துரைக்க உதவும்.",
        "lang_label": "Select Language / மொழியை தேர்ந்தெடுக்கவும்",
        "section_photo": "📷 பயிர் புகைப்படம்",
        "upload_label": "பாதிக்கப்பட்ட பயிரின் புகைப்படத்தை பதிவேற்றவும்",
        "section_details": "🌾 பயிர் விவரங்கள்",
        "crop_type": "பயிர் வகை",
        "soil_type": "மண் வகை",
        "water_level": "நீர் அளவு",
        "weather": "சமீபத்திய வானிலை",
        "stem_feel": "தண்டு உணர்வு",
        "leaf_feel": "இலை உணர்வு",
        "problem_start": "பிரச்சனை எப்போது தொடங்கியது?",
        "insects": "பயிரில் பூச்சிகள் தெரிகிறதா?",
        "submit": "🔍 என் பயிரை பகுப்பாய்வு செய்",
        "analyzing": "🔬 உங்கள் பயிரை பகுப்பாய்வு செய்கிறோம்... தயவுசெய்து காத்திருக்கவும்.",
        "result_title": "🩺 நோய் கண்டறிதல் முடிவு",
        "disease_name": "நோயின் பெயர்",
        "cause": "காரணம்",
        "treatment": "சிகிச்சை படிகள்",
        "pesticide": "பூச்சிக்கொல்லி / உரம் பரிந்துரை",
        "prevention": "தடுப்பு குறிப்புகள்",
        "disclaimer": "⚠️ மறுப்பு: இந்த பகுப்பாய்வு AI-ஆல் உருவாக்கப்பட்டது மற்றும் 100% துல்லியமாக இல்லை. தீவிரமான பயிர் பிரச்சனைகளுக்கு தகுதியான வேளாண் நிபுணரை கலந்தாலோசிக்கவும்.",
        "no_photo": "சமர்ப்பிக்கும் முன் பாதிக்கப்பட்ட பயிரின் புகைப்படத்தை பதிவேற்றவும்.",
        "error_msg": "பகுப்பாய்வு செய்யும் போது பிழை ஏற்பட்டது. மீண்டும் முயற்சிக்கவும்.",
        "crops": ["நெல்", "கோதுமை", "தக்காளி", "பருத்தி", "மக்காச்சோளம்", "கரும்பு", "உருளைக்கிழங்கு", "சோயா", "வேர்க்கடலை", "வெங்காயம்", "மற்றவை"],
        "soils": ["சிவப்பு மண்", "கரும் மண்", "மணல் மண்", "வண்டல் மண்", "களிமண்", "மற்றவை"],
        "water_levels": ["குறைவு", "நடுத்தரம்", "அதிகம்"],
        "weathers": ["வெயில்", "மழை", "மேகமூட்டம்", "ஈரப்பதம்"],
        "stems": ["கடினமான", "மென்மையான", "அழுகிய"],
        "leaves": ["உலர்ந்த", "ஈரமான", "ஒட்டும்", "உதிர்கின்ற"],
        "problem_times": ["இன்று", "2-3 நாட்களுக்கு முன்பு", "1 வாரத்திற்கு முன்பு", "1 வாரத்திற்கும் மேல்"],
        "insects_opts": ["ஆம்", "இல்லை"],
    },
    "తెలుగు (Telugu)": {
        "title": "🌿 వ్యవసాయ AI",
        "subtitle": "AI-ఆధారిత పంట వ్యాధి గుర్తింపు",
        "tagline": "మీ పంట ఫోటోను అప్‌లోడ్ చేసి కొన్ని ప్రశ్నలకు సమాధానం ఇవ్వండి. FarmAI వ్యాధిని గుర్తించి చికిత్స సూచించడంలో సహాయపడుతుంది.",
        "lang_label": "Select Language / భాషను ఎంచుకోండి",
        "section_photo": "📷 పంట ఫోటో",
        "upload_label": "ప్రభావిత పంట ఫోటోను అప్‌లోడ్ చేయండి",
        "section_details": "🌾 పంట వివరాలు",
        "crop_type": "పంట రకం",
        "soil_type": "మట్టి రకం",
        "water_level": "నీటి స్థాయి",
        "weather": "ఇటీవలి వాతావరణం",
        "stem_feel": "కాండం స్పర్శ",
        "leaf_feel": "ఆకు స్పర్శ",
        "problem_start": "సమస్య ఎప్పుడు మొదలైంది?",
        "insects": "పంటపై పురుగులు కనిపిస్తున్నాయా?",
        "submit": "🔍 నా పంటను విశ్లేషించు",
        "analyzing": "🔬 మీ పంటను విశ్లేషిస్తున్నాము... దయచేసి వేచి ఉండండి.",
        "result_title": "🩺 రోగనిర్ధారణ ఫలితం",
        "disease_name": "వ్యాధి పేరు",
        "cause": "కారణం",
        "treatment": "చికిత్స దశలు",
        "pesticide": "పురుగుమందు / ఎరువు సిఫారసు",
        "prevention": "నివారణ చిట్కాలు",
        "disclaimer": "⚠️ నిరాకరణ: ఈ విశ్లేషణ AI-రూపొందించినది మరియు 100% ఖచ్చితమైనది కాదు. తీవ్రమైన పంట సమస్యలకు దయచేసి అర్హత కలిగిన వ్యవసాయ నిపుణుడిని సంప్రదించండి.",
        "no_photo": "సమర్పించే ముందు ప్రభావిత పంట ఫోటోను అప్‌లోడ్ చేయండి.",
        "error_msg": "విశ్లేషించే సమయంలో లోపం ఏర్పడింది. దయచేసి మళ్ళీ ప్రయత్నించండి.",
        "crops": ["వరి", "గోధుమ", "టమాటో", "పత్తి", "మొక్కజొన్న", "చెరకు", "బంగాళాదుంప", "సోయాబీన్", "వేరుశెనగ", "ఉల్లిపాయ", "ఇతర"],
        "soils": ["ఎర్ర మట్టి", "నల్ల మట్టి", "ఇసుక మట్టి", "లోమి మట్టి", "సుద్ద మట్టి", "ఇతర"],
        "water_levels": ["తక్కువ", "మధ్యస్థ", "అధిక"],
        "weathers": ["ఎండ", "వర్షం", "మేఘావృతం", "తేమ"],
        "stems": ["గట్టి", "మెత్తని", "కుళ్ళిన"],
        "leaves": ["ఎండిన", "తడిగా", "అంటుకునే", "రాలిపడే"],
        "problem_times": ["ఈరోజు", "2-3 రోజుల క్రితం", "1 వారం క్రితం", "1 వారం కంటే ఎక్కువ"],
        "insects_opts": ["అవును", "కాదు"],
    },
    "ಕನ್ನಡ (Kannada)": {
        "title": "🌿 ಕೃಷಿ AI",
        "subtitle": "AI-ಚಾಲಿತ ಬೆಳೆ ರೋಗ ಪತ್ತೆಕಾರ",
        "tagline": "ನಿಮ್ಮ ಬೆಳೆಯ ಒಂದು ಫೋಟೋ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ ಮತ್ತು ಕೆಲವು ಪ್ರಶ್ನೆಗಳಿಗೆ ಉತ್ತರಿಸಿ. FarmAI ರೋಗ ಗುರುತಿಸಲು ಮತ್ತು ಚಿಕಿತ್ಸೆ ಸೂಚಿಸಲು ಸಹಾಯ ಮಾಡುತ್ತದೆ.",
        "lang_label": "Select Language / ಭಾಷೆಯನ್ನು ಆಯ್ಕೆ ಮಾಡಿ",
        "section_photo": "📷 ಬೆಳೆ ಫೋಟೋ",
        "upload_label": "ಪ್ರಭಾವಿತ ಬೆಳೆಯ ಫೋಟೋ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ",
        "section_details": "🌾 ಬೆಳೆ ವಿವರಗಳು",
        "crop_type": "ಬೆಳೆ ಪ್ರಕಾರ",
        "soil_type": "ಮಣ್ಣಿನ ಪ್ರಕಾರ",
        "water_level": "ನೀರಿನ ಮಟ್ಟ",
        "weather": "ಇತ್ತೀಚಿನ ಹವಾಮಾನ",
        "stem_feel": "ಕಾಂಡದ ಸ್ಪರ್ಶ",
        "leaf_feel": "ಎಲೆಯ ಸ್ಪರ್ಶ",
        "problem_start": "ಸಮಸ್ಯೆ ಯಾವಾಗ ಪ್ರಾರಂಭವಾಯಿತು?",
        "insects": "ಬೆಳೆಯ ಮೇಲೆ ಕೀಟಗಳು ಕಾಣಿಸುತ್ತಿವೆಯೇ?",
        "submit": "🔍 ನನ್ನ ಬೆಳೆಯನ್ನು ವಿಶ್ಲೇಷಿಸಿ",
        "analyzing": "🔬 ನಿಮ್ಮ ಬೆಳೆಯನ್ನು ವಿಶ್ಲೇಷಿಸಲಾಗುತ್ತಿದೆ... ದಯವಿಟ್ಟು ಕಾಯಿರಿ.",
        "result_title": "🩺 ರೋಗನಿರ್ಣಯ ಫಲಿತಾಂಶ",
        "disease_name": "ರೋಗದ ಹೆಸರು",
        "cause": "ಕಾರಣ",
        "treatment": "ಚಿಕಿತ್ಸೆ ಹಂತಗಳು",
        "pesticide": "ಕೀಟನಾಶಕ / ಗೊಬ್ಬರ ಶಿಫಾರಸು",
        "prevention": "ತಡೆಗಟ್ಟುವ ಸಲಹೆಗಳು",
        "disclaimer": "⚠️ ಹಕ್ಕು ನಿರಾಕರಣೆ: ಈ ವಿಶ್ಲೇಷಣೆ AI-ಉತ್ಪಾದಿತ ಮತ್ತು 100% ನಿಖರವಾಗಿಲ್ಲ. ಗಂಭೀರ ಬೆಳೆ ಸಮಸ್ಯೆಗಳಿಗೆ ದಯವಿಟ್ಟು ಅರ್ಹ ಕೃಷಿ ತಜ್ಞರನ್ನು ಸಂಪರ್ಕಿಸಿ.",
        "no_photo": "ಸಲ್ಲಿಸುವ ಮೊದಲು ಪ್ರಭಾವಿತ ಬೆಳೆಯ ಫೋಟೋ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ.",
        "error_msg": "ವಿಶ್ಲೇಷಣೆ ಸಮಯದಲ್ಲಿ ದೋಷ ಸಂಭವಿಸಿದೆ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.",
        "crops": ["ಭತ್ತ", "ಗೋಧಿ", "ಟೊಮೆಟೊ", "ಹತ್ತಿ", "ಮೆಕ್ಕೆ ಜೋಳ", "ಕಬ್ಬು", "ಆಲೂಗೆಡ್ಡೆ", "ಸೋಯಾಬೀನ್", "ಶೇಂಗಾ", "ಈರುಳ್ಳಿ", "ಇತರೆ"],
        "soils": ["ಕೆಂಪು ಮಣ್ಣು", "ಕಪ್ಪು ಮಣ್ಣು", "ಮರಳು ಮಣ್ಣು", "ಲೋಮಿ ಮಣ್ಣು", "ಜೇಡಿ ಮಣ್ಣು", "ಇತರೆ"],
        "water_levels": ["ಕಡಿಮೆ", "ಮಧ್ಯಮ", "ಹೆಚ್ಚು"],
        "weathers": ["ಬಿಸಿಲು", "ಮಳೆ", "ಮೋಡ", "ತೇವ"],
        "stems": ["ಗಟ್ಟಿ", "ಮೃದು", "ಕೊಳೆತ"],
        "leaves": ["ಒಣ", "ಒದ್ದೆ", "ಅಂಟಂಟ", "ಉದುರುತ್ತಿರುವ"],
        "problem_times": ["ಇಂದು", "2-3 ದಿನಗಳ ಹಿಂದೆ", "1 ವಾರದ ಹಿಂದೆ", "1 ವಾರಕ್ಕಿಂತ ಹೆಚ್ಚು"],
        "insects_opts": ["ಹೌದು", "ಇಲ್ಲ"],
    },
}


def build_prompt(lang, crop, soil, water, weather, stem, leaf, problem_start, insects, image_provided):
    lang_instruction = {
        "English": "Respond in English.",
        "हिन्दी (Hindi)": "Respond in Hindi (हिन्दी में जवाब दें).",
        "தமிழ் (Tamil)": "Respond in Tamil (தமிழில் பதிலளிக்கவும்).",
        "తెలుగు (Telugu)": "Respond in Telugu (తెలుగులో సమాధానం ఇవ్వండి).",
        "ಕನ್ನಡ (Kannada)": "Respond in Kannada (ಕನ್ನಡದಲ್ಲಿ ಉತ್ತರಿಸಿ).",
    }.get(lang, "Respond in English.")

    photo_note = "A photo of the affected crop has been provided. Carefully analyze it for visible symptoms such as discoloration, spots, lesions, wilting, or pest damage." if image_provided else "No photo was provided. Use the field observations below to make your best assessment."

    prompt = f"""You are FarmAI, an expert agricultural AI assistant for Indian farmers. {lang_instruction}

{photo_note}

Farmer's field observations:
- Crop type: {crop}
- Soil type: {soil}
- Water level: {water}
- Recent weather: {weather}
- Stem feel: {stem}
- Leaf feel: {leaf}
- Problem started: {problem_start}
- Insects visible: {insects}

Based on the photo (if provided) and all the above observations, provide a detailed diagnosis. You MUST respond with a valid JSON object and nothing else — no markdown, no explanation outside the JSON.

Return this exact JSON structure:
{{
  "disease_name": "Name of the disease or condition",
  "cause": "What causes this disease (pathogen, environmental, nutritional, pest, etc.)",
  "treatment": ["Step 1", "Step 2", "Step 3", "Step 4"],
  "pesticide": "Specific pesticide or fertilizer name, dosage, and application method",
  "prevention": ["Prevention tip 1", "Prevention tip 2", "Prevention tip 3"]
}}

Be specific, practical, and use language simple enough for a rural farmer to understand. Give actionable advice suitable for Indian farming conditions."""
    return prompt


def analyze_crop(lang, image_bytes, image_mime, crop, soil, water, weather, stem, leaf, problem_start, insects):
    prompt = build_prompt(lang, crop, soil, water, weather, stem, leaf, problem_start, insects, image_bytes is not None)

    contents = []

    if image_bytes:
        import PIL.Image
        import io
        pil_image = PIL.Image.open(io.BytesIO(image_bytes))
        contents.append(pil_image)

    contents.append(prompt)

    response = model.generate_content(
        contents,
        generation_config=genai.types.GenerationConfig(
            max_output_tokens=8192,
            temperature=0.3,
        ),
    )

    raw = response.text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    return json.loads(raw)


def main():
    lang_options = list(TRANSLATIONS.keys())

    if "language" not in st.session_state:
        st.session_state.language = "English"

    t = TRANSLATIONS[st.session_state.language]

    st.selectbox(
        t["lang_label"],
        lang_options,
        index=lang_options.index(st.session_state.language),
        key="language",
    )

    t = TRANSLATIONS[st.session_state.language]

    st.title(t["title"])
    st.subheader(t["subtitle"])
    st.write(t["tagline"])
    st.divider()

    st.subheader(t["section_photo"])
    uploaded_file = st.file_uploader(
        t["upload_label"],
        type=["jpg", "jpeg", "png", "webp"],
        label_visibility="visible",
    )

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, use_container_width=True, caption="📷 Uploaded crop photo")

    st.divider()
    st.subheader(t["section_details"])

    col1, col2 = st.columns(2)
    with col1:
        crop = st.selectbox(t["crop_type"], t["crops"])
        soil = st.selectbox(t["soil_type"], t["soils"])
    with col2:
        water = st.radio(t["water_level"], t["water_levels"], horizontal=False)
        weather = st.radio(t["weather"], t["weathers"], horizontal=False)

    st.divider()

    col3, col4 = st.columns(2)
    with col3:
        stem = st.radio(t["stem_feel"], t["stems"])
        leaf = st.radio(t["leaf_feel"], t["leaves"])
    with col4:
        problem_start = st.radio(t["problem_start"], t["problem_times"])
        insects = st.radio(t["insects"], t["insects_opts"])

    st.divider()

    if st.button(t["submit"], use_container_width=True, type="primary"):
        if not uploaded_file:
            st.warning(t["no_photo"])
        else:
            with st.spinner(t["analyzing"]):
                try:
                    uploaded_file.seek(0)
                    image_bytes = uploaded_file.read()
                    mime_type = uploaded_file.type or "image/jpeg"

                    result = analyze_crop(
                        lang=st.session_state.language,
                        image_bytes=image_bytes,
                        image_mime=mime_type,
                        crop=crop,
                        soil=soil,
                        water=water,
                        weather=weather,
                        stem=stem,
                        leaf=leaf,
                        problem_start=problem_start,
                        insects=insects,
                    )

                    st.success(t["result_title"])
                    st.divider()

                    en = TRANSLATIONS["English"]
                    is_english = st.session_state.language == "English"

                    def heading(emoji, key):
                        label = t[key]
                        if not is_english:
                            label += f" ({en[key]})"
                        return f"### {emoji} {label}"

                    st.markdown(heading("🦠", "disease_name"))
                    st.info(result.get("disease_name", "—"))

                    st.markdown(heading("🔍", "cause"))
                    st.write(result.get("cause", "—"))

                    st.markdown(heading("💊", "treatment"))
                    for i, step in enumerate(result.get("treatment", []), 1):
                        st.markdown(f"**{i}.** {step}")

                    st.markdown(heading("🧴", "pesticide"))
                    st.success(result.get("pesticide", "—"))

                    st.markdown(heading("🛡️", "prevention"))
                    for tip in result.get("prevention", []):
                        st.markdown(f"✅ {tip}")

                except json.JSONDecodeError:
                    st.error(t["error_msg"])
                    st.write("Raw AI response could not be parsed. Please try again.")
                except Exception as e:
                    st.error(t["error_msg"])
                    st.write(str(e))

    st.divider()
    st.warning(t["disclaimer"])


if __name__ == "__main__":
    main()
