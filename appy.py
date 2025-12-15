import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Exam Cracker Pro", page_icon="🎓", layout="centered")

# --- 2. PROFESSIONAL STYLING ---
st.markdown("""
    <style>
    .stButton>button {
        background: linear-gradient(90deg, #d53369 0%, #daae51 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        width: 100%;
        padding: 15px;
    }
    .report-box {
        border: 2px solid #e0e0e0;
        padding: 20px;
        border-radius: 10px;
        background-color: #f9f9f9;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SYSTEM SETUP ---
VIP_DB = {"MZ786": "2030-01-01", "TEST": "2025-12-30"}
FREE_LIMIT = 2

# Session State
if 'count' not in st.session_state: st.session_state.count = 0
if 'user_role' not in st.session_state: st.session_state.user_role = "Free"

# --- 4. SMART API CONNECTION ---
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    else:
        st.error("🚨 API Key Missing! Settings > Secrets mein check karein.")
        st.stop()
except Exception as e:
    st.error(f"Connection Failed: {e}")

# --- 5. SIDEBAR LOGIN ---
with st.sidebar:
    st.header("🔐 Control Panel")
    if st.session_state.user_role == "VIP":
        st.success("💎 VIP Access Active")
        if st.button("Logout"):
            st.session_state.user_role = "Free"
            st.rerun()
    else:
        code = st.text_input("Enter VIP Code", type="password")
        if code in VIP_DB:
            st.session_state.user_role = "VIP"
            st.rerun()
        
        st.divider()
        left = FREE_LIMIT - st.session_state.count
        st.write(f"Free Tries: {left}/{FREE_LIMIT}")
        st.progress(left/FREE_LIMIT)

# --- 6. MAIN APP ---
st.title("🎓 Exam Cracker AI")
st.write("**Punjab Board Paper Checker (Auto-Fix Edition)**")

uploaded_file = st.file_uploader("Upload Paper (JPG/PNG)", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Your Paper", use_container_width=True)
    
    # Check Permission
    allowed = False
    if st.session_state.user_role == "VIP": allowed = True
    elif st.session_state.count < FREE_LIMIT: allowed = True
    
    if allowed:
        if st.button("🚀 CHECK MY PAPER"):
            with st.spinner("🧠 AI System finding the best model..."):
                try:
                    # PROMPT
                    prompt = """
                    You are a strict Punjab Board Professor.
                    Check this paper. Mark mistakes. Give marks.
                    Reply in Roman Urdu.
                    """
                    
                    # --- AUTO-DETECT MODEL LOGIC (The Magic) ---
                    active_model = None
                    
                    # List of models to try (Priority wise)
                    candidates = ["gemini-1.5-flash", "gemini-1.5-flash-latest", "gemini-pro", "gemini-1.5-pro"]
                    
                    # 1. Pehle Direct Try karein
                    for model_name in candidates:
                        try:
                            model = genai.GenerativeModel(model_name)
                            response = model.generate_content([prompt, image])
                            active_model = model_name # Agar chal gaya to naam save kar lo
                            st.markdown(f"<small>Connected to: {active_model} ✅</small>", unsafe_allow_html=True)
                            
                            # Result Show
                            st.markdown(f'<div class="report-box">{response.text}</div>', unsafe_allow_html=True)
                            
                            # Count update
                            if st.session_state.user_role == "Free":
                                st.session_state.count += 1
                            break # Loop tod do, kaam ho gaya
                            
                        except Exception as e:
                            continue # Agla model try karo
                    
                    # 2. Agar koi bhi na chala, to List maango
                    if not active_model:
                        st.warning("⚠️ Standard models failed. Searching available models...")
                        found_any = False
                        for m in genai.list_models():
                            if 'generateContent' in m.supported_generation_methods:
                                try:
                                    # Jo pehla model mile usay chala do
                                    model = genai.GenerativeModel(m.name)
                                    response = model.generate_content([prompt, image])
                                    st.success(f"✅ Auto-Fixed! Used: {m.name}")
                                    st.markdown(response.text)
                                    found_any = True
                                    break
                                except:
                                    continue
                        
                        if not found_any:
                            st.error("❌ Critical Error: Google ne apki API Key par koi Model allow nahi kiya.")
                            st.info("Solution: Nayi Gmail ID se API Key banayen.")

                except Exception as final_error:
                    st.error(f"System Error: {final_error}")

    else:
        st.error("⛔ Limit Reached. Enter Code.")

st.markdown("---")
st.caption("Auto-Healing AI System v2.0")
