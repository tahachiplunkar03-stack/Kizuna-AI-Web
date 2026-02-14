import streamlit as st
from groq import Groq

# --- MOBILE MASTER CONFIG ---
st.set_page_config(page_title="KIZUNA AI WEB", page_icon="🔱", layout="wide")

# --- CUSTOM CSS FOR TOP MENU ---
st.markdown("""
    <style>
    .stApp { background-color: #0e0e0e; color: white; }
    
    /* Hide the broken sidebar completely */
    [data-testid="stSidebar"] { display: none !important; }
    button[kind="headerNoSpacing"] { display: none !important; }

    /* Top Navigation Bar */
    .top-bar {
        background-color: #131314;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 20px;
        border-bottom: 2px solid #FFD700;
        text-align: center;
    }
    
    .stChatMessage { background-color: #1e1f20 !important; border-radius: 15px !important; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# API Setup
client = Groq(api_key="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")
if "all_sessions" not in st.session_state: st.session_state.all_sessions = []
if "messages" not in st.session_state: st.session_state.messages = []

# --- TOP NAVIGATION MENU ---
st.markdown("<div class='top-bar'><h2 style='color: #FFD700; margin:0;'>🔱 KIZUNA AI</h2></div>", unsafe_allow_html=True)

# Menu Buttons in a Row
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("➕ New"):
        st.session_state.messages = []
        st.rerun()
with col2:
    # History Dropdown (Ab click ka jhanjhat hi khatam)
    options = ["Select History"] + [s['title'] for s in st.session_state.all_sessions]
    selection = st.selectbox("", options, label_visibility="collapsed")
    if selection != "Select History":
        for s in st.session_state.all_sessions:
            if s['title'] == selection:
                st.session_state.messages = s['chats']
                st.rerun()
with col3:
    if st.button("🗑️ Clear"):
        st.session_state.all_sessions = []
        st.rerun()

st.write("---")

# --- MAIN CHAT ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Bolo Bhai..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                messages=[{"role": "system", "content": "You are Kizuna AI. Direct answers."}] + 
                         [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-6:]],
                model="llama-3.3-70b-versatile"
            )
            reply = response.choices[0].message.content
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            
            title = prompt[:20] + "..."
            if not any(s['title'] == title for s in st.session_state.all_sessions):
                st.session_state.all_sessions.insert(0, {"title": title, "chats": st.session_state.messages.copy()})
        except Exception as e:
            st.error(f"Error: {e}")
