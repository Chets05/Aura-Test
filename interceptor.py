from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# Import your newly built AI Healer Module
from ai_healer import get_new_locator

# --- THE CLEANER TOOL ---
def minimize_html(raw_html):
    """
    Strips out non-visual and structural noise from HTML to save LLM tokens.
    """
    soup = BeautifulSoup(raw_html, 'html.parser')
    # Remove the 'Noise' (scripts and styles)
    for junk in soup(["script", "style", "svg", "img", "video", "noscript"]):
        junk.decompose()
    return soup.prettify()

# --- THE INTERCEPTOR (The Main Logic) ---
def smart_click(driver, element_id):
    """
    Attempts to click an element by ID. If it fails, invokes AuraTest self-healing.
    """
    try:
        print(f"Attempting to click element with ID: {element_id}")
        
        # 1. Standard Execution
        target = driver.find_element(By.ID, element_id)
        target.click()
        print("Action clicked successfully on the first try!")
        
    except NoSuchElementException:
        print(f"FAILURE: Element '{element_id}' moved or changed.")
        
        # 2. Capture the messy HTML
        raw_html = driver.page_source 
        
        # 3. Call the Cleaner
        print("Cleaning HTML for the AI...")
        cleaned_html = minimize_html(raw_html)
        
        # 4. Save to Text File (Great for debugging)
        with open("cleaned_dom.txt", "w", encoding="utf-8") as f:
            f.write(cleaned_html)
            
        print("SUCCESS: 'cleaned_dom.txt' has been created.")
        
        # ---------------------------------------------------------
        # 5. THE AI INTEGRATION
        # ---------------------------------------------------------
        print("Handing over to AI Healer...")
        
        # Call your function using the cleaned DOM and the broken ID
        new_locator = get_new_locator(cleaned_html, element_id)
        
        # 6. Resume the test with the newly found ID
        if new_locator and new_locator != "NOT_FOUND":
            # Remove any # or . that the AI might have added to the start of the ID
            clean_locator = new_locator.lstrip('#').lstrip('.')
            
            print(f"HEALED! Resuming test with clean ID: '{clean_locator}'")
            
            # The retry action
            driver.find_element(By.ID, clean_locator).click() 
            print("Action clicked successfully using AI locator!")
             
            # ADD THIS: Save a report for the UI
            with open("healing_report.txt", "w") as report:
                report.write(f"STATUS: HEALED\n")
                report.write(f"OLD_ID: {element_id}\n")
                report.write(f"NEW_ID: {clean_locator}\n")
                report.write(f"TIMESTAMP: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            
        else:
            print("Fatal Error: AI could not find a replacement. Failing test.")
            raise # Let the test crash gracefully if the AI can't fix it
# ... existing code ...
            
           