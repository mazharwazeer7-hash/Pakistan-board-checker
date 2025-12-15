import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Pakistan Board Checker",
    page_icon="🇵🇰",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. ULTRA PREMIUM CSS (Glassmorphism & Animations) ---
st.markdown("""
    <style>
    /* Global Settings */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* Main Title Animation */
    .main-title {
        text-align: center;
        font-size: 3.2em;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #11998e, #38ef7d);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 10px;
        animation: fadeIn 2s ease-in-out;
    }
    
    .welcome-text {
        text-align: center;
        color: #555;
        font-size: 1.3em;
        margin-bottom: 30px;
        font-weight: 300;
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.7);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.18);
        padding: 20px;
        margin-bottom: 20px;
    }

    /* Floating Chat Bar */
    .stChatInputContainer {
        border-radius: 25px;
        box-shadow: 0 -5px 15px rgba(0,0,0,0.05);
        background: white;
        padding-bottom: 10px;
    }

    /* Message Bubbles */
    .stChatMessage {
        border-radius: 18px;
        animation: slideIn 0.5s ease;
    }

    /* Animations */
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(-20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    @keyframes slideIn {
        0% { opacity: 0; transform: translateX(-10px); }
        100% { opacity: 1; transform: translateX(0); }
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SETTINGS & LIMITS ---
VIP_CODE = "student100"  # Aapka Code
FREE_LIMIT = 3           # 3 Tries Limit

if 'count' not in st.session_state: st.session_state.count = 0
if 'user_role' not in st.session_state: st.session_state.user_role = "Free"
if 'messages' not in st.session_state: st.session_state.messages = []
if 'selected_subject' not in st.session_state: st.session_state.selected_subject = "General"

# --- 4. API CONNECTION ---
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    else:
        st.error("🚨 API Key Missing.")
        st.stop()
except:
    st.error("Connection Error.")

# --- 5. LOGIC: PUNJAB BOARD RULES + MODEL 2.5 ---
def get_board_response(prompt_text, image=None, subject="General"):
    
    board_rules = f"""
    ROLE: Strict Examiner for Pakistan/Punjab Board. Subject: {subject}.
    
    MARKING SCHEME (Strict):
    1. **SHORT QUESTIONS (2 Marks Each):**
       - Definition Only = 1 Mark.
       - Definition + Example/Diagram = 2 Marks.
    
    2. **LONG QUESTIONS:**
       - Matric (9th/10th): Check for Part A (5) & Part B (4).
       - Inter (11th/12th): Check for detailed Theory (4 Marks).
       - No Headings = Deduct Marks.
    
    OUTPUT FORMAT (Roman Urdu):
    - Marks: [Obtained]/[Total]
    - Mistakes: (Bullet points)
    - Tips: (Improvement advice)
    """
    
    final_prompt = f"{board_rules}\nUser Request: {prompt_text}"

    # --- ULTRA MODEL PRIORITY LIST ---
    # Sabse pehle 2.5 Flash try karega (Jaise aapne kaha)
    models_to_try = [
        "gemini-2.5-flash",       # Top Priority 🚀
        "gemini-1.5-flash-latest",
        "gemini-1.5-flash", 
        "gemini-pro"
    ]
    
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
            
    return "⚠️ Server Busy. Thodi der baad try karein."

# --- 6. SIDEBAR (Login Panel) ---
with st.sidebar:
    st.header("🔐 Access Control")
    if st.session_state.user_role == "VIP":
        st.success("✅ VIP Student Verified")
        if st.button("Logout"):
            st.session_state.user_role = "Free"
            st.rerun()
    else:
        st.info("👤 Free Guest Mode")
        code_in = st.text_input("Enter Code", type="password", placeholder="student100")
        if code_in == VIP_CODE:
            st.session_state.user_role = "VIP"
            st.rerun()
        
        # Limit Progress Bar
        left = FREE_LIMIT - st.session_state.count
        if left < 0: left = 0
        st.caption(f"Free Tries Left: {left}/{FREE_LIMIT}")
        st.progress(left/FREE_LIMIT)

# --- 7. MAIN INTERFACE ---

# === WELCOME SCREEN ===
if not st.session_state.messages:
    st.markdown('<div class="main-title">Pakistan Board Checker</div>', unsafe_allow_html=True)
    st.markdown('<div class="welcome-text">AI Powered • Free • Fast</div>', unsafe_allow_html=True)

    # Glassmorphism Box for Input
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    # Subject Select
    st.write("##### 📘 Step 1: Subject Select Karein")
    subj = st.selectbox("", ["Physics", "Chemistry", "Biology", "English", "Computer", "Urdu", "Islamiat"], label_visibility="collapsed")
    st.session_state.selected_subject = subj
    
    st.write("---")
    
    # Upload
    st.write("##### 📤 Step 2: Paper Upload Karein")
    uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"], label_visibility="collapsed")
    
    st.markdown('</div>', unsafe_allow_html=True) # End Glass Card

    if uploaded_file:
        # Check Limit
        is_allowed = (st.session_state.user_role == "VIP") or (st.session_state.count < FREE_LIMIT)
        
        if is_allowed:
            img = Image.open(uploaded_file)
            # Add to Chat
            st.session_state.messages.append({"role": "user", "content": f"Check my {subj} paper", "image": img})
            
            # Count Update
            if st.session_state.user_role == "Free":
                st.session_state.count += 1
            st.rerun()
        else:
            st.error(f"⛔ Free Limit Khatam! Unlimited access ke liye code lagayen: {VIP_CODE}")

# === CHAT SCREEN ===
else:
    # Show History
    for msg in st.session_state.messages:
        role_icon = "🧑‍🎓" if msg["role"] == "user" else "🤖"
        with st.chat_message(msg["role"], avatar=role_icon):
            if "image" in msg:
                st.image(msg["image"], width=300)
            st.markdown(msg["content"])

    # Handle New AI Response
    if st.session_state.messages[-1]["role"] == "user":
        last_msg = st.session_state.messages[-1]
        
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Checking Paper (Using Gemini 2.5)... ⚡"):
                if "image" in last_msg:
                    response = get_board_response("Check this paper.", last_msg["image"], st.session_state.selected_subject)
                else:
                    response = get_board_response(last_msg["content"], subject=st.session_state.selected_subject)
                
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})

# === CHAT INPUT ===
if prompt := st.chat_input("Sawal poochein..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()
