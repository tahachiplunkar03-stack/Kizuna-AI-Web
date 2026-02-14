import streamlit as st
from groq import Groq

# --- ULTIMATE CONFIG ---
# Maine initial_sidebar_state ko wapas 'expanded' kar diya hai taaki load hote hi dikhe
st.set_page_config(page_title="KIZUNA AI WEB", page_icon="🔱", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM CSS FOR INTERACTIVE MENU ---
st.markdown("""
    <style>
    .stApp { background-color: #0e0e0e; color: white; }
    
    /* Yellow Menu Button Styling */
    div.stButton > button:first-child {
        background-color: #FFD700 !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        border: none !important;
        height: 45px !important;
        width: 100px !important;
    }

    /* Hide the original tiny arrow button which is causing issues */
    button[kind="headerNoSpacing"] { display: none !important; }

    /* Clean Sidebar and Chat */
    [data-testid="stSidebar"] { background-color: #131314 !important; }
    .stChatMessage { background-color: #1e1f20 !important; border-radius: 15px !important; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# API & Memory Setup
client = Groq(api_key="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")
if "all_sessions" not in st.session_state: st.session_state.all_sessions = []
if "messages" not in st.session_state: st.session_state.messages = []

# --- THE REAL SIDEBAR LOGIC ---
with st.sidebar:
    st.markdown("<h2 style='color: #FFD700;'>🔱 KIZUNA AI</h2>", unsafe_allow_html=True)
    
    # New Chat Button inside Sidebar
    if st.button("+ New Chat", key="sidebar_new_chat"):
        st.session_state.messages = []
        st.rerun()
    
    st.write("---")
    st.write("📂 **Recent History**")
    for i, session in enumerate(st.session_state.all_sessions):
        if st.button(session['title'], key=f"hist_{i}"):
            st.session_state.messages = session['chats']
            st.rerun()

# --- MAIN SCREEN ---
# Top bar with a working "Home/Reset" Menu button
col1, col2 = st.columns([1, 5])
with col1:
    if st.button("☰ Menu"):
        # Isse sidebar toggle hone ki feel aayegi (Mobile par swipe bhi kaam karega)
        st.toast("Sidebar is on the left! Swipe or use the arrow.")

st.markdown("<h3 style='text-align: center; color: #FFD700;'>The Unbreakable Bond</h3>", unsafe_allow_html=True)

# Display Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Bolo Bhai..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                messages=[{"role": "system", "content": "You are Kizuna AI. Direct answers only."}] + 
                         [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-6:]],
                model="llama-3.3-70b-versatile"
            )
            reply = response.choices[0].message.content
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            
            # Auto-save to History
            title = prompt[:20] + "..."
            if not any(s['title'] == title for s in st.session_state.all_sessions):
                st.session_state.all_sessions.insert(0, {"title": title, "chats": st.session_state.messages.copy()})
        except Exception as e:
            st.error(f"Error: {e}")
