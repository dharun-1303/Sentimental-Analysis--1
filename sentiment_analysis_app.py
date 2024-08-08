import streamlit as st
from textblob import TextBlob
import pandas as pd

def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    score = abs(sentiment)
    if sentiment > 0:
        return "Positive", score
    elif sentiment < 0:
        return "Negative", score
    else:
        return "Neutral", score

# Streamlit app
st.title("Sentiment Analysis")
st.write("---")

# Input text for sentiment analysis
user_text = st.text_input("Enter text for sentiment analysis:")

# File uploader for CSV
uploaded_file = st.file_uploader("Upload a CSV file for analysis:")

# Button to trigger analysis
if st.button("Analyze"):
    results = {"Text": [], "Sentiment": [], "Score": []}
    sentiments = {"Positive": 0, "Neutral": 0, "Negative": 0}

    # Analyze user text
    if user_text:
        sentiment, score = analyze_sentiment(user_text)
        results["Text"].append(user_text)
        results["Sentiment"].append(sentiment)
        results["Score"].append(score)
        sentiments[sentiment] += 1
    
    # Analyze CSV file
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            if df.shape[1] != 1:
                st.error("CSV file must contain only one column.")
            else:
                text_column = df.columns[0]
                for text in df[text_column]:
                    sentiment, score = analyze_sentiment(text)
                    results["Text"].append(text)
                    results["Sentiment"].append(sentiment)
                    results["Score"].append(score)
                    sentiments[sentiment] += 1
        except Exception as e:
            st.error(f"Error processing file: {e}")
    
    # Display the results
    if results["Text"]:
        results_df = pd.DataFrame(results)
        st.write(results_df)
        
        # Calculate and display sentiment percentages
        total_feedbacks = len(results["Text"])
        percentages = {sentiment: (count / total_feedbacks) * 100 for sentiment, count in sentiments.items()}
        st.write("### Sentiment Percentages:")
        for sentiment, percentage in percentages.items():
            st.write(f"Sentiment: {sentiment}, Percentage: {percentage:.2f}%")
    else:
        st.write("No text provided for analysis.")
