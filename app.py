import streamlit as st
from groq import Groq

# --- MOBILE & WEB OPTIMIZED CONFIG ---
st.set_page_config(page_title="KIZUNA AI", page_icon="🔱", layout="wide")

# Custom CSS for Kizuna Master Look
st.markdown("""
    <style>
    .stApp { background-color: #0e0e0e; color: white; }
    [data-testid="stSidebar"] { background-color: #131314 !important; border-right: 1px solid #333; }
    .stChatMessage { background-color: #1e1f20 !important; border-radius: 15px !important; margin-bottom: 10px !important; }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    /* Style for history buttons in sidebar */
    .stButton>button { width: 100%; text-align: left; background-color: transparent; border: none; color: gray; }
    .stButton>button:hover { color: #FFD700; background-color: #232324; }
    </style>
    """, unsafe_allow_html=True)

# API Initialization
client = Groq(api_key="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")

# --- MEMORY MANAGEMENT ---
if "all_sessions" not in st.session_state:
    st.session_state.all_sessions = [] # Sabhi purani chats yahan rahengi

if "messages" not in st.session_state:
    st.session_state.messages = [] # Current chat

# --- SIDEBAR (RESTORED RECENT HISTORY) ---
with st.sidebar:
    st.markdown("<h2 style='color: #FFD700;'>🔱 KIZUNA AI</h2>", unsafe_allow_html=True)
    
    if st.button("+ New Chat", key="new_chat_btn"):
        st.session_state.messages = []
        st.rerun()
    
    st.write("---")
    st.write("📂 **Recent History**")
    
    # History list display logic
    for i, session in enumerate(st.session_state.all_sessions):
        if st.button(session['title'], key=f"session_{i}"):
            st.session_state.messages = session['chats']
            st.rerun()

# --- MAIN CHAT INTERFACE ---
st.markdown("<h3 style='text-align: center; color: #FFD700;'>The Unbreakable Bond</h3>", unsafe_allow_html=True)

# Display Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Bolo Bhai..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI Response
    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                model="llama-3.3-70b-versatile"
            )
            reply = response.choices[0].message.content
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            
            # Update History Sidebar
            session_title = prompt[:20] + "..."
            # Check if session exists, else add new
            existing = False
            for s in st.session_state.all_sessions:
                if s['title'] == session_title:
                    s['chats'] = st.session_state.messages
                    existing = True
            if not existing:
                st.session_state.all_sessions.insert(0, {"title": session_title, "chats": st.session_state.messages})
                
        except Exception as e:
            st.error(f"Error: {e}")
