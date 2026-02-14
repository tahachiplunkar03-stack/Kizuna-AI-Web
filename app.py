import streamlit as st
from groq import Groq

# --- CONFIG ---
st.set_page_config(page_title="KIZUNA AI WEB", page_icon="🔱", layout="wide", initial_sidebar_state="expanded")

# --- THE UNSTOPPABLE MENU BUTTON CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0e0e0e; color: white; }
    
    /* 1. Custom Floating Button (Sirf visual ke liye) */
    .floating-menu {
        position: fixed;
        top: 12px;
        left: 12px;
        z-index: 1000000;
        background-color: #FFD700;
        color: black;
        border-radius: 8px;
        padding: 8px 12px;
        font-weight: bold;
        font-family: 'Inter', sans-serif;
        pointer-events: none; /* Taaki niche wala asli button click ho sake */
    }

    /* 2. Hacking the REAL Streamlit Button to be exactly under our visual button */
    button[kind="headerNoSpacing"] {
        position: fixed !important;
        top: 10px !important;
        left: 10px !important;
        width: 70px !important;
        height: 50px !important;
        z-index: 1000001 !important;
        opacity: 0.1 !important; /* Thoda visible rakha hai taaki tu dhoond sake */
        background-color: #FFD700 !important;
    }

    /* Sidebar & Chat Tweaks */
    [data-testid="stSidebar"] { background-color: #131314 !important; }
    .stChatMessage { background-color: #1e1f20 !important; border-radius: 15px !important; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
    </style>
    
    <div class="floating-menu">☰ Menu</div>
    """, unsafe_allow_html=True)

# API & Memory Logic
client = Groq(api_key="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")
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
st.markdown("<h3 style='text-align: center; color: #FFD700;'>The Unbreakable Bond</h3>", unsafe_allow_html=True)

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
                messages=[{"role": "system", "content": "You are Kizuna AI. No anime spam. Be direct."}] + 
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
