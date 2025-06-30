import streamlit as st from dotenv import load_dotenv import google.generativeai as gen_ai import os import gspread from oauth2client.service_account import ServiceAccountCredentials from datetime import datetime import json import uuid

load_dotenv() api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY") gen_ai.configure(api_key=api_key)

st.set_page_config(page_title="🧠 Generative AI Chatbot", layout="centered")

custom_css = """

<style>
    body {
        background-image: url("https://images.unsplash.com/photo-1507525428034-b723cf961d3e");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white;
    }
    .block-container {
        background-color: rgba(0, 0, 0, 0.6);
        border-radius: 15px;
        padding: 2rem;
    }
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        color: white;
    }
    .stTextInput > div > input {
        background-color: #1e1e1e;
        color: white;
        border-radius: 10px;
        padding: 10px;
    }
</style>"""

st.markdown(custom_css, unsafe_allow_html=True)

model = gen_ai.GenerativeModel("gemini-2.0-flash")

if "chat_session" not in st.session_state: st.session_state.chat_session = model.start_chat(history=[]) st.session_state.initial_message_shown = False

if "user_id" not in st.session_state: st.session_state.user_id = str(uuid.uuid4())

st.markdown("<h1 style='text-align: center;'>💬 Generative AI Chatbot</h1>", unsafe_allow_html=True)

st.sidebar.image("https://cdn-icons-png.flaticon.com/512/4712/4712102.png", width=100) st.sidebar.markdown("### 🤖 Your AI Side Kick") st.sidebar.markdown("Built with Python, Streamlit, and 💙")

if st.sidebar.button("🔄 Reset Chat"): st.session_state.chat_session = model.start_chat(history=[]) st.session_state.initial_message_shown = False st.session_state.user_id = str(uuid.uuid4()) st.rerun()

if not st.session_state.initial_message_shown: with st.chat_message("assistant"): st.markdown("👋 Hello! I'm your AI assistant. How can I help you today?") st.session_state.initial_message_shown = True

for message in st.session_state.chat_session.history: with st.chat_message("assistant" if message.role == "model" else message.role): st.markdown(message.parts[0].text)

user_input = st.chat_input("Type your message here...")

if user_input: st.chat_message("user").markdown(user_input) response = st.session_state.chat_session.send_message(user_input) with st.chat_message("assistant"): st.markdown(response.text)

try:
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    service_account_info = json.loads(st.secrets["GOOGLE_SERVICE_ACCOUNT"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
    client = gspread.authorize(creds)
    sheet = client.open("CHAT_LOGS").sheet1
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([timestamp, user_input, response.text, st.session_state.user_id])
except Exception as e:
    st.error(f"Error saving to Google Sheets: {e}")
