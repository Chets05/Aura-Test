import os
import time
from selenium import webdriver
from interceptor import smart_click

def run_live_test():
    print("🚀 Launching Browser...")
    # Initialize the Selenium Chrome Driver
    driver = webdriver.Chrome()
    
    try:
        # Get the absolute path to your local test.html file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        html_file_path = f"file:///{os.path.join(current_dir, 'test.html')}"
        
        # Open the local webpage
        driver.get(html_file_path)
        time.sleep(2) # Brief pause so you can see the browser open
        
        print("\n🤖 Initiating AuraTest sequence...")
        # INTENTIONAL FAILURE: We tell the script to look for the old, broken ID
        smart_click(driver, "old-submit-btn")
        
        # Keep the browser open for 5 seconds so you can visually verify the click
        print("\nTest complete! Closing browser in 5 seconds...")
        time.sleep(5)
        
    finally:
        driver.quit()

if __name__ == "__main__":
    run_live_test()