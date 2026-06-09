import requests
from bs4 import BeautifulSoup
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def clean_text(text):
    """Basic preprocessing for privacy policy text"""

    text = text.lower()

    text = re.sub(r'\n', ' ', text)

    text = re.sub(r'\s+', ' ', text)

    text = re.sub(r'[^a-zA-Z0-9., ]', '', text)

    return text


def fetch_privacy_policy(url):

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)

        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        # remove scripts and styles
        for script in soup(["script", "style", "noscript"]):
            script.decompose()

        text = soup.get_text(separator=" ")

        text = clean_text(text)

        return text

    except Exception as e:
        print("Error fetching policy:", e)
        return None