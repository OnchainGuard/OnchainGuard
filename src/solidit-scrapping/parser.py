import time
import json
import logging
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Setting up basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Credentials for Solodit
EMAIL = "testingforever121@gmail.com"
PASSWORD = "ethglobalbrussels"

def parse_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        logging.info("JSON file successfully parsed.")
        return data
    except Exception as e:
        logging.error(f"Error parsing JSON file: {e}")
        return None

def find_all_links(data):
    all_links = []
    def traverse_items(items):
        for item in items:
            if item['referenceList']:
                all_links.extend(item['referenceList'])
            if 'childs' in item:
                traverse_items(item['childs'])
    traverse_items(data)
    logging.info(f"Total links found: {len(all_links)}")
    return all_links

def setup_driver():
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        logging.info("WebDriver setup successfully.")
        return driver
    except Exception as e:
        logging.error(f"Failed to set up WebDriver: {e}")
        return None

def login(driver):
    try:
        driver.get("https://solodit.xyz/auth?next=/login")
        wait = WebDriverWait(driver, 10)

        # Find and fill the email field
        email_field = wait.until(EC.presence_of_element_located((By.NAME, "email")))
        email_field.send_keys(EMAIL)

        # Find and fill the password field
        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys(PASSWORD)

        # Submit the form
        password_field.send_keys(Keys.RETURN)
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='dashboard']")))  # Adjust based on actual element after login
        
        logging.info("Logged in to Solodit successfully.")
    except Exception as e:
        logging.error(f"Login failed: {e}")
        driver.save_screenshot('login_failed.png')  # Save a screenshot for debugging

def save_as_text(driver, url, output_dir, index):
    if "solodit" in url:
        logging.info(f"Skipping Solodit URL: {url}")
        return
    
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        logging.info(f"URL loaded: {url}")
        text_path = f"{output_dir}/downloaded_content_{index}.txt"
        page_content = driver.find_element(By.TAG_NAME, "body").text
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(page_content)
        logging.info(f"Content saved to {text_path}")
    except Exception as e:
        logging.error(f"Failed to save content for URL {url}: {e}")
        driver.save_screenshot(f'error_{index}.png')  # Save a screenshot for debugging

def main():
    file_path = 'solodit_13-07-2024.txt'
    output_dir = 'audit-reports'
    
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logging.info(f"Created directory: {output_dir}")
    else:
        logging.info(f"Directory already exists: {output_dir}")

    data = parse_json_file(file_path)
    if data:
        all_links = find_all_links(data)
        driver = setup_driver()
        if driver:
            # Perform login
            login(driver)

            for index, link in enumerate(all_links):
                logging.info(f"Starting content generation for: {link}")
                save_as_text(driver, link, output_dir, index)
            driver.quit()
        else:
            logging.error("WebDriver was not initialized. Exiting.")
    else:
        logging.error("Failed to parse data. Exiting.")

if __name__ == "__main__":
    main()
