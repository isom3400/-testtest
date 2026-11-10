import streamlit as st
from transformers import pipeline

# 1. Load a standard text-generation model
@st.cache_resource
def load_chatbot():
    # GPT-2 or a tiny equivalent doesn't need rigid templates; it just continues text
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
            
            # --- THE FIX: Convert chat history list into a single flat string prompt ---
            chat_prompt = ""
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    chat_prompt += f"User: {msg['content']}\n"
                else:
                    chat_prompt += f"AI: {msg['content']}\n"
            
            # Append "AI:" at the very end to prompt the model to answer as the AI
            chat_prompt += "AI:"
            
            # Run the model using the raw string prompt
            # clean_up_tokenization_spaces=True avoids weird spacing errors
            outputs = chatbot(chat_prompt, max_new_tokens=40, pad_token_id=50256)
            
            # Extract the raw generated text
            full_generated_text = outputs[0]["generated_text"]
            
            # Cut off the historical prompt so we ONLY get the brand new sentence after "AI:"
            new_response = full_generated_text[len(chat_prompt):].strip()
            
            # Clean up the output to stop it from writing the next "User:" turn itself
            ai_response = new_response.split("User:")[0].split("AI:")[0].strip()
            
            # Fallback if the model outputs nothing
            if not ai_response:
                ai_response = "I am processing that!"
                
            st.markdown(ai_response)
            
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": ai_response})

