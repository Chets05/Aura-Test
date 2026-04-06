import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# 1. Initialize the OpenAI Client to point to NVIDIA NIM
# We override the base_url to route traffic to NVIDIA instead of OpenAI
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)

def get_new_locator(html_string: str, old_locator: str) -> str:
    """
    Analyzes a broken HTML DOM snippet and returns the updated CSS/ID locator.
    
    Args:
        html_string (str): The scraped HTML DOM snippet from the Interceptor.
        old_locator (str): The previous locator (ID, class, XPath) that failed.
        
    Returns:
        str: The newly identified locator string, or an empty string if it fails.
    """
    
    # 2. THE SYSTEM PROMPT
    # We use explicit constraints and negative prompting to prevent conversational filler.
    system_prompt = (
        "You are an expert QA Automation Engineer acting as a strict data parser. "
        "Your only job is to analyze an HTML snippet and output a valid CSS selector or XPath "
        "to replace a broken locator. "
        "STRICT RULES: "
        "1. Output exactly ONE valid locator string (CSS selector preferred). "
        "2. Do NOT output any explanations, markdown code blocks (```), or conversational text. "
        "3. If you cannot find a logical replacement, output exactly: NOT_FOUND"
    )

    # 3. THE USER PROMPT
    # Inject the runtime variables clearly.
    user_prompt = f"""
    Broken Locator: {old_locator}
    
    Current HTML DOM Snippet:
    {html_string}
    
    Updated Locator:
    """

    try:
        # 4. THE API CALL
        response = client.chat.completions.create(
            model="meta/llama-3.1-70b-instruct", 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.0, # Greedy decoding: 0.0 forces the model to be deterministic and factual
            top_p=1.0,
            max_tokens=50    # We only need a short string, capping this saves time and compute
        )

        # 5. PARSE AND CLEAN THE OUTPUT
        # Extract the text and strip whitespace or accidental newlines
        raw_output = response.choices[0].message.content.strip()
        
        # Defensive programming: Strip out markdown backticks just in case the LLM disobeys Rule 2
        clean_locator = raw_output.replace("`", "").strip()
        
        if clean_locator == "NOT_FOUND":
            print(f"AI Healer: Could not confidently identify a replacement for '{old_locator}'.")
            return ""
            
        return clean_locator

    except Exception as e:
        print(f"AI Healer Error: API communication failed. Details: {e}")
        return ""

# ==========================================
# Test Execution Block (For local testing)
# ==========================================
if __name__ == "__main__":
    # Simulated payload from Module 2 (The Interceptor)
    sample_broken_locator = "#submit_btn_v1"
    sample_html_dom = """
    <div class="login-form">
        <input type="text" id="username" placeholder="Enter username">
        <input type="password" id="password" placeholder="Enter password">
        <button id="login-action" class="btn primary-btn">Login Securely</button>
    </div>
    """
    
    print("Initializing AI Healer...")
    new_locator = get_new_locator(sample_html_dom, sample_broken_locator)
    
    print(f"Old Locator: {sample_broken_locator}")
    print(f"Healed Locator: {new_locator}")