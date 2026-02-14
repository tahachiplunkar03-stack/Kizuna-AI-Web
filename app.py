import streamlit as st
from groq import Groq
import re

# --- MASTER CONFIG ---
st.set_page_config(page_title="KIZUNA AI WEB", page_icon="🔱", layout="wide", initial_sidebar_state="expanded")

# Custom CSS to force Sidebar and Clean UI
st.markdown("""
    <style>
    .stApp { background-color: #0e0e0e; color: white; }
    /* Force sidebar visibility */
    [data-testid="stSidebar"] { background-color: #131314 !important; min-width: 250px !important; }
    .stChatMessage { background-color: #1e1f20 !important; border-radius: 15px !important; margin-bottom: 10px !important; }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    /* Code box styling */
    code { color: #FFD700 !important; background-color: #1e1e1e !important; }
    </style>
    """, unsafe_allow_html=True)

# API Setup
client = Groq(api_key="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")

# --- DATABASE / MEMORY LOCK ---
if "all_sessions" not in st.session_state: st.session_state.all_sessions = []
if "messages" not in st.session_state: st.session_state.messages = []

# --- SIDEBAR (RESTORED MENU) ---
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

# --- MAIN CHAT ---
st.markdown("<h3 style='text-align: center; color: #FFD700;'>The Unbreakable Bond</h3>", unsafe_allow_html=True)

# Display Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input (Fixed Bar)
if prompt := st.chat_input("Bolo Bhai..."):
    # Anti-Spam Check: Ignore empty or binary-like input
    if len(prompt.strip()) > 0:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                # Anti-Spam System Prompt included
                response = client.chat.completions.create(
                    messages=[{"role": "system", "content": "You are Kizuna AI. Be direct, no anime roleplay, no repeating sentences."}] + 
                             [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-6:]],
                    model="llama-3.3-70b-versatile",
                    temperature=0.6
                )
                reply = response.choices[0].message.content
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
                
                # Update Sidebar History
                title = prompt[:20] + "..."
                if not any(s['title'] == title for s in st.session_state.all_sessions):
                    st.session_state.all_sessions.insert(0, {"title": title, "chats": st.session_state.messages.copy()})
            except Exception as e:
                st.error(f"Error: {e}")
