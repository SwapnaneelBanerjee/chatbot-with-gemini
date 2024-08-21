import os

import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai


# Load environment variables
load_dotenv()

# Streamlit configuration
st.set_page_config(
    page_title="Neel's Answerbot!",
    page_icon="🤖",
    layout="centered", 
    menu_items={
        'Get Help': 'https://www.your-help-url.com',  # Need to add a help link soon
        'Report a bug': 'https://www.your-bug-report-url.com',  # Need to add a Bug report link
        'About': "# Neel's Answerbot\nThis is an AI-powered chatbot built with Streamlit and uses Google Gemini-Pro.",
        'Visit my page':'https://swapnaneelbanerjee.github.io/Profile/'
    }
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')


# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role


if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])


st.title("Neel's Smart AnswerBot")

for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

user_prompt = st.chat_input("Ask your question...")
if user_prompt:
    st.chat_message("user").markdown(user_prompt)

    
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)
