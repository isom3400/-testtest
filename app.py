import streamlit as st
from transformers import pipeline

# 1. Load a standard text-generation model
@st.cache_resource
def load_chatbot():
    return pipeline("text-generation", model="gpt2")

chatbot = load_chatbot()

# 2. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. App UI Layout
st.title("🤖 Your AI Companion")
st.write("Talk to this open-source AI chatbot!")

# Display past chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Accept User Input
if user_input := st.chat_input("Say something to the AI..."):
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 5. Generate AI Response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            
            # Convert chat history list into a single flat script prompt
            chat_prompt = ""
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    chat_prompt += f"User: {msg['content']}\n"
                else:
                    chat_prompt += f"AI: {msg['content']}\n"
            
            # Append "AI:" to prompt the model to talk next
            chat_prompt += "AI:"
            
            # Run the model with creative sampling turned on
            outputs = chatbot(
                chat_prompt, 
                max_new_tokens=50, 
                pad_token_id=50256,
                do_sample=True,      # Crucial: stops the model from repeating the same text
                temperature=0.8,     # Adds randomness/creativity
                top_k=50
            )
            
            # Extract only the newly generated text
            full_generated_text = outputs[0]["generated_text"]
            new_response = full_generated_text[len(chat_prompt):].strip()
            
            # Clean up: stop the AI if it tries to generate the next "User:" line itself
            ai_response = new_response.split("User:")[0].split("AI:")[0].strip()
            
            # Fallback if the cleaning removed everything
            if not ai_response:
                ai_response = "I see! Tell me more."
                
            st.markdown(ai_response)
            
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": ai_response})

