import streamlit as st
from transformers import pipeline

# 1. Load the conversational pipeline (optimized for Streamlit Cloud)
@st.cache_resource
def load_chatbot():
    # Blenderbot is a great, lightweight open-source conversational model
    return pipeline("conversational", model="facebook/blenderbot-400M-distill")

chatbot = load_chatbot()

# 2. Initialize Chat History
# Streamlit reruns the whole script on every input, so we use st.session_state 
# to keep memory of the conversation, exactly like ChatGPT.
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. App UI Layout
st.title("🤖 Your AI Companion")
st.write("Talk to this open-source AI chatbot! It remembers what you say during the session.")

# Display past chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Accept User Input
if user_input := st.chat_input("Say something to the AI..."):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 5. Generate AI Response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Hugging Face Conversational pipeline needs a specific structure
            from transformers import Conversation
            
            # Reconstruct the conversation history for the model
            conversation = Conversation()
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    conversation.add_user_input(msg["content"])
                else:
                    conversation.mark_processed() # Marks the previous turn as done
            
            # Send the conversation history to the model
            updated_conversation = chatbot(conversation)
            
            # Extract the newest response from the AI
            ai_response = updated_conversation.generated_responses[-1]
            st.markdown(ai_response)
            
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
