import streamlit as st
import pandas as pd
import joblib

#Load trained model
model = joblib.load("models/model.pkl")

#Feature Extraction Function

def extract_features(url):
    features = {}

    features['url_length'] = len(url)
    features['num_dots'] = url.count('.')
    features['num_slashes'] = url.count('/')
    features['num_digits'] = sum(c.isdigit() for c in url)
    features['num_hyphens'] = url.count('-')
    features['num_underscores'] = url.count('_')
    features['num_questionmarks'] = url.count('?')
    features['num_equal'] = url.count('=')

    features['has_https'] = 1 if 'https' in url else 0
    features['has_http'] = 1 if 'http' in url else 0
    features['has_www'] = 1 if 'www' in url else 0
    features['has_at'] = 1 if '@' in url else 0

    suspicious_words = ['login','verify','secure','bank','account','update','free','bonus','signin','paypal']

    features['suspicious_words'] = sum(word in url.lower() for word in suspicious_words)

    return features

#StreamLit UI
st.set_page_config(page_title="Malicious URL Detector",
                   page_icon="🚨",
                   layout='centered')
st.title("🚨 Malicious URL Detector")
st.write("Detect whether a URL is safe or malicious using Machine Learning")

#User Input
url = st.text_input("Enter URL")

#Prediction

if st.button("Check URL"):

    if url.strip() == "":
        st.warning("Please enter a url")
    else :
        features = extract_features(url)
        input_data = pd.DataFrame([features])
        prediction = model.predict(input_data)[0]
        probabilities = model.predict_proba(input_data)[0]
        confidence = max(probabilities) * 100

        #Output

        st.subheader("Prediction Result")

        if prediction== "benign":
            st.success("Safe URL")

        else:
            st.error(f"Malicious URL Detected: {prediction}")

        st.info(f"Confidence Score : {confidence:.2f}%")

