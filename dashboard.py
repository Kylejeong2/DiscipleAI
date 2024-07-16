import streamlit as st
from app import app

# Set page configuration
st.set_page_config(page_title="Disciple AI", layout="wide")

# Main title
st.title("Disciple AI")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What would you like to know about the Bible?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = app(prompt)
        st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar for additional options
st.sidebar.title("Options")
if st.sidebar.button("Clear Chat History"):
    st.session_state.messages = []

# Display the current chat history
st.sidebar.title("Chat History")
for message in st.session_state.messages:
    st.sidebar.text(f"{message['role']}: {message['content'][:50]}...")