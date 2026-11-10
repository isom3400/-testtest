import streamlit as st
from openai import OpenAI

# 1. Initialize the HKUST Azure OpenAI Client
# (We put it in a function so it initializes cleanly)
def get_openai_client():
    apikey = "6b81055fda7247c5a51e7d3789be35b3" # Replace with your actual student key
    custom_headers = {"api-key": apikey}
    
    return OpenAI(
        base_url="https://azure-api.net",
        api_key=apikey,
        default_headers=custom_headers,
    )

client = get_openai_client()
model_name = "gpt-4o-mini"

# 2. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# 3. App UI Layout
st.title("🤖 HKUST AI Chatbot")
st.write("Powered by gpt-4o-mini through the campus API gateway!")

# Display past chat messages from history (ignoring the hidden system message)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 4. Accept User Input
if user_input := st.chat_input("Ask me anything about ISOM3400..."):
    # Display user message instantly
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 5. Generate AI Response via Azure Gateway
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Call the OpenAI API using your precise configuration layout
            response = client.chat.completions.create(
                model=model_name,
                messages=st.session_state.messages
            )
            
            # Extract the text answer smoothly
            ai_response = response.choices[0].message.content
            st.markdown(ai_response)
            
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": ai_response})

