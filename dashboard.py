import streamlit as st
from app import app
from generate_context import generate_context

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

context = [] #start with no context
currContext = "" #start with no current context
# Accept user input
if prompt := st.chat_input("What would you like to know about the Bible?"):
    # newContext = generate_context(currContext, context)
    # currContext = newContext
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = app(prompt, context=None)
        st.markdown("### Answer")
        st.markdown(response[0])
        st.markdown("### Verses")
        st.markdown(response[1])
    context = [prompt, response[0]]
    # Add assistant response to chat history
    assistant_content = f"### Answer\n{response[0]}\n\n### Verses\n{response[1]}"
    st.session_state.messages.append({"role": "assistant", "content": assistant_content})

# Sidebar for additional options
st.sidebar.title("Options")
if st.sidebar.button("Clear Chat History"):
    st.session_state.messages = []

# Display the current chat history
st.sidebar.title("Chat History")
for message in st.session_state.messages:
    st.sidebar.text(f"{message['role']}: {message['content'][:50]}...")