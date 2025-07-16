import os, requests
from dotenv import load_dotenv

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

def query_openai(prompt):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer " + OPENAI_KEY,
        "Content-Type": "application/json"
    }
    body = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": "You are Mythiq, a visionary assistant."},
            {"role": "user", "content": prompt}
        ]
    }
    res = requests.post(url, headers=headers, json=body)
    res.raise_for_status()
    return res.json()["choices"][0]["message"]["content"]
