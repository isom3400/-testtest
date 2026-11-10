import streamlit as st
from groq import Groq

# Initialize a free Groq client
# Students can grab a free API key instantly at https://groq.com
def get_groq_client():
    return Groq(api_key="YOUR_FREE_GROQ_API_KEY")

client = get_groq_client()
model_name = "llama3-8b-8192"  # Fast, free, and smart conversational model

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# App UI Layout
st.title("🤖 Free Global AI Chatbot")
st.write("This version bypasses campus firewall issues to work seamlessly in the cloud!")

# Display past chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept User Input
if user_input := st.chat_input("Ask me anything..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Generate AI Response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model=model_name,
                messages=st.session_state.messages
            )
            
            ai_response = response.choices[0].message.content
            st.markdown(ai_response)
            
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
