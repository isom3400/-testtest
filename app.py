import os
import streamlit as st
from huggingface_hub import InferenceClient


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Hugging Face Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Hugging Face Chatbot")
st.caption("A simple chatbot built with Streamlit and Hugging Face")


# ---------------------------------------------------------
# Hugging Face configuration
# ---------------------------------------------------------
# Store HF_TOKEN in Streamlit Cloud > App settings > Secrets
HF_TOKEN = st.secrets.get("HF_TOKEN", os.getenv("HF_TOKEN"))

if not HF_TOKEN:
    st.error(
        "Hugging Face token not found. "
        "Please add HF_TOKEN to your Streamlit secrets."
    )
    st.stop()


# Change this if you want to use another compatible model
MODEL = "Qwen/Qwen2.5-7B-Instruct"

client = InferenceClient(
    model=MODEL,
    token=HF_TOKEN
)


# ---------------------------------------------------------
# Initialize conversation
# ---------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! How can I help you today?"
        }
    ]


# ---------------------------------------------------------
# Show chat history
# ---------------------------------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ---------------------------------------------------------
# User input
# ---------------------------------------------------------
if prompt := st.chat_input("Type your message here..."):

    # Save and display user's message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)


    # -----------------------------------------------------
    # Generate response
    # -----------------------------------------------------
    with st.chat_message("assistant"):

        try:

            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are a helpful AI assistant. "
                        "Answer clearly and concisely."
                    )
                }
            ]

            messages.extend(st.session_state.messages)

            response = client.chat_completion(
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )

            answer = response.choices[0].message.content

            st.markdown(answer)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

        except Exception as e:
            st.error(f"Error communicating with Hugging Face: {e}")


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------
with st.sidebar:

    st.header("Chatbot Settings")

    st.write("**Model**")
    st.code(MODEL)

    if st.button("🗑️ Clear conversation"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Hello! How can I help you today?"
            }
        ]

        st.rerun()
