import streamlit as st
import streamlit.components.v1 as components
from openai import OpenAI
from bs4 import BeautifulSoup
import requests
import os

# ------------------------
# Config (OpenAI)
# ------------------------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "gpt-4o-mini"

# ------------------------
# Scraper
# ------------------------
def fetch_website_contents(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    for tag in soup(["script", "style", "img", "input"]):
        tag.decompose()

    return soup.get_text(separator="\n", strip=True)[:2000]

# ------------------------
# Summarizer
# ------------------------
def summarize(url, style, custom):
    content = fetch_website_contents(url)

    style_map = {
        "Short": "Summarize briefly in 3-4 lines.",
        "Detailed": "Provide a detailed explanation.",
        "Bullet Points": "Summarize in clear bullet points.",
        "Beginner Friendly": "Explain in very simple terms."
    }

    instruction = style_map.get(style, "")

    if custom:
        instruction += f" Also follow this instruction: {custom}"

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes websites clearly."},
            {"role": "user", "content": instruction + "\n\n" + content}
        ]
    )

    return response.choices[0].message.content

# ------------------------
# UI
# ------------------------
st.set_page_config(page_title="Website Summarizer AI", layout="wide")

st.title("🌐 Website Summarizer AI")
st.caption("Summarize any website with AI + preview it live")

url = st.text_input("Enter website URL")

# Style selector
style = st.selectbox(
    "Choose summary style",
    ["Short", "Detailed", "Bullet Points", "Beginner Friendly"]
)

# Custom instruction
custom = st.text_input(
    "Optional: Customize the summary",
    placeholder="e.g., make it funny, focus on key points, explain like a teacher..."
)

# Button action
if st.button("Summarize"):
    if url:
        with st.spinner("⏳ Processing..."):
            summary = summarize(url, style, custom)

        # Layout (side by side)
        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("🧠 Summary")
            st.markdown(summary)

        with col2:
            st.subheader("🌐 Website Preview")
            components.iframe(url, height=500, scrolling=True)

        # Fallback link
        st.info("If preview doesn't load, open below:")
        st.link_button("🔗 Open Website", url)

    else:
        st.warning("Please enter a URL")
