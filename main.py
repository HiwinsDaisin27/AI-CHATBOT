import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import json
import uuid

load_dotenv()
api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
gen_ai.configure(api_key=api_key)

st.set_page_config(
    page_title="Chat with Generative AI",
    page_icon='🧠',
    layout="centered",
)

background_image = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url('https://images.unsplash.com/photo-1527443154391-507e9dc6c5cc?auto=format&fit=crop&w=1400&q=80');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    opacity: 0.98;
}

[data-testid="stSidebar"] {
    background-color: rgba(0, 0, 0, 0.8);
}

[data-testid="stChatMessage"] {
    background-color: rgba(255, 255, 255, 0.85);
    border-radius: 10px;
    padding: 8px;
    margin-bottom: 8px;
    box-shadow: 0px 0px 8px rgba(0,0,0,0.1);
}
</style>
"""
st.markdown(background_image, unsafe_allow_html=True)

model = gen_ai.GenerativeModel("gemini-2.0-flash")

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])
    st.session_state.initial_message_shown = False

if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

st.title("🧠 Generative AI Chatbot")
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/4712/4712102.png", width=100)
st.sidebar.markdown("### 🤖 Your  AI  Side  Kick")
st.sidebar.markdown("Built  with  Python, Streamlit , and  love 💻❤")

if st.sidebar.button("🔄 Reset Chat"):
    st.session_state.chat_session = model.start_chat(history=[])
    st.session_state.initial_message_shown = False
    st.session_state.user_id = str(uuid.uuid4())
    st.rerun()

if not st.session_state.initial_message_shown:
    with st.chat_message("assistant"):
        st.markdown("👋 Hello! I'm your AI assistant. How can I help you today?")
    st.session_state.initial_message_shown = True

for message in st.session_state.chat_session.history:
    with st.chat_message("assistant" if message.role == "model" else message.role):
        st.markdown(message.parts[0].text)

user_input = st.chat_input("Type your message here...")

if user_input:
    st.chat_message("user").markdown(user_input)
    response = st.session_state.chat_session.send_message(user_input)
    with st.chat_message("assistant"):
        st.markdown(response.text)

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
