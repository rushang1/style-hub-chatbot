import streamlit as st
from openai import OpenAI

# --- CONFIG ---
st.set_page_config(
    page_title="Style Hub Assistant",
    page_icon="👗",
    layout="centered"
)

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    body { background-color: #0f0f0f; }
    .stChatMessage { border-radius: 12px; padding: 8px; }
    .stTextInput input { border-radius: 20px; }
    header { visibility: hidden; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("## 👗 Style Hub — AI Fashion Assistant")
st.markdown("*Your personal stylist, available 24/7*")
st.divider()

# --- OPENAI CLIENT ---
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- CHAT HISTORY ---
if len(st.session_state.messages) > 20:
    st.warning("Session limit reached. Please refresh to start a new conversation.")
    st.stop()

# --- WELCOME MESSAGE ---
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.write("👋 Welcome to Style Hub! I can help you find the perfect outfit, check our timings, or answer any fashion questions. What can I help you with today?")

# --- DISPLAY HISTORY ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# --- CHAT INPUT ---
if prompt := st.chat_input("Ask me anything about fashion or our store..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {
                "role": "system",
                "content": """You are a warm, stylish AI assistant for Style Hub — a premium clothing store in Jalandhar. 
                You help customers with:
                - Outfit recommendations for any occasion
                - Store timings (10am - 8pm, all days)
                - Styling tips and fashion advice
                - Finding the right fit and colors for their body type
                
                Keep replies short, friendly and confident. Use emojis occasionally. 
                If asked anything unrelated to fashion or the store, politely redirect."""
            }
        ] + st.session_state.messages
    )

    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)
