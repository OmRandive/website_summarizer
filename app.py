import streamlit as st
import streamlit.components.v1 as components
from scraper import fetch_website_contents
from summarizer import summarize
import time
if "history" not in st.session_state:
    st.session_state.history = []

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
    start_time = time.time()
    if url:
        with st.spinner("Processing..."):
            content = fetch_website_contents(url)
            summary = summarize(content, style, custom)
            original_len = len(content)
            summary_len = len(summary)
            compression = round((summary_len / original_len) * 100, 2)
            processing_time = round(end_time - start_time, 2)
        st.session_state.history.append({
            "url": url,
            "summary": summary
        })

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Summary")
            st.markdown(summary)

        with col2:
            st.subheader("Preview")
            components.iframe(url, height=500)
        
    else:
        st.warning("Enter a URL")

    end_time = time.time()


compression = round((summary_len / original_len) * 100, 2)
processing_time = round(end_time - start_time, 2)
st.subheader("📊 Analysis")

colA, colB, colC, colD = st.columns(4)

colA.metric("Original Length", original_len)
colB.metric("Summary Length", summary_len)
colC.metric("Compression %", f"{compression}%")
colD.metric("Time Taken", f"{processing_time}s")

st.divider()
st.subheader("🕘 History")

if st.session_state.history:
    for i, item in enumerate(reversed(st.session_state.history), 1):
        with st.expander(f"{i}. {item['url']}"):
            st.markdown(item["summary"])
else:
    st.write("No history yet.")

if st.button("Clear History"):
    st.session_state.history = []
