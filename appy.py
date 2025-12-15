import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="NEXA AI - Pakistan",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. NEXA BRANDING & CSS (Ultra Modern) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #1f1f1f;
        background-color: #ffffff;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #ffffff; }

    /* NEXA TITLE STYLE */
    .brand-tag {
        font-size: 1rem;
        font-weight: 600;
        color: #4285F4;
        text-align: center;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-top: 30px;
    }
    .main-greeting {
        font-size: 3.8rem;
        font-weight: 800;
        background: -webkit-linear-gradient(90deg, #0b0c10, #1f2833);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
        text-align: center;
        letter-spacing: -2px;
    }
    .sub-greeting {
        font-size: 1.2rem;
        color: #66fcf1; /* Neon Cyan for Future Vibe */
        background-color: #0b0c10;
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        margin-bottom: 30px;
    }
    .center-text { text-align: center; }

    /* CHAT INPUT */
    .stChatInputContainer {
        border-radius: 15px;
        border: 1px solid #e0e0e0;
        background: #f0f4f9;
        padding: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    
    /* SADAPAY PAYMENT BOX */
    .payment-box {
        background: linear-gradient(135deg, #ffffff 0%, #f0fdfc 100%);
        border: 2px solid #00d1c1; /* SadaPay Teal */
        color: #333;
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        margin-top: 20px;
        box-shadow: 0 10px 30px rgba(0, 209, 193, 0.15);
        animation: popUp 0.5s ease;
    }
    @keyframes popUp {
        0% { transform: scale(0.9); opacity: 0; }
        100% { transform: scale(1); opacity: 1; }
    }
    .sada-title { color: #00d1c1; font-weight: 900; font-size: 1.8rem; }
    .account-number {
        font-size: 2rem; font-weight: 800;
        background: #e0fbf9; color: #00796b;
        padding: 15px; border-radius: 12px;
        margin: 15px 0; letter-spacing: 3px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BUSINESS SETTINGS ---
VIP_CODE = "student100"  # Secret Code
FREE_LIMIT = 3           # Free Tries
SADAPAY_NUMBER = "0317-4796154" 
ACCOUNT_TITLE = "Mazhar Wazeer"

# Smart Memory (URL Hack)
query_params = st.query_params
url_count = query_params.get("used", "0")

if 'count' not in st.session_state: st.session_state.count = int(url_count)
if 'user_role' not in st.session_state: st.session_state.user_role = "Free"
if 'messages' not in st.session_state: st.session_state.messages = []

# --- 4. API CONNECTION ---
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    else:
        st.error("🚨 System Error: API Key Missing.")
        st.stop()
except:
    st.error("Connection Error.")

# --- 5. NEXA BRAIN (The Logic) ---
def get_nexa_response(prompt_text, image=None):
    
    SYSTEM_INSTRUCTION = """
    ROLE: You are 'NEXA', a Super-Intelligent AI Mentor for Pakistani Students.
    
    YOUR POWER:
    1. **Auto-Detect:** Identify subject from image (Physics, Urdu, etc.) and apply Punjab Board Rules.
       - Short Qs: 2 Marks fixed.
       - Long Qs: Check Headings & Diagrams.
    2. **Exam Advisor (2025):** - Chem 12th: Pairings (Ch 1+2, 5+15).
       - Bio 12th: Pairings (Ch 15+21, 16+25).
    3. **Future Guide:** Advice on Career, Freelancing, and Life.
    
    TONE: Friendly, Futuristic, Roman Urdu.
    Start response with: "⚡ **NEXA Analysis:**"
    """
    
    final_prompt = f"{SYSTEM_INSTRUCTION}\n\nUSER: {prompt_text}"

    # Priority: 2.5 Flash
    models_to_try = ["gemini-2.5-flash", "gemini-1.5-flash-latest", "gemini-pro"]
    
    for m in models_to_try:
        try:
            model = genai.GenerativeModel(m)
            if image:
                response = model.generate_content([final_prompt, image])
            else:
                response = model.generate_content(final_prompt)
            return response.text
        except:
            continue
    return "⚠️ NEXA Server Busy. Try again."

# --- 6. SIDEBAR (Hidden Admin Panel) ---
with st.sidebar:
    st.header("⚙️ NEXA Settings")
    if st.session_state.user_role == "VIP":
        st.success("🌟 Premium Unlocked")
        if st.button("Logout"):
            st.session_state.user_role = "Free"
            st.rerun()
    else:
        st.info("👤 Guest Mode")
        code_in = st.text_input("Enter VIP Code", type="password")
        if code_in == VIP_CODE:
            st.session_state.user_role = "VIP"
            st.balloons()
            st.rerun()
        
        left = FREE_LIMIT - st.session_state.count
        if left < 0: left = 0
        st.caption(f"Free Tries: {left}/{FREE_LIMIT}")
        st.progress(left/FREE_LIMIT)
        st.divider()
        st.markdown(f"**Owner:** {ACCOUNT_TITLE}")

# --- 7. MAIN INTERFACE ---

# === WELCOME SCREEN ===
if not st.session_state.messages:
    # Branding
    st.markdown('<div class="brand-tag">POWERED BY NEXA AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-greeting">Hello, Friend.</div>', unsafe_allow_html=True)
    
    # Center Subtitle
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown('<div class="center-text">Main tumhara <b>Future Guide</b> hun.<br>Paper check karo ya Career set karo.</div>', unsafe_allow_html=True)

    st.write("")
    st.write("### 👇 Upload Paper / Ask Anything")
    uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"], label_visibility="collapsed")

    if uploaded_file:
        # CHECK LIMIT
        is_allowed = (st.session_state.user_role == "VIP") or (st.session_state.count < FREE_LIMIT)
        
        if is_allowed:
            img = Image.open(uploaded_file)
            st.session_state.messages.append({"role": "user", "content": "Check my paper", "image": img})
            
            if st.session_state.user_role == "Free":
                st.session_state.count += 1
                st.query_params["used"] = str(st.session_state.count)
            
            st.rerun()
        else:
            # === SADAPAY PAYWALL ===
            st.error("⛔ Free Trials Ended!")
            st.markdown(f"""
            <div class="payment-box">
                <h3 class="sada-title">SadaPay</h3>
                <p>Unlock <b>Unlimited Access</b> for just Rs. 100</p>
                <div class="account-number">{SADAPAY_NUMBER}</div>
                <p><b>Title:</b> {ACCOUNT_TITLE}</p>
                <hr>
                <p>📷 Send Screenshot on <b>WhatsApp</b> to get VIP Code.</p>
                <p><i>Future is waiting!</i> 🚀</p>
            </div>
            """, unsafe_allow_html=True)

# === CHAT SCREEN ===
else:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            if "image" in msg:
                st.image(msg["image"], width=300)
            st.markdown(msg["content"])

    if st.session_state.messages[-1]["role"] == "user":
        last_msg = st.session_state.messages[-1]
        with st.chat_message("assistant"):
            with st.spinner("NEXA Thinking... ⚡"):
                if "image" in last_msg:
                    response = get_nexa_response("Check this paper", last_msg["image"])
                else:
                    response = get_nexa_response(last_msg["content"])
                st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# === INPUT ===
if prompt := st.chat_input("Ask NEXA (Exam, Career, Life)..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()
