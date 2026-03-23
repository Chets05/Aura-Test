from selenium import webdriver
from interceptor import smart_click # This imports your Step 2 & 3 code
import os

# Setup Chrome (Selenium 4 manages the driver automatically)
driver = webdriver.Chrome()

try:
    # Get the absolute path of your local HTML file
    file_path = "file://" + os.path.abspath("test_site.html")
    driver.get(file_path)

    # TEST CASE: Try to click an ID that IS NOT in the HTML
    # This should trigger your 'except' block and 'page_source' capture
    result = smart_click(driver, "fake-button-id")
    
    if result:
        print("Test Passed: Interceptor caught the error and captured the DOM.")

finally:
    driver.quit()