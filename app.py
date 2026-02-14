import streamlit as st
from groq import Groq

# --- Page Config ---
st.set_page_config(page_title="KIZUNA AI WEB", page_icon="🔱")

# --- Kizuna Vibe Custom CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0e0e0e; color: white; }
    .stChatMessage { border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔱 KIZUNA AI")

# API Setup
client = Groq(api_key="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")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Chat
if prompt := st.chat_input("Bolo Bhai..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            model="llama-3.3-70b-versatile"
        )
        reply = response.choices[0].message.content
        st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
