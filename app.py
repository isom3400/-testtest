import streamlit as st
from transformers import pipeline
import pandas as pd

# 1. Load the Hugging Face emotion classifier
# This downloads a model trained to detect emotions (joy, sadness, anger, fear, etc.)
@st.cache_resource  # Keeps the model in memory so it doesn't reload every time
def load_model():
    return pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion", top_k=None)

classifier = load_model()

# 2. App UI
st.title("😊 Happiness & Emotion Detector")
st.write("Type how your day went, and the AI will analyze your emotions!")

user_text = st.text_area("How are you feeling today?", "I had a wonderful day today and accomplished a lot!")

if st.button("Analyze Emotion"):
    if user_text.strip() == "":
        st.warning("Please type something first!")
    else:
        # 3. Run the model
        with st.spinner("Analyzing text..."):
            results = classifier(user_text)[0]
        
        # 4. Process and display results
        # Format the data for a nice Streamlit bar chart
        emotions = [res['label'] for res in results]
        scores = [res['score'] for res in results]
        df = pd.DataFrame({"Score": scores}, index=emotions)
        
        # Find the dominant emotion
        top_emotion = results[0]['label']
        
        st.success(f"Primary Emotion Detected: **{top_emotion.capitalize()}**")
        st.bar_chart(df)
