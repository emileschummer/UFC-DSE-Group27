from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def CallChatGPT(request):
    # Initialize the WebDriver (replace with your WebDriver path)
    driver = webdriver.Chrome(executable_path="C:\Program Files\Google\Chrome\Application\chrome.exe")
    
    try:
        # Open ChatGPT
        driver.get("https://chatgpt.com/?model=gpt-4o")
        
        # Wait for the page to load (you may need to manually log in the first time)
        time.sleep(5)  # Adjust as needed
        
        # Find the input box (ChatGPT's textarea has a specific ID or class)
        # Note: The selector may change if ChatGPT updates their UI
        input_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "textarea#prompt-textarea"))
        )
        
        # Enter the request and submit
        input_box.send_keys(request)
        input_box.send_keys(Keys.RETURN)
        
        print("Request submitted to ChatGPT.")
        
        # Keep the browser open for a while to see the result
        time.sleep(10)
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the browser
        driver.quit()

# Example usage
CallChatGPT("Please recommend things to do on holiday in South Africa")