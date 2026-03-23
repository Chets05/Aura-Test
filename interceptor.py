import requests

# Updated to the correct Direct Text Router URL for Phi-3
API_URL = "https://router.huggingface.co/hf-inference/models/microsoft/Phi-3-mini-4k-instruct"
headers = {"Authorization": "Bearer YOUR_HUGGING_FACE_TOKEN_HERE"}

def ask_ai_for_fix(failed_id, cleaned_html):
    """
    Sends the HTML to the LLM and asks for the new ID.
    """
    # This is 'Prompt Engineering' - giving the AI strict instructions 
    prompt = f"""
    Context: A Selenium script failed to find an element with ID: '{failed_id}'.
    Task: Look at the HTML below and identify the new ID or attribute for this element.
    Constraint: Return ONLY the new ID string. Do not explain.
    
    HTML:
    {cleaned_html}
    """

    payload = {"inputs": prompt}
    
    # Sending the request 
    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        # Extract the AI's text answer [cite: 65]
        ai_suggestion = response.json()[0]['generated_text']
        # We clean the output to ensure it's just the ID [cite: 65]
        return ai_suggestion.strip().split()[-1] 
    else:
        return None
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException

# --- THE CLEANER TOOL ---
def minimize_html(raw_html):
    soup = BeautifulSoup(raw_html, 'html.parser')
    # Remove the 'Noise' (scripts and styles)
    for junk in soup(["script", "style", "svg", "img", "video", "noscript"]):
        junk.decompose()
    return soup.prettify()

# --- THE INTERCEPTOR (The Main Logic) ---
def smart_click(driver, element_id):
    try:
        print(f"Attempting to find: {element_id}")
        target = driver.find_element("id", element_id)
        target.click()
    except NoSuchElementException:
        print(f"FAILURE: '{element_id}' moved or changed.")
        
        # 1. Capture the messy HTML
        raw_html = driver.page_source 
        
        # 2. CALL THE CLEANER (This is the part you were missing!)
        print("Cleaning HTML for the AI...")
        cleaned_html = minimize_html(raw_html)
        
        # 3. SAVE TO TEXT FILE (So you can see it in VS Code)
        with open("cleaned_dom.txt", "w", encoding="utf-8") as f:
            f.write(cleaned_html)
            
        print("SUCCESS: 'cleaned_dom.txt' has been created.")
        return "HEALING_READY"