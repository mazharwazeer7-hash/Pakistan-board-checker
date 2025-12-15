import streamlit as st
import google.generativeai as genai
from PIL import Image
from datetime import datetime, timedelta, timezone

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Exam Cracker AI", page_icon="🎓")

# --- 2. SETTINGS & VIP REGISTER (SMART SYSTEM) ---
# Yahan aap apne customers add karenge.
# Format: "CODE": "EXPIRY-DATE (Saal-Mahina-Din)"
VIP_DB = {
    "VIP786": "2030-01-01",       # Master Key (Hamesha chalegi)
    "AliTrial": "2025-12-16",     # Misaal: Ali ka 2 din ka trial
    "AhmedWk1": "2025-12-21",     # Misaal: Ahmed ka 1 week
    # Jab naya banda aaye, bas yahan ek line aur likh dein
}

FREE_LIMIT = 2

# --- 3. AUTOMATIC KEY LOADER ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    st.error("🚨 API Key Missing! Secrets check karein.")
    st.stop()

# Pakistan Date
pak_time = timezone(timedelta(hours=5))
today_date = datetime.now(pak_time).date()
DAILY_CODE = f"PAKISTAN{today_date.day}"

# --- 4. SESSION STATE ---
if 'count' not in st.session_state:
    st.session_state.count = 0
if 'is_vip' not in st.session_state:
    st.session_state.is_vip = False
if 'vip_expiry' not in st.session_state:
    st.session_state.vip_expiry = None

# --- 5. SIDEBAR ---
with st.sidebar:
    st.title("🎓 Exam Cracker Menu")
    st.write("### 🔐 Access Control")
    
    if st.session_state.is_vip:
        # Check Expiry
        if st.session_state.vip_expiry:
            exp_date = datetime.strptime(st.session_state.vip_expiry, "%Y-%m-%d").date()
            if today_date > exp_date:
                st.session_state.is_vip = False
                st.error("⏳ Subscription Expired! Renew karein.")
                st.rerun()
        
        st.success(f"💎 VIP Active!")
        if st.session_state.vip_expiry:
            st.caption(f"Valid till: {st.session_state.vip_expiry}")
            
        if st.button("Logout"):
            st.session_state.is_vip = False
            st.session_state.vip_expiry = None
            st.rerun()
    else:
        code_input = st.text_input("Enter Daily or VIP Code:", type="password")
        
        if code_input:
            if code_input in VIP_DB:
                expiry_str = VIP_DB[code_input]
                exp_date = datetime.strptime(expiry_str, "%Y-%m-%d").date()
                
                if today_date <= exp_date:
                    st.session_state.is_vip = True
                    st.session_state.vip_expiry = expiry_str
                    st.success(f"💎 Welcome! Valid till {expiry_str}")
                    st.rerun()
                else:
                    st.error(f"❌ Ye Code Expire ho gaya! ({expiry_str})")
            elif code_input == DAILY_CODE:
                st.success(f"🔓 Daily Code Applied! (Limit: {FREE_LIMIT})")
            else:
                st.error("❌ Ghalat Code!")
                st.info(f"Hint: Aaj ka free code hai PAKISTAN{today_date.day}")

    st.markdown("---")
    if not st.session_state.is_vip:
        used = st.session_state.count
        left = FREE_LIMIT - used
        st.write(f"Free Tries Left: **{left}**")
        if left == 0:
            st.error("Quota Khatam!")

# --- 6. MAIN APP ---
st.title("🎓 MAZHAR BHAI KA APP")
st.write("**Punjab Board Special**")

mode = st.radio("Select Mode:", ["📝 Paper Check Karo", "📚 Smart Past Papers (Demo)"])

if mode == "📝 Paper Check Karo":
    can_check = False
    if st.session_state.is_vip:
        can_check = True
    elif st.session_state.count < FREE_LIMIT:
        can_check = True
    
    if not can_check:
        st.warning("⛔ Limit Khatam! Unlimited access ke liye:")
        with st.expander("💎 Get VIP Access (Rs 100/Week)"):
             st.write("1. **Rs 100** EasyPaisa: **0317-4796154**") 
             st.write("2. Screenshot WhatsApp karein.")
             st.markdown("[👉 WhatsApp Me](https://wa.me/923174796154)")
        st.stop()

    SYSTEM_PROMPT = """
    Role: Senior Professor (Punjab Board).
    Task: Check this handwritten Chemistry/Physics paper.
    Output: 1. Shabash, 2. Galtiyan, 3. Ideal Jawab, 4. Marks.
    Tone: Roman Urdu + English.
    """

    uploaded_file = st.file_uploader("Upload Paper", type=["jpg", "png"])
    
    if uploaded_file and st.button("Check My Paper 🚀"):
        with st.spinner("Checking... 🧠"):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-pro")
                response = model.generate_content([SYSTEM_PROMPT, Image.open(uploaded_file)])
                st.success("✅ Report Ready!")
                st.write(response.text)
                if not st.session_state.is_vip:
                    st.session_state.count += 1
            except Exception as e:
                st.error(f"Error: {e}")

elif mode == "📚 Smart Past Papers (Demo)":
    st.subheader("🧪 Chemistry - Chapter 1")
    questions = [{"q": "Define Stoichiometry", "times": 18}, {"q": "Limiting Reactant", "times": 12}]
    for q in questions: st.write(f"- {q['q']} (**{q['times']}** times)")

st.markdown("---")
st.caption("Powered by Exam Cracker AI | Developed by Mazhar")
