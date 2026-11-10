import streamlit as st
from transformers import pipeline

# 1. Load a lightweight text generator (GPT-2 is small and fast for laptops)
@st.cache_resource
def load_text_gen():
    return pipeline("text-generation", model="gpt2")

generator = load_text_gen()

# 2. App UI
st.title("📚 AI Storybook Generator")
st.write("Start a story, and let the AI finish it!")

# Prompt input
prompt = st.text_input("Story Starter:", "Once upon a time, a small blue dragon discovered a...")

# Sidebar settings to teach students about AI hyperparameters
st.sidebar.header("AI Settings")
story_length = st.sidebar.slider("Story Length (Words)", 50, 200, 100)
creativity = st.sidebar.slider("Creativity (Temperature)", 0.6, 1.2, 0.8)

if st.button("Generate Story"):
    with st.spinner("Writing the next chapter..."):
        # 3. Generate text
        output = generator(
            prompt, 
            max_new_tokens=story_length, 
            temperature=creativity, 
            do_sample=True
        )
        
        story_text = output[0]['generated_text']
        
        # 4. Display result in a nice box
        st.subheader("Your AI Masterpiece:")
        st.info(story_text)
