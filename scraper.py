from bs4 import BeautifulSoup
import requests

def fetch_website_contents(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    for tag in soup(["script", "style", "img", "input"]):
        tag.decompose()

    return soup.get_text(separator="\n", strip=True)[:2000]
