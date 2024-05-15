from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")


try:
    driver = webdriver.Chrome(options=chrome_options)

    # Open a website
    driver.get("https://www.wuxiaworld.com/")

    # Set implicit wait time
    driver.implicitly_wait(1)  # Wait for up to 10 seconds for elements to be found

    # Find the button by its class name and click it
    button = driver.find_element(By.CLASS_NAME, "MuiButtonBase-root")
    button.click()

    driver.implicitly_wait(10)
    button2 = driver.find_element(By.CLASS_NAME, "MuiGrid-root")
    button2.click() 

    input_user = driver.find_element(By.NAME, "Username")
    input_user.send_keys("email" )

    input_PASS = driver.find_element(By.NAME, "Password")
    input_PASS.send_keys("password")

    button3 = driver.find_element(By.NAME, "button")
    # Click the button
    button3.click()

    time.sleep(1)

    button4 = driver.find_element(By.CSS_SELECTOR, ".MuiButtonBase-root.MuiIconButton-root.MuiIconButton-sizeMedium")
    button4.click() 
    
    time.sleep(1)

    popup_button = driver.find_element(By.XPATH, '//button[contains(text(), "COMPLETE")]')
    popup_button.click()

    time.sleep(2)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    if driver:
        # Quit the browser
        driver.quit()

