import requests
import json, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
import pytz
import dotenv
import os


# Load environment variables
dotenv.load_dotenv()

# Environment variables for AWS
USER_NAME = os.getenv("USER_NAME", "")
USER_PASS = os.getenv("USER_PASS", "")

def drive_download():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ensure GUI is off
    chrome_options.add_argument("--window-size=1920,1080")  # Set a window size
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # Initialize the Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        driver.get('https://app.textel.net/login')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'input-15')))
        username_field = driver.find_element(By.ID, 'input-15')
        password_field = driver.find_element(By.ID, 'input-18')
        submit_button = driver.find_element(By.XPATH, '//button[@type="button"]')

        username_field.send_keys(USER_NAME)
        password_field.send_keys(USER_PASS)
        submit_button.click()
        # After submitting the login form
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1.view-title.text-h1"))
        )
        driver.get("https://app.textel.net/reporting/history")
        # Open the website
        button_class_name = 'uniform-button.v-btn.v-btn--is-elevated.v-btn--has-bg.theme--light.v-size--small.primary'
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, button_class_name))
        )
        button.click()
        time.sleep(2)
    except Exception as e:
        print(e)

def convert_to_utc(dt):
    # Convert datetime to UTC timezone
    utc_timezone = pytz.utc
    dt_utc = dt.astimezone(utc_timezone)
    return dt_utc

def authenticate_and_get_token():
    auth_url = 'https://foundation.textel.net/clientapi/v1/auth/authenticate'
    auth_data = {
        "email": USER_NAME,
        "password": USER_PASS
    }
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(auth_url, headers=headers, data=json.dumps(auth_data), verify=False)
        if response.status_code == 200:
            token = response.json().get('accessToken')
            print("Authentication successful. Token obtained.")
            return token
        else:
            print("Failed to authenticate.")
            print(f"Status Code: {response.status_code}")
            return None
    except Exception as e:
        print("An error occurred during authentication:", e)
        return None

def create_report(token):
    # Define the PST timezone
    pst_timezone = pytz.timezone('America/Los_Angeles')
    now_pst = datetime.now(pst_timezone)
    print(now_pst)
    # Calculate the start and end dates for the day before, with time set to 9:00 AM PST
    end_date = now_pst.replace(hour=9, minute=0, second=0, microsecond=0) - timedelta(days=1)
    start_date = end_date - timedelta(days=1)

    # Convert start and end dates to UTC
    start_date_utc = convert_to_utc(start_date)
    end_date_utc = convert_to_utc(end_date)

    # Format the dates as strings in the required format
    start_date_str = start_date_utc.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    end_date_str = end_date_utc.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    
    url = 'https://foundation.textel.net/clientapi/v1/report/detail-report'
    data = {
        "StartDate": start_date_str,
        "EndDate": end_date_str,
        "ReportType": 2,
        "LineIds": []
    }    
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Authorization': f'Bearer {token}',
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            print("Report creation initiated successfully.")
            report_id = response.json().get('reportId')
            print(f"Report ID: {report_id}")
        else:
            print("Failed to initiate report creation.")
            print(f"Status Code: {response.status_code}")
            return None
    except Exception as e:
        print("An error occurred during report creation:", e)
        return None

# Main execution flow
token = authenticate_and_get_token()
if token:
    create_report(token)
    drive_download()
else:
    print("Could not obtain token. Process aborted.")
