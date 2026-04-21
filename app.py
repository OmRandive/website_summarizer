import streamlit as st
import streamlit.components.v1 as components
from scraper import fetch_website_contents
from summarizer import summarize

st.set_page_config(page_title="Website Summarizer AI", layout="wide")

st.title("🌐 Website Summarizer AI")

url = st.text_input("Enter website URL")

style = st.selectbox(
    "Choose summary style",
    ["Short", "Detailed", "Bullet Points", "Beginner Friendly"]
)

custom = st.text_input(
    "Optional instruction",
    placeholder="e.g., make it funny, focus on key points..."
)

if st.button("Summarize"):
    if url:
        with st.spinner("Processing..."):
            content = fetch_website_contents(url)
            summary = summarize(content, style, custom)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Summary")
            st.markdown(summary)

        with col2:
            st.subheader("Preview")
            components.iframe(url, height=500)

    else:
        st.warning("Enter a URL")
