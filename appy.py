import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Page Setup
st.set_page_config(page_title="Pakistan Board Checker", page_icon="🇵🇰")

st.title("🇵🇰 Pakistan Board Paper Checker AI")
st.write("Valid for Punjab, Federal, Sindh, KPK & Balochistan Boards")
st.subheader("Upload your paper to check Presentation & Mistakes")

# 2. Sidebar for API Key
with st.sidebar:
    st.write("### 🔑 Login")
    api_key = st.text_input("Apni Google Gemini API Key yahan paste karein:", type="password")
    st.info("Ye key safe rahegi. Sirf check karne ke liye use hogi.")

# 3. Agent ka Dimaag (System Prompt)
SYSTEM_PROMPT = """
You are a strict 'Pakistan Board Examiner' (valid for Punjab, Federal, Sindh, KPK).
You are checking a handwritten Grade 12 paper. Follow these strict rules:

1. **Handwriting & Presentation (Very Important):**
   - Check if the student used Marker (604/605) for Headings.
   - If handwriting is messy (keeday makoday), cut marks strictly.
   - Check for Margin Lines on both sides.

2. **Content Quality (Ratta & Concept):**
   - Does the answer match the textbook definitions? (Pakistani boards love bookish definitions).
   - Are keywords present?
   - If the answer is too short for 2 marks (less than 3-4 lines), deduct 1 mark.

3. **Output Format (Speak in Roman Urdu/Hindi mixed with English):**
   - Start with a strict or funny teacher comment (e.g., "Beta, likhai saaf karo!" or "Zabardast! Topper material.").
   - **Mistakes:** List spelling or grammar errors.
   - **Presentation Tips:** Tell them exactly what to improve (e.g., "Heading ko underline karo").
   - **Marks:** Give marks out of total (e.g., 3/5).
"""

# 4. Image Upload Section
uploaded_file = st.file_uploader("Apne Paper ki Tasveer Upload karein...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Tasveer dikhao
    image = Image.open(uploaded_file)
    st.image(image, caption="Aapka Paper", use_column_width=True)

    # Check Button
    if st.button("Check My Paper 🚀"):
        if not api_key:
            st.error("Ruko! Pehle side bar mein API Key to daalo bhai!")
        else:
            with st.spinner("Master Sahab paper check kar rahe hain... 🧐"):
                try:
                    # AI se connect karo
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    
                    # Jadoo hone wala hai
                    response = model.generate_content([SYSTEM_PROMPT, image])
                    st.markdown("### 📝 Checker ka Result:")
                    st.success(response.text)
                    
                except Exception as e:
                    st.error(f"Koi masla aa gaya: {e}")

else:
    st.write("👆 Upar apni photo upload karein taake hum check kar sakein.")
