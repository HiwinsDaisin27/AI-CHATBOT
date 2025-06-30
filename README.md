# 🤖 Generative AI Chatbot

A chatbot built using *Google Gemini* and *Streamlit*, capable of engaging in intelligent, conversational dialogue.

## 🚀 Features

- Built with Gemini 2.0 Flash (via Google Generative AI API)
- Runs fully on Streamlit Cloud (no paid services)
- Clean chat UI with assistant/user roles
- Custom welcome message + Reset button
- Chat history tracking during session
- Secure API key handling with st.secrets
  
## 🔐 User input and response logging to Google Sheets

- Includes timestamp
- Tracks unique user IDs per session

## 🧠 Tech Stack

- Python
- Streamlit
- Google Generative AI Studio (Gemini)
- Google Sheets (for logging)
- GitHub (for hosting code)
- Streamlit Cloud (for deployment)

## 🔐 API Key Handling

This app uses secret keys stored securely in Streamlit Cloud under Settings → Secrets:
- GOOGLE_API_KEY – Gemini API key
- GOOGLE_SERVICE_ACCOUNT – JSON key for Google Sheets integration

## 📊 Data Logging

Every message (user input and AI response) is logged to a connected *Google Sheet* named CHAT_LOGS with the following fields:
- Timestamp
- User Input
- AI Response
- User ID (UUID)

All data is securely handled using Google’s OAuth2 credentials and never exposed publicly.

## 🌐 Live Demo
[Click here to try the chatbot](https://ai-chatbotgit-nqemz54qjn5nyz6vnfpipp.streamlit.app/)

## 📸 Screenshot
![Chatbot Screenshot](![Screenshot 2025-06-29 020929](https://github.com/user-attachments/assets/3d9b65aa-a0e4-4f68-aec9-47fc476a0e45)
)
