import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# Importing Cheshta's LLM Connector Brain
from ai_healer import get_new_locator

# 1. Start the Execution Engine (The Browser)
print("Starting AuraTest Execution Engine...")
driver = webdriver.Chrome()

# Get the absolute path to your test.html file
file_path = "file://" + os.path.abspath("test.html")
driver.get(file_path)

# 2. The Interceptor Logic
try:
    # 💥 THE CRASH: We intentionally look for an ID that doesn't exist
    print("\nAttempting to click the old ID: 'old-button'")
    driver.find_element(By.ID, "old-button").click()
    print("Success on first try!")

except Exception as e:
    print("\n🚨 CRASH DETECTED! Activating Interceptor...")
    
    # Step A: Grab the current webpage HTML
    broken_html = driver.page_source
    
    # Step B: Call the LLM Connector
    print("Asking AI for the fix...")
    # We pass the broken HTML and the ID we *tried* to find
    new_id = get_new_locator(broken_html, "old-button")
    
    # Step C: The Recovery
    if new_id != "NOT_FOUND":
        print(f"✅ AI found the new ID: {new_id}. Resuming test!")
        driver.find_element(By.ID, new_id).click()
        print("🎉 Test Successfully Healed!")
    else:
        print("❌ AI could not find the button. Test failed.")

finally:
    # Keep the browser open for 3 seconds so you can see it work, then close
    time.sleep(3)
    driver.quit()
