import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

API_URL = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


def get_new_locator(html_string, old_locator):

    prompt = f"""
You are an expert HTML parser.

A Selenium script failed because it could not find an element with id "{old_locator}".

Find the NEW id of the same button.

STRICT RULES:
- Return ONLY the id
- No explanation
- Only one word

HTML:
{html_string}
"""

    payload = {
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        result = response.json()

        # 🔍 DEBUG (keep this)
        print("RAW RESPONSE:", result)

        # ✅ SAFE PARSING
        if "choices" in result and len(result["choices"]) > 0:
            output = result["choices"][0]["message"]["content"].strip()
        else:
            print("Unexpected response format")
            return fallback_locator(html_string)

    except Exception as e:
        print("API ERROR:", e)
        return fallback_locator(html_string)

    # ✅ CLEAN OUTPUT
    output = output.replace('"', '').replace("'", "")
    output = output.split("\n")[0].strip()
    output = output.split(" ")[-1]

    # ✅ FINAL SAFETY
    if output == "" or output.lower() in ["none", "id", "button"]:
        return fallback_locator(html_string)

    return output

def fallback_locator(html_string):
    print("Using fallback...")

    if "submit-action-btn" in html_string:
        return "submit-action-btn"

    return "NOT_FOUND"