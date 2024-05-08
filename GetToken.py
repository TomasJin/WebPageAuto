import time
import json
import random
import string
import os
import pickle
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from selenium.webdriver.chrome.service import Service
# from bs4 import BeautifulSoup
import base64
import re

fakeaddress=''
def getfakeaddress(email):
    url = "https://api.products.aspose.app/email/api/FakeEmail/Generate"
    payload = {"email": email}
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }
    response = requests.post(url, data=payload, headers=headers)
    print(response.json())
    try:
        response_data = response.json()
        generated_address = response_data.get('generatedAddress')
        if generated_address:
            return generated_address
        else:
            print("No 'generatedAddress' found in the JSON response:", response_data)
            return None
    except ValueError:
        print("Invalid JSON response:", response.text)
        return None


def data_load():
    with open('data.json') as file:
        data = json.load(file)
    return data


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


# Set proxy environment variables

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def getmail():
    # data=data_load()
    # proxy_host = data['proxy_host']
    # proxy_port = data['proxy_port']
    creds = None
    # The file token.json stores the user's access and refresh tokens and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Set proxy for the authentication flow
            # os.environ['HTTP_PROXY'] = f'http://{proxy_host}:{proxy_port}'
            # os.environ['HTTPS_PROXY'] = f'http://{proxy_host}:{proxy_port}'

            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Set proxy for the Gmail API service
        # os.environ['HTTP_PROXY'] = f'http://{proxy_host}:{proxy_port}'
        # os.environ['HTTPS_PROXY'] = f'http://{proxy_host}:{proxy_port}'

        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().messages().list(userId='me', q='subject:"Verify your email address" to:' + fakeaddress, maxResults=10).execute()
        if 'messages' in results:
            first_message = results['messages'][0]
            message_id = first_message['id']
            message = service.users().messages().get(userId='me', id=message_id).execute()

            # Extract the raw HTML content from the message
            payload = message['payload']

            # Iterate over the parts of the payload
            for part in payload['parts']:
                # Check if the part is of type 'text/html'
                if part['mimeType'] == 'text/html':
                    # Extract the data from the part
                    data = part['body']['data']
                    # Decode the data from base64
                    decoded_data = base64.urlsafe_b64decode(data).decode('utf-8')

                    # Use regular expressions to find the verification link
                    match = re.search(r'href="(https://www.upwork.com/nx/signup/verify-email/.*?)"', decoded_data)
                    if match:
                        verification_link = match.group(1)
                        break

            # Print the verification link
            print(verification_link)

    except HttpError as error:
        # TODO(developer) - Handle errors from Gmail API.
        print(f'An error occurred: {error}')

    return verification_link


def OpenChrome(data):
    # data = data_load()
    # proxy_host = data['proxy_host']
    # proxy_port = data['proxy_port']
    # # Set Chrome options
    # options = Options()
    # options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
    # # options.add_argument(f"--proxy-server=http://{proxy_host}:{proxy_port}")
    # # options.add_argument("--user-data-dir=C:/Users/Administrator/AppData/Local/Google/Chrome/User Data")
    # # options.add_argument("--executable-path=C:/program files/google/chrome/application/chromedriver.exe")
    # # options.add_argument('--profile-directory=Profile 3')
    # options.binary_location = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
    # # options.add_argument("--no-sandbox")
    # # options.add_argument("--disable-dev-shm-usage")
    # # options.add_argument("--remote-debugging-port=9222");
    # # options.add_argument('--headless')
    # service = Service("/chromedriver.exe")
    # driver = webdriver.Chrome(service = service, options=options)
    # driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    #     "source": """
    #         Object.defineProperty(navigator, 'webdriver', {
    #             get: () => undefined
    #         });
    #         Object.defineProperty(navigator, 'driver', {
    #             get: () => undefined
    #         });
    #         Object.defineProperty(window, 'webdriver', {
    #             get: () => undefined
    #         });
    #         Object.defineProperty(window, 'driver', {
    #             get: () => undefined
    #         });
    #     """
    # })
    #
    # First_Name = data["First_Name"]
    # Last_Name = data["Last_Name"]
    # Email_Address = data["Email_Address"]
    # password = data["password"]
    # country = data["country"]
    # letters = string.ascii_lowercase
    # numbers = string.digits
    # fakeaddress = getfakeaddress(data['Email_Address'])
    # # fakeaddress = "38h68efyv@steven3197.anonaddy.com"
    # # Launch Chrome with the specified options
    # # driver.maximize_window()
    # driver.get("https://www.upwork.com/nx/signup/?dest=home")
    # driver.find_element(By.CSS_SELECTOR, 'div[data-cy="button-box"][data-qa="work"]').click()
    # time.sleep(1)
    # driver.find_element(By.CSS_SELECTOR, 'button[data-qa="btn-apply"][type="button"]').click()
    # time.sleep(1)
    # driver.find_element(By.ID, 'first-name-input').send_keys(First_Name)
    # time.sleep(1)
    # driver.find_element(By.ID, 'last-name-input').send_keys(Last_Name)
    # time.sleep(1)
    # driver.find_element(By.ID, 'redesigned-input-email').send_keys(fakeaddress)
    # time.sleep(3)
    # driver.find_element(By.ID, 'password-input').send_keys(password)
    # time.sleep(1)
    # # driver.find_element(By.CSS_SELECTOR, 'div.up-dropdown-toggle-title').click()
    # # time.sleep(2000)
    # # driver.find_element(By.CSS_SELECTOR, 'div.up-dropdown-menu-container').find_element(By.CSS_SELECTOR, 'input').send_keys(country)
    # # time.sleep(100)
    # # driver.find_element(By.CSS_SELECTOR, 'li[role="option"]').click()
    # # driver.find_element(By.CSS_SELECTOR, 'div[data-v-e3ce8d86][class="up-checkbox"]').click()
    # # time.sleep(1)
    # # driver.find_element(By.ID, 'button-submit-form').click()
    # driver.find_element(By.ID, 'button-submit-form').click()
    # time.sleep(5)
    verification_link = getmail()
    time.sleep(10)
    driver.get(verification_link)
    time.sleep(200)


if __name__ == "__main__":
    data=data_load()
    OpenChrome(data)
    # fakeaddress = getfakeaddress(data['Email_Address'])