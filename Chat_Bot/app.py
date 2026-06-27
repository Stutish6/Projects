import streamlit as st
from main import chat

#This the title on the tab on web
st.set_page_config(
    page_title = "DIET ASSISTANT",
)

#Title of the page
st.title("DIET PLANNING ASSISTANT")


#session_state stores data while the app is running
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


if "messages" not in st.session_state:
    st.session_state.messages = []

#Chat input box title to be set
user_input = st.chat_input("Ask me anything about diet!!!")

if user_input:

    st.session_state.chat_history.append(
        ("user",user_input)
    )

    reply = chat(user_input)

    st.session_state.chat_history.append(
        ("assistant",reply)
    )

for role, message in st.session_state.chat_history:

    with st.chat_message(role):
        st.write(message)