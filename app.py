import streamlit as st
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
def summarize(url):
    content = fetch_website_contents(url)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes websites clearly."},
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
        with st.spinner("⏳ Processing..."):
            summary = summarize(url)
        st.markdown(summary)
    else:
        st.warning("Please enter a URL")
