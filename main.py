import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from tempfile import mkdtemp


def lambda_handler(event, context):
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-tools")
    chrome_options.add_argument("--no-zygote")
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument(f"--user-data-dir={mkdtemp()}")
    chrome_options.add_argument(f"--data-path={mkdtemp()}")
    chrome_options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    chrome_options.add_argument("--remote-debugging-pipe")
    chrome_options.add_argument("--verbose")
    chrome_options.add_argument("--log-path=/tmp")
    chrome_options.binary_location = "/opt/chrome/chrome-linux64/chrome"

    service = Service(
        executable_path="/opt/chrome-driver/chromedriver-linux64/chromedriver",
        service_log_path="/tmp/chromedriver.log"
    )

    driver = webdriver.Chrome(
        service=service,
        options=chrome_options
    )

    try:
        print("Open a website\n")
        driver.get("https://www.wuxiaworld.com/")
        
        print("Set explicit wait\n")
        # Set explicit wait
        wait = WebDriverWait(driver, 10)
        actions = ActionChains(driver)

        # Wait for and click the first button
        print("Wait for and click the first button\n")
        button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="header"]/div/div/div[2]/button')))
        actions.move_to_element(button).click().perform()

        # Wait for and click the second button
        print("Wait for and click the second button\n")
        button2 = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "LOG IN")]')))
        driver.execute_script("arguments[0].click();", button2)

        # Input username
        print("Input username\n")
        username = os.getenv('USERNAME')
        input_user = wait.until(EC.presence_of_element_located((By.NAME, "Username")))
        input_user.send_keys(username)

        # Input password
        print("Input password\n")
        password = os.getenv('PASSWORD')
        input_PASS = wait.until(EC.presence_of_element_located((By.NAME, "Password")))
        input_PASS.send_keys(password)
        time.sleep(1)
        
        # Click the login button
        print("Click login\n")
        button3 = wait.until(EC.element_to_be_clickable((By.NAME, "button")))
        driver.execute_script("arguments[0].click();", button3)

        time.sleep(3)

        # Click the next button
        print("Diamond button\n")
        while True:
            try:
                fourth_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".MuiButtonBase-root.MuiIconButton-root.MuiIconButton-sizeMedium")))
                driver.execute_script("arguments[0].click();", fourth_button)
                break
            except StaleElementReferenceException:
                print("Encountered stale element, retrying...\n")

        time.sleep(2)

        # Click the popup button
        print("Collecting karma\n")
        while True:
            try:
                popup_button = driver.find_element(By.XPATH, '//button[contains(text(), "COMPLETE")]')
                driver.execute_script("arguments[0].click();", popup_button)
                print("Just clicked COMPLETE, status is now COMPLETED")
                break
            except StaleElementReferenceException:
                print("Encountered stale element, retrying...\n")
            except:
                print("Status is COMPLETED.\n")
                break

        time.sleep(1)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if driver:
            # Quit the browser
            driver.quit()
    return {
        'statusCode': 200,
        'body': "Success"
    }
    
    