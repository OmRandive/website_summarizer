import streamlit as st
from openai import OpenAI
from bs4 import BeautifulSoup
import requests

# ------------------------
# Config
# ------------------------
OLLAMA_BASE_URL = "http://localhost:11434/v1"
MODEL = "llama3.2:1b"

client = OpenAI(
    base_url=OLLAMA_BASE_URL,
    api_key="ollama"
)

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
def summarize(url):
    content = fetch_website_contents(url)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Summarize this website briefly."},
            {"role": "user", "content": content}
        ]
    )

    return response.choices[0].message.content

# ------------------------
# UI
# ------------------------
st.title("🌐 Website Summarizer AI")

url = st.text_input("Enter website URL")

if st.button("Summarize"):
    if url:
        st.write("⏳ Processing...")
        summary = summarize(url)
        st.markdown(summary)
    else:
        st.warning("Please enter a URL")