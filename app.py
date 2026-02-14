import streamlit as st
from groq import Groq

# --- CONFIG ---
st.set_page_config(page_title="KIZUNA AI WEB", page_icon="🔱", layout="wide", initial_sidebar_state="expanded")

# --- THE REAL CSS HACK FOR MENU BUTTON ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp { background-color: #0e0e0e; color: white; }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] { background-color: #131314 !important; min-width: 250px !important; }

    /* Hacking the Default Streamlit Sidebar Button */
    button[kind="headerNoSpacing"] {
        background-color: #FFD700 !important; /* Gold Color */
        color: black !important;
        border-radius: 10px !important;
        width: 60px !important;
        height: 45px !important;
        position: fixed !important;
        top: 15px !important;
        left: 15px !important;
        z-index: 999999 !important;
        display: block !important;
    }

    /* Making the "The Unbreakable Bond" text look clean */
    .header-text {
        text-align: center;
        color: #FFD700;
        font-family: 'Inter', sans-serif;
        margin-top: 20px;
    }

    /* Message styling */
    .stChatMessage { background-color: #1e1f20 !important; border-radius: 15px !important; }
    
    /* Hide default header to keep it clean */
    header { visibility: hidden; }
    footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# API Setup
client = Groq(api_key="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")

# Memory Lock
if "all_sessions" not in st.session_state: st.session_state.all_sessions = []
if "messages" not in st.session_state: st.session_state.messages = []

# --- SIDEBAR (THE MENU) ---
with st.sidebar:
    st.markdown("<h2 style='color: #FFD700;'>🔱 KIZUNA AI</h2>", unsafe_allow_html=True)
    if st.button("+ New Chat"):
        st.session_state.messages = []
        st.rerun()
    
    st.write("---")
    st.write("📂 **Recent History**")
    for i, session in enumerate(st.session_state.all_sessions):
        if st.button(session['title'], key=f"s_{i}"):
            st.session_state.messages = session['chats']
            st.rerun()
    
    st.write("---")
    if st.button("🗑️ Clear All History"):
        st.session_state.all_sessions = []
        st.rerun()

# --- MAIN CONTENT ---
st.markdown("<h3 class='header-text'>The Unbreakable Bond</h3>", unsafe_allow_html=True)

# Display Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Bolo Bhai..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                messages=[{"role": "system", "content": "You are Kizuna AI. Answer once, no repetition."}] + 
                         [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-6:]],
                model="llama-3.3-70b-versatile",
                temperature=0.6
            )
            reply = response.choices[0].message.content
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            
            # History Logic
            title = prompt[:20] + "..."
            if not any(s['title'] == title for s in st.session_state.all_sessions):
                st.session_state.all_sessions.insert(0, {"title": title, "chats": st.session_state.messages.copy()})
        except Exception as e:
            st.error(f"Error: {e}")
