#
# Description: A Streamlit web user interface for the AI Tutor Chatbot.
# This UI communicates with the FastAPI backend to provide a user-friendly chat experience.
#

import streamlit as st
import requests
import json

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Tutor Chatbot",
    page_icon="🤖",
    layout="centered"
)

# --- Title and Header ---
st.title("🤖 AI Tutor Chatbot")
st.write(
    "Welcome! I'm your AI Tutor, trained on key research papers in Artificial Intelligence. "
    "Ask me a question about concepts like Transformers, BERT, GANs, or RAG."
)

# --- API Endpoint ---
API_URL = "http://127.0.0.1:8000/ask"

# --- Session State Initialization ---
# This keeps the chat history persistent across reruns
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How can I help you today?"}]

# --- Display Chat History ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chat Input and Logic ---
if prompt := st.chat_input("Ask a question..."):
    # Add user message to chat history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response while processing
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        
        try:
            # Prepare the request data
            request_data = {"question": prompt}
            
            # Send the request to the FastAPI backend
            response = requests.post(API_URL, data=json.dumps(request_data))
            response.raise_for_status()  # Raise an exception for bad status codes
            
            # Get the answer from the response
            answer = response.json().get("answer", "Sorry, I couldn't get a response.")
            
            # Display the actual answer
            message_placeholder.markdown(answer)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": answer})

        except requests.exceptions.RequestException as e:
            error_message = f"Could not connect to the API. Please make sure the backend server is running. Error: {e}"
            message_placeholder.error(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})