import streamlit as st
import requests


FASTAPI_URL = "http://127.0.0.1:8000/chat"

st.set_page_config(page_title="ICT HUB Chatbot")
st.title("ICT HUB Smart Assistant")
st.markdown("Welcome! I am here to answer your inquiries about our services.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Type your question here...")

if user_input:

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)


    try:
        response = requests.post(FASTAPI_URL, json={"user_message": user_input}, timeout=10)
        if response.status_code == 200:
            api_data = response.json()
            bot_reply = api_data["bot_response"]
        else:
            bot_reply = "Sorry, I encountered an error processing your request internally."
    except requests.exceptions.ConnectionError:
        bot_reply = "Sorry, the smart server is currently out of service (FastAPI is not running)."
    except Exception as e:
        bot_reply = "Sorry, an unexpected error occurred."


    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)