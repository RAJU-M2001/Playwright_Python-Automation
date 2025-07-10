from dotenv import load_dotenv
import json
import os
from playwright.sync_api import sync_playwright


load_dotenv()
AUTH_USERNAME = os.getenv("USERNAME")
AUTH_PASSWORD = os.getenv("PASSWORD")

STORAGE_FILE = "woyage_session.json"

def run():#This def is used to unlock the bowser auth and launch the stage url and login to store the session token in the local is named woyage_session.json file
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        # HTTP Basic Auth context
        context = browser.new_context(
            http_credentials={
                "username": AUTH_USERNAME,
                "password": AUTH_PASSWORD
            }
        )

        # Login page
        page = context.new_page()
        page.goto("https://stage.woyage.ai/", timeout=60000)
        page.wait_for_timeout(5000)

        # Login steps
        page.locator("xpath=//input[@id='email']").fill("offshoreqa@woyage.ai")
        page.wait_for_timeout(1000)
        page.locator("xpath=//input[@id='password']").fill("Woyage!1")
        page.wait_for_timeout(1000)
        page.locator("xpath=(//i[@class='-tw-ml-8 fa-regular tw-cursor-pointer fa-eye-slash'])[1]").click()
        page.wait_for_timeout(1000)
        page.locator("//button[@type='submit']").click()
        page.wait_for_timeout(1000)

        # Wait for navigation
        page.wait_for_url("https://stage.woyage.ai/app#interview", timeout=20000)

        # Save authenticated storage state
        context.storage_state(path=STORAGE_FILE)
        print("Session saved to", STORAGE_FILE)

        browser.close()

def read_session_token(): #This def is used to read the session token values from json file and print the session token in the terminal and it will be used to stay on the dashboard page
    
    with open(STORAGE_FILE, 'r') as file:
        data = json.load(file)

    # woyage_user_session_value = None

    for origin in data.get("origins", []):
        for item in origin.get("localStorage", []):
            if item.get("name") == "woyage_user_session":
                woyage_user_session_value = item.get("value")
                break
        if woyage_user_session_value:
            break

    print("woyage_user_session value:", woyage_user_session_value)
    return woyage_user_session_value

def stay_on_dashboard_page(): #This def is working for an directly launch the dashboard page using the session token value to test the updated scripts 
    """Launches the dashboard using the stored session"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        context = browser.new_context(
            viewport={"width":1400,"height":800},
            storage_state=STORAGE_FILE,
            http_credentials={
                "username": AUTH_USERNAME,
                "password": AUTH_PASSWORD
            }
        )

        page = context.new_page()
        page.goto("https://stage.woyage.ai/app#interview", timeout=60000)
        page.wait_for_timeout(5000)
        print("Landed on the dashboard page using stored session.")
        

if __name__ == "__main__":
    # run()
    # read_session_token()
    stay_on_dashboard_page()