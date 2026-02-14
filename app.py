import streamlit as st
from groq import Groq

# --- MOBILE OPTIMIZED CONFIG ---
st.set_page_config(page_title="KIZUNA AI", page_icon="🔱", layout="centered")

# Custom CSS for Mobile View
st.markdown("""
    <style>
    /* Main Background */
    .stApp { background-color: #0e0e0e; color: white; }
    
    /* Hide Streamlit Header/Footer for clean look */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Chat Container Tweaks */
    .stChatMessage {
        background-color: #1e1f20 !important;
        border-radius: 15px !important;
        margin-bottom: 10px !important;
        padding: 10px !important;
    }
    
    /* Code Box Styling */
    code { color: #FFD700 !important; font-size: 14px !important; }
    pre { background-color: #1a1a1a !important; border: 1px solid #333 !important; }

    /* Fix Input Bar at bottom */
    div[data-testid="stChatInput"] {
        bottom: 20px !important;
        background-color: transparent !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Branding
st.markdown("<h2 style='text-align: center; color: #FFD700;'>🔱 KIZUNA AI</h2>", unsafe_allow_html=True)

# API Initialization
client = Groq(api_key="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")

if "messages" not in st.session_state:
    st.session_state.messages = []

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
