import streamlit as st
from groq import Groq

# --- MASTER CONFIG ---
st.set_page_config(page_title="KIZUNA AI WEB", page_icon="🔱", layout="wide")

# Custom CSS for Gold Theme
st.markdown("""
    <style>
    .stApp { background-color: #0e0e0e; color: white; }
    [data-testid="stSidebar"] { display: none !important; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
    
    /* Gold Buttons */
    div.stButton > button {
        background-color: #FFD700 !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 10px !important;
    }
    
    /* Chat bubbles */
    .stChatMessage { background-color: #1e1f20 !important; border-radius: 15px !important; }
    </style>
    """, unsafe_allow_html=True)

# API Initialization
client = Groq(api_key="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")

# --- SMART MEMORY ---
if "all_sessions" not in st.session_state: st.session_state.all_sessions = {}
if "messages" not in st.session_state: st.session_state.messages = []
if "current_session_id" not in st.session_state: st.session_state.current_session_id = None

# --- TOP NAVIGATION ---
st.markdown("<h2 style='text-align: center; color: #FFD700;'>🔱 KIZUNA AI</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.button("➕ New Chat"):
        st.session_state.messages = []
        st.session_state.current_session_id = None
        st.rerun()

with col2:
    # History Selectbox
    options = ["Current Chat"] + list(st.session_state.all_sessions.keys())
    selection = st.selectbox("", options, label_visibility="collapsed")
    if selection != "Current Chat" and selection != st.session_state.current_session_id:
        st.session_state.messages = st.session_state.all_sessions[selection]
        st.session_state.current_session_id = selection
        st.rerun()

with col3:
    if st.button("🗑️ Clear All"):
        st.session_state.all_sessions = {}
        st.session_state.messages = []
        st.session_state.current_session_id = None
        st.rerun()

st.write("---")

# --- CHAT AREA ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input Logic
if prompt := st.chat_input("Bolo Bhai..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Setting a stable session ID if none exists
    if not st.session_state.current_session_id:
        st.session_state.current_session_id = prompt[:25] + "..."

    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-10:]],
                model="llama-3.3-70b-versatile"
            )
            reply = response.choices[0].message.content
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            
            # Save or Update the session in the dictionary
            st.session_state.all_sessions[st.session_state.current_session_id] = st.session_state.messages.copy()
        except Exception as e:
            st.error(f"Error: {e}")
