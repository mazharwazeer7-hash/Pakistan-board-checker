import streamlit as st
import google.generativeai as genai
from PIL import Image
from datetime import datetime, timedelta, timezone

# --- 1. PAGE SETUP (Naam: Exam Cracker) ---
st.set_page_config(page_title="Exam Cracker AI", page_icon="🎓")

# --- 2. SETTINGS & SECRETS ---
VIP_PASSCODE = "VIP786"   # Paid bachon ke liye
FREE_LIMIT = 2            # Free walon ke liye daily limit

# --- 3. AUTOMATIC KEY LOADER (JADOO) ---
# Ye line ab user se nahi mangegi, seedha Streamlit Secrets se uthayegi
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    st.error("🚨 Owner ne API Key set nahi ki! (Settings > Secrets mein dalein)")
    st.stop()

# Pakistan Date ke hisaab se Daily Code (Auto)
pak_time = timezone(timedelta(hours=5))
today_date = datetime.now(pak_time).day
DAILY_CODE = f"PAKISTAN{today_date}" # e.g., PAKISTAN14

# --- 4. SESSION STATE (Memory) ---
if 'count' not in st.session_state:
    st.session_state.count = 0
if 'is_vip' not in st.session_state:
    st.session_state.is_vip = False

# --- 5. SIDEBAR (The Guard & Menu) ---
with st.sidebar:
    st.title("🎓 Exam Cracker Menu")
    
    # --- LOCK SYSTEM ---
    st.write("### 🔐 Access Control")
    
    # Agar VIP pehle se hai to dikhao
    if st.session_state.is_vip:
        st.success(f"💎 VIP Mode Active! (Unlimited)")
        if st.button("Logout"):
            st.session_state.is_vip = False
            st.rerun()
    else:
        # Code Input Box
        code_input = st.text_input("Enter Daily or VIP Code:", type="password")
        
        if code_input == VIP_PASSCODE:
            st.session_state.is_vip = True
            st.success("💎 VIP Unlocked!")
            st.rerun()
        elif code_input == DAILY_CODE:
            st.success(f"🔓 Daily Code Applied! (Limit: {FREE_LIMIT})")
        elif code_input:
            st.error("❌ Ghalat Code!")
            st.info(f"Hint: Aaj ka free code hai 'PAKISTAN' + {today_date}")

    st.markdown("---")
    
    # --- QUOTA DISPLAY ---
    if not st.session_state.is_vip:
        used = st.session_state.count
        left = FREE_LIMIT - used
        st.write(f"Free Tries Left: **{left}**")
        if left == 0:
            st.error("Quota Khatam! Kal aana ya VIP lo.")
            
    # NOTE: Ab yahan se API Key ka box hata diya gaya hai.

# --- 6. MAIN PAGE ---
st.title("🎓 Exam Cracker AI")
st.write("**Punjab Board Special: Checker + Guess Paper**")

# Mode Selection (Checker ya Past Paper)
mode = st.radio("Kya karna chahte ho?", ["📝 Paper Check Karo", "📚 Smart Past Papers (Demo)"])

# ==========================================
# MODE 1: PAPER CHECKER (English Only)
# ==========================================
if mode == "📝 Paper Check Karo":
    
    # --- Quota Check ---
    can_check = False
    if st.session_state.is_vip:
        can_check = True
    elif st.session_state.count < FREE_LIMIT:
        can_check = True
    
    if not can_check:
        st.warning("⛔ Limit Khatam! Unlimited access ke liye niche dekhein.")
        with st.expander("💎 Get VIP Access (Rs 100/Week)"):
             st.write("1. **Rs 100** EasyPaisa: **0317-4796154**") 
             st.write("2. Screenshot WhatsApp karein.")
             st.markdown("[👉 Click to WhatsApp Me](https://wa.me/923174796154)")
        st.stop()

    # --- System Prompt (Best Version) ---
    SYSTEM_PROMPT = """
    Role: Senior Professor (Punjab Board).
    Task: Check this handwritten Chemistry/Physics paper.
    
    Output Format:
    1. **🌟 Shabash (Good Points):** Praise presentation (605 Marker).
    2. **⚠️ Galtiyan (Mistakes):** Point out missing keywords.
    3. **💡 Ideal Jawab (Topper's Answer):** Rewrite the definition exactly as per the book for the student to memorize.
    4. **🔢 Marks:** Give marks out of total.
    
    Tone: Strictly Academic but Motivating. Use Roman Urdu + English.
    Note: If the handwriting is Urdu/Nastaliq, apologize and say "Main abhi sirf English Medium check kar sakta hun."
    """

    uploaded_file = st.file_uploader("Sirf English Medium Papers (Chem/Phy/Bio)", type=["jpg", "png"])
    
    if uploaded_file and st.button("Check My Paper 🚀"):
        # Ab hum 'api_key' variable use karenge jo secrets se aaya hai
        if not api_key:
             st.error("System Error: API Key missing.")
        else:
            with st.spinner("Exam Cracker dimagh laga raha hai... 🧠"):
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    response = model.generate_content([SYSTEM_PROMPT, Image.open(uploaded_file)])
                    
                    st.success("✅ Analysis Complete!")
                    st.write(response.text)
                    
                    # Count katna (Agar free user hai)
                    if not st.session_state.is_vip:
                        st.session_state.count += 1
                except Exception as e:
                    st.error(f"Error: {e}")

# ==========================================
# MODE 2: SMART PAST PAPERS (Demo Data)
# ==========================================
elif mode == "📚 Smart Past Papers (Demo)":
    st.subheader("🧪 Chemistry - Chapter 1 (Free Demo)")
    st.info("Puri book ka data VIP members ke liye jald a raha hai!")
    
    # Hardcoded Data (Aaj raat ke liye kaafi hai)
    questions = [
        {"q": "Define Stoichiometry & Assumptions", "times": 18},
        {"q": "Difference between Ion and Molecular Ion", "times": 15},
        {"q": "Limiting Reactant definition", "times": 12},
        {"q": "Yield (Actual vs Theoretical)", "times": 10},
        {"q": "Avogadro's Number short note", "times": 8},
        {"q": "Mole definition", "times": 6}
    ]
    
    col1, col2 = st.columns(2)
    with col1:
        st.error("🔥 Most Repeated (Diamond)")
        for q in questions:
            if q['times'] >= 15:
                st.write(f"- {q['q']} (**{q['times']}** times)")
    
    with col2:
        st.warning("🥇 Important (Gold)")
        for q in questions:
            if 10 <= q['times'] < 15:
                st.write(f"- {q['q']} (**{q['times']}** times)")

st.markdown("---")
st.caption("Powered by Exam Cracker AI | Developed by Mazhar")
