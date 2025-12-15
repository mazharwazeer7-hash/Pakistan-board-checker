import streamlit as st
import google.generativeai as genai
from PIL import Image
from datetime import datetime, timedelta, timezone

# --- 1. PROFESSIONAL PAGE SETUP ---
st.set_page_config(
    page_title="Exam Cracker Pro",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- 2. CUSTOM STYLING (CSS) ---
# Ye code app ko sunder banayega
st.markdown("""
    <style>
    .stButton>button {
        background-color: #FF4B4B;
        color: white;
        border-radius: 10px;
        height: 3em;
        width: 100%;
        font-weight: bold;
    }
    .main-header {
        font-size: 2.5rem;
        color: #333;
        text-align: center;
        font-weight: 700;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SYSTEM CONFIGURATION ---
# VIP Database (Aapka Register)
VIP_DB = {
    "VIP786": "2030-01-01",      # Master Code
    "AliTrial": "2025-12-20",    # Example
}
FREE_LIMIT = 2

# Time Setup
pak_time = timezone(timedelta(hours=5))
today_date = datetime.now(pak_time).date()
DAILY_CODE = f"PAKISTAN{today_date.day}"

# --- 4. API & MODEL SETUP ---
try:
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
    else:
        st.error("🚨 System Error: API Key Missing.")
        st.stop()
except Exception as e:
    st.error(f"Connection Error: {e}")

# --- 5. SESSION STATE (Memory) ---
if 'count' not in st.session_state: st.session_state.count = 0
if 'is_vip' not in st.session_state: st.session_state.is_vip = False
if 'user_name' not in st.session_state: st.session_state.user_name = "Guest"

# --- 6. SIDEBAR (Login System) ---
with st.sidebar:
    st.title("🔐 Login Panel")
    
    if st.session_state.is_vip:
        st.success(f"👤 Welcome, {st.session_state.user_name}!")
        st.info("💎 Premium Access Active")
        if st.button("Logout"):
            st.session_state.is_vip = False
            st.rerun()
    else:
        st.write("Enter Access Code:")
        code_input = st.text_input("Code", type="password", label_visibility="collapsed")
        
        if st.button("Login"):
            if code_input in VIP_DB:
                exp_date = datetime.strptime(VIP_DB[code_input], "%Y-%m-%d").date()
                if today_date <= exp_date:
                    st.session_state.is_vip = True
                    st.session_state.user_name = code_input
                    st.toast("Login Successful!", icon="✅")
                    st.rerun()
                else:
                    st.error("❌ Code Expired!")
            elif code_input == DAILY_CODE:
                st.toast(f"Daily Code Active! ({FREE_LIMIT} Tries)", icon="🔓")
            elif code_input:
                st.error("❌ Invalid Code")

    st.divider()
    if not st.session_state.is_vip:
        left = FREE_LIMIT - st.session_state.count
        st.metric("Free Tries Left", left)

# --- 7. MAIN INTERFACE ---
st.markdown('<div class="main-header">🎓 Exam Cracker AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Punjab Board Professional Checker</div>', unsafe_allow_html=True)

# TABS LAYOUT (Professional Look)
tab1, tab2 = st.tabs(["📝 Paper Checker", "📚 Smart Prep (Beta)"])

with tab1:
    st.write("### 📤 Upload Answer Sheet")
    st.caption("Supports: JPG, PNG (Max 200MB)")
    
    uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"], label_visibility="collapsed")

    # Limit Check
    allowed = False
    if st.session_state.is_vip: allowed = True
    elif st.session_state.count < FREE_LIMIT: allowed = True

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Paper", use_container_width=True)
        
        if allowed:
            if st.button("🔍 Analyze Paper Now"):
                with st.spinner("🤖 AI Professor checking... (Please wait)"):
                    try:
                        # ULTRA PROMPT
                        prompt = """
                        Act as a Strict Senior Professor of Punjab Board Pakistan (Class 12).
                        Analyze this handwritten paper image carefully.
                        
                        Provide output in this format:
                        1. **Marks:** [Obtained]/[Total]
                        2. **Mistakes:** (List specific mistakes in bullet points)
                        3. **Correction:** (Explain the right answer simply)
                        4. **Remarks:** (Encouraging feedback in Roman Urdu)
                        """
                        
                        # MODEL CALL
                        model = genai.GenerativeModel("gemini-1.5-flash")
                        response = model.generate_content([prompt, image])
                        
                        st.success("✅ Assessment Complete!")
                        st.markdown(response.text)
                        
                        # Counter Update
                        if not st.session_state.is_vip:
                            st.session_state.count += 1
                            
                    except Exception as e:
                        st.error("⚠️ Network Error. Please try again.")
                        # Secret error for you (Developer)
                        st.caption(f"Dev Error: {e}")
        else:
            st.warning("⛔ Free Limit Reached. Please enter a VIP Code.")

with tab2:
    st.info("🚧 Coming Soon: Smart Past Papers & Guess Papers")
    st.image("https://img.freepik.com/free-vector/exams-concept-illustration_114360-2754.jpg", width=300)

# Footer
st.markdown("---")
st.caption("© 2025 Exam Cracker AI | Professional Edition")
