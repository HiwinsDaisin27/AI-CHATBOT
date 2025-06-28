import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
import os

api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
gen_ai.configure(api_key=api_key)

st.set_page_config(
    page_title="Chat with Generative AI",
    page_icon='🧠',
    layout="centered",
)

model = gen_ai.GenerativeModel("gemini-2.0-flash")

def map_role(role):
    return "assistant" if role == "model" else role

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])
    st.session_state.initial_message_shown = False

st.title("🧠 Generative AI Chatbot")
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/4712/4712102.png", width=100)
st.sidebar.markdown("### 🤖 Your AI Side Chick")
st.sidebar.markdown("Built with Python, Gemini, and love 💻❤")



if st.sidebar.button("🔄 Reset Chat"):
    st.session_state.chat_session = model.start_chat(history=[])
    st.session_state.initial_message_shown = False
    st.rerun()

if not st.session_state.initial_message_shown:
    with st.chat_message("assistant"):
        st.markdown("👋 Hello! I'm your AI assistant. How can I help you today?")
    st.session_state.initial_message_shown = True

for message in st.session_state.chat_session.history:
    with st.chat_message(map_role(message.role)):
        st.markdown(message.parts[0].text)

user_input = st.chat_input("Type your message here...")

if user_input:
    st.chat_message("user").markdown(user_input)
    response = st.session_state.chat_session.send_message(user_input)
    with st.chat_message("assistant"):
        st.markdown(response.text)
