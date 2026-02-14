import streamlit as st
from groq import Groq

# --- MOBILE OPTIMIZED CONFIG ---
st.set_page_config(page_title="KIZUNA AI", page_icon="🔱", layout="centered")

# Custom CSS to force Dark Theme & Fix UI
st.markdown("""
    <style>
    .stApp { background-color: #0e0e0e; color: white; }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Input box fix */
    div[data-testid="stChatInput"] {
        bottom: 20px !important;
    }
    
    /* Make chat bubbles look like a real app */
    .stChatMessage {
        background-color: #1a1a1a !important;
        border: 1px solid #333 !important;
        border-radius: 15px !important;
        padding: 10px !important;
    }

    /* Fix for that white gap at bottom */
    .main .block-container {
        padding-bottom: 100px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Branding
st.markdown("<h1 style='text-align: center; color: #FFD700; margin-bottom: 0;'>🔱 KIZUNA AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 12px; color: gray;'>The Unbreakable Bond</p>", unsafe_allow_html=True)

# API Initialization
client = Groq(api_key="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")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Action Buttons in one row
col1, col2 = st.columns(2)
with col1:
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
with col2:
    st.markdown("<p style='text-align:right; padding-top:10px;'>Kizuna Gang v1.0</p>", unsafe_allow_html=True)

st.write("---")

# Display Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Mobile Input
if prompt := st.chat_input("Bolo Bhai..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                model="llama-3.3-70b-versatile"
            )
            reply = response.choices[0].message.content
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"Error: {e}")
