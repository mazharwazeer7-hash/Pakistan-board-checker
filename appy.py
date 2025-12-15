import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# --- 1. SUPER CONFIGURATION (Sabse Pehle) ---
st.set_page_config(
    page_title="Exam Cracker Pro",
    page_icon="🎓",
    layout="wide",  # Wide mode for professional dashboard look
    initial_sidebar_state="expanded"
)

# --- 2. PROFESSIONAL CSS (Design & Styling) ---
# Ye code app ko "Website" jaisa banayega
st.markdown("""
    <style>
    /* Main Background Cleaner */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Login & Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e0e0e0;
    }
    
    /* Button Styling - Gradient Red */
    div.stButton > button {
        background: linear-gradient(45deg, #d32f2f, #ff1744);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: bold;
        width: 100%;
        transition: 0.3s;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0,0,0,0.2);
    }

    /* Success Message Box */
    .vip-badge {
        background-color: #e8f5e9;
        color: #2e7d32;
        padding: 10px;
        border-radius: 6px;
        border: 1px solid #c8e6c9;
        text-align: center;
        font-weight: bold;
        margin-bottom: 15px;
    }
    
    /* Header Styling */
    h1 {
        color: #1a237e;
        font-family: 'Helvetica', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SYSTEM LOGIC & DATABASE ---
VIP_DB = {
    "MZ786": "Admin Access",  # Aapka Code
    "TRIAL2025": "Student Access"
}
FREE_LIMIT = 2

# Session State Initialization (Memory)
if 'count' not in st.session_state: st.session_state.count = 0
if 'user_role' not in st.session_state: st.session_state.user_role = "Free"

# --- 4. API CONNECTION (Safe Mode) ---
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    else:
        st.error("⚠️ SYSTEM ALERT: API Key is missing.")
        st.stop()
except Exception as e:
    st.error("⚠️ Connection Failed.")

# --- 5. SIDEBAR (SMART LOGIN) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2997/2997312.png", width=80)
    st.title("Control Panel")
    
    # Status Indicator
    if st.session_state.user_role == "VIP":
        st.markdown('<div class="vip-badge">💎 VIP USER ACTIVE</div>', unsafe_allow_html=True)
        if st.button("Logout"):
            st.session_state.user_role = "Free"
            st.rerun()
    else:
        st.info("👤 Guest Mode Active")
        with st.expander("🔐 VIP Login", expanded=True):
            code_input = st.text_input("Enter Access Code:", type="password")
            if code_input:
                if code_input in VIP_DB:
                    st.session_state.user_role = "VIP"
                    st.toast("Access Granted! Welcome.", icon="🎉")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Invalid Code")

    st.divider()
    # Free Limit Meter
    if st.session_state.user_role == "Free":
        used = st.session_state.count
        left = FREE_LIMIT - used
        st.write(f"**Free Tries:** {left}/{FREE_LIMIT}")
        st.progress(left/FREE_LIMIT)
    else:
        st.write("**Plan:** Unlimited Enterprise")

# --- 6. MAIN DASHBOARD ---
st.title("🎓 Exam Cracker AI")
st.markdown("### Professional Board Paper Checker (Punjab Board)")
st.markdown("---")

# Main Interface
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("#### 📤 Upload Paper")
    uploaded_file = st.file_uploader("Select Image (JPG/PNG)", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Document", use_container_width=True, channels="RGB")

with col2:
    st.markdown("#### 🤖 AI Analysis Report")
    
    if uploaded_file:
        # Permission Check
        has_access = False
        if st.session_state.user_role == "VIP":
            has_access = True
        elif st.session_state.count < FREE_LIMIT:
            has_access = True
        
        if has_access:
            if st.button("🚀 CHECK MY PAPER NOW", use_container_width=True):
                
                # Progress Bar Animation
                progress_text = "Scanning handwriting..."
                my_bar = st.progress(0, text=progress_text)
                
                for percent_complete in range(100):
                    time.sleep(0.01)
                    my_bar.progress(percent_complete + 1, text="Analyzing mistakes...")
                
                my_bar.empty() # Remove bar
                
                # --- THE HYBRID ENGINE (NO 404 LOGIC) ---
                try:
                    prompt = """
                    You are a strict Senior Professor for Punjab Board (Class 12).
                    Analyze this handwritten paper image deeply.
                    
                    Output Structure:
                    1. **OBTAINED MARKS:** [Marks]/[Total]
                    2. **MAJOR MISTAKES:** (Bulleted list)
                    3. **CORRECT ANSWER:** (Explain the concept)
                    4. **TEACHER'S REMARKS:** (Encouraging tone in Roman Urdu)
                    
                    Keep the tone professional yet easy to understand.
                    """
                    
                    # 1. Try Fast Model (Flash)
                    try:
                        model = genai.GenerativeModel("gemini-1.5-flash")
                        response = model.generate_content([prompt, image])
                    except:
                        # 2. If Failed, Auto-Switch to Backup (Pro)
                        # User ko pata bhi nahi chalega
                        model = genai.GenerativeModel("gemini-pro")
                        response = model.generate_content([prompt, image])
                    
                    # Success Display
                    st.success("✅ Assessment Complete!")
                    
                    # Result ko khoobsurat box mein dikhana
                    with st.container(border=True):
                        st.markdown(response.text)
                    
                    # Limit Deduct
                    if st.session_state.user_role == "Free":
                        st.session_state.count += 1
                        
                except Exception as e:
                    st.error("System Busy. Please try again with a clearer image.")
                    st.caption(f"Error Code: {e}") # Sirf aapke liye
        else:
            st.warning("⛔ Free Limit Reached!")
            st.error("Please enter a VIP Code in the sidebar to continue.")
    else:
        st.info("👈 Please upload a paper image from the left side to begin.")

# --- 7. FOOTER ---
st.markdown("---")
st.caption("© 2025 Exam Cracker System | Developed by Mazhar")
