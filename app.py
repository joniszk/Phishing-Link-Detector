import streamlit as st
import google.generativeai as genai
import config  # API key in config.py

# Configuration
PAGE_TITLE = "Phishing Link Detector"
MODEL_NAME = "gemini-2.0-pro"  

st.set_page_config(page_title=PAGE_TITLE, page_icon="🔍", layout="centered")

# verify the API key
if not cred.API_KEY:
    st.error("API Key not found. Please add your Google API key in `cred.py`.")
    st.stop()

genai.configure(api_key=cred.API_KEY)

# Prompt Template for User
PROMPT_TEMPLATE = """
This app is used to find phishing threats. 
It will do the following:
- HTTPS presence check
- Shortened URL expansion
- Domain age verification

- Analysis Report
The app will provide a structured and easy to read security report, while highlighting risks and giving the user prevention steps. 
At the end of the report it will state whether the site is safe or phishing.
URL to analyze: {url}
"""

def analyze_url(url):
    """Uses Google's Gemini API to create a phishing analysis report."""
    try:
        prompt = PROMPT_TEMPLATE.format(url=url)
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        return response.text if response else "There is an error generating the report."
    except Exception as e:
        return f"Error: {e}"

# Streamlit UI
st.title(PAGE_TITLE)
st.markdown("Enter a URL to analyze for a report on phishing threats.")

url = st.text_input("URL:")

if st.button("Analyze"):
    if url:
        with st.spinner("Analyzing..."):
            report = analyze_url(url)
            st.markdown("Analysis Report: ")
            st.markdown(report, unsafe_allow_html=True)
    else:
        st.warning("Please enter a URL.")
