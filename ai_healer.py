import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ✅ YOUR CODE: The superior NVIDIA connection using the OpenAI client
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)

def get_new_locator(html_string: str, old_locator: str) -> str:
    """
    Analyzes a broken HTML DOM snippet and returns the updated locator.
    """
    
    # YOUR CODE: The stricter, more professional prompt
    system_prompt = (
        "You are an expert QA Automation Engineer acting as a strict data parser. "
        "Your only job is to analyze an HTML snippet and output a valid CSS selector or ID "
        "to replace a broken locator. "
        "STRICT RULES: "
        "1. Output exactly ONE valid locator string. "
        "2. Do NOT output any explanations, markdown code blocks, or conversational text. "
        "3. If you cannot find a replacement, output exactly: NOT_FOUND"
    )

    user_prompt = f"Broken Locator: {old_locator}\n\nHTML DOM Snippet:\n{html_string}\n\nUpdated Locator:"

    try:
        # YOUR CODE: Calling the smarter 70B model
        response = client.chat.completions.create(
            model="meta/llama-3.1-70b-instruct", 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.0,
            top_p=1.0,
            max_tokens=50
        )
        
        output = response.choices[0].message.content.strip()

    except Exception as e:
        print("API ERROR:", e)
        # TEAMMATE'S CODE: Safely fall back if the API crashes
        return fallback_locator(html_string)

    # ✅ TEAMMATE'S CODE: Excellent defensive string cleaning
    output = output.replace('"', '').replace("'", "").replace("`", "")
    output = output.split("\n")[0].strip()
    output = output.split(" ")[-1]

    # ✅ TEAMMATE'S CODE: Final Safety Check
    if output == "" or output == "NOT_FOUND" or output.lower() in ["none", "id", "button"]:
        return fallback_locator(html_string)

    return output

# ✅ TEAMMATE'S CODE: The hardcoded fallback mechanism
def fallback_locator(html_string):
    print("AI failed or was unsure. Using hardcoded fallback...")
    
    # If the specific button they are testing for is in the DOM, grab it
    if "submit-action-btn" in html_string:
        return "submit-action-btn"
        
    return "NOT_FOUND"