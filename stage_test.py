from pathlib import Path
import json
import os
import pdb
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

load_dotenv()


#path
session_token = Path(r"C:\Users\rajut\OneDrive\Desktop\Projectss\Playwright_Automation\STAGE_PRO\Session_Token_JSON\woyage_session.json")
download_path = Path(r"C:\Users\rajut\OneDrive\Desktop\Projectss\Playwright_Automation\STAGE_PRO\Download_Resumes")
pdf_path = Path(r"C:\Users\rajut\OneDrive\Desktop\Projectss\Playwright_Automation\STAGE_PRO\Parsing_Resumes\ALL_SECTIONS.pdf")

AUTH_USERNAME = os.getenv("USERNAME")
AUTH_PASSWORD = os.getenv("PASSWORD")
STAGE_EMAIL = os.getenv("EMAIL")
STAGE_PASSWORD = os.getenv("PASSWORDS")
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
        page.locator("xpath=//input[@id='email']").fill(STAGE_EMAIL)
        page.wait_for_timeout(1000)
        page.locator("xpath=//input[@id='password']").fill(STAGE_PASSWORD)
        page.wait_for_timeout(1000)
        page.locator("xpath=(//i[@class='-tw-ml-8 fa-regular tw-cursor-pointer fa-eye-slash'])[1]").click()
        page.wait_for_timeout(1000)
        page.locator("//button[@type='submit']").click()
        page.wait_for_timeout(1000)

        # Wait for navigation
        page.wait_for_url("https://stage.woyage.ai/app#interview", timeout=20000)

        # Save authenticated storage state
        context.storage_state(path=session_token)
        print("Session saved to",session_token )

        browser.close()

def read_session_token(): #This def is used to read the session token values from json file and print the session token in the terminal and it will be used to stay on the dashboard page

    with open(session_token, 'r') as file:
        data = json.load(file)

    # woyage_user_session_value = None

    for origin in data.get("origins"):
        for item in origin.get("localStorage"):
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
            viewport={"width": 1400, "height": 800},
            storage_state=session_token,
            http_credentials={
                "username": AUTH_USERNAME,
                "password": AUTH_PASSWORD
            },
            accept_downloads=True
        )

        page = context.new_page()
        page.goto("https://stage.woyage.ai/app#interview", timeout=60000)
        page.wait_for_timeout(2000)
        print("Landed on the dashboard page using stored session.")

        # Click to go to resume page
        page.locator("xpath=(//span[contains(@class,'resume-icon icon')])[1]").click(force=True)
        page.wait_for_url("https://stage.woyage.ai/app#resume")
        page.wait_for_timeout(1000)

        # Wait for resume gallery to be visible
        page.locator("xpath=//div[@class='saved-resume-gallery tw-w-full tw-relative tw-float-start tw-block tw-pb-1']").wait_for(state="visible")
        page.wait_for_timeout(500)

        #Download the saved resume from gallery
    #     with page.expect_download() as download_info:
    #         page.locator("//span[@class='overlay-download-icon tw-p-2 tw-w-9 tw-cursor-pointer overlay-download-icon-0']").click()

    #     download = download_info.value
    #     download_path.mkdir(parents=True, exist_ok=True)
    #     download.save_as(download_path / download.suggested_filename)
    #     print("Download saved as resume.pdf")
        
    #     #Parsing Feature and download the resume
    #     page.wait_for_timeout(1000)
    #     page.evaluate("window.scrollTo(0, 0)")
    #     page.locator("xpath=//label[@for='uploadFile1']").set_input_files(str(pdf_path))
    #     print("PDF Uploaded successfully")
    #     page.locator("//div[@class='parse-page-holder']").wait_for(state="visible")
    #     page.wait_for_url("https://stage.woyage.ai/app#resume")
    #     page.wait_for_timeout(1000)
    #     page.locator("xpath=//div[@class='content-wrapper md:tw-min-w-[1100px] tw-w-full md:tw-w-9/12']").wait_for(state="visible")
    #     page.locator("xpath=//img[@alt='ats-template-4']").click(force=True)
    #     page.wait_for_timeout(500)
    #     page.wait_for_url("https://stage.woyage.ai/app#edit")
    #     page.wait_for_timeout(1000)
        
    #     #resume name 
    #     # page.locator("xpath=//div[@class='resume-loader']").scroll_into_view_if_needed()
    #     page.wait_for_timeout(1000)
    #     page.locator("xpath=//div[@class='resume-loader']").wait_for(state="hidden")
    #     page.wait_for_timeout(5000)
    #     print("parsing is hidded")
    #     Resume_name = page.locator("xpath=//div[@class='edit-resume-name resume-name   tw-border-b-2 tw-pl-2']")
    #     Resume_name.click(force=True)
    #     Resume_name.fill("Parsing Resume")
    #     print("Success for edit the resume name")
        
    #     #Click finalize button
    #     page.wait_for_timeout(2000)
    #     page.locator("xpath=//i[@class='fa-solid fa-file tw-text-lg  tw-px-2']").click(force=True)
    #     print("Pro clicked the finalize button")
    #     page.wait_for_timeout(3000)
    #     page.locator("xpath=(//div[@class='loader'])[2]").wait_for(state="hidden")
    #     page.wait_for_timeout(1000)
        
    #     #download the parsed resume
    # with page.expect_download() as download_info:
    #     page.locator("xpath=(//img[contains(@alt,'Download Resume')])[1]").click(force=True)
    #     print("Pro clicked the download")
    #     download = download_info.value
    #     download_path.mkdir(parents=True, exist_ok=True)
    #     download.save_as(download_path / download.suggested_filename)
    #     page.wait_for_timeout(500)
    #     page.locator("xpath=//div[@class='overlay-loader-icon preview-overlay-loader']").wait_for(state="hidden")
    #     page.wait_for_timeout(1000)
    #     print("Download saved as resume.pdf")
        
    #     #navigate to #resume page
    #     page.locator("xpath=(//span[@class='resume-icon icon'])[1]").click(force=True)
    #     page.wait_for_url("https://stage.woyage.ai/app#edit")
    #     page.wait_for_timeout(1000)
    #     print("successfully landed in resume page")
    
        #PRO Create a New resume
        # page.locator("xpath=//label[normalize-space()='Create a new Resume']").click(force=True)
        # page.wait_for_url("https://stage.woyage.ai/app#templates")
        # page.locator("xpath=(//div[contains(@class,'row')])[2]").wait_for(state="visible")
        # page.wait_for_timeout(1000)
        # page.locator("xpath=//img[@alt='ats-template-3']").click(force=True)
        # page.locator("xpath=(//div[@class='loader'])[1]").wait_for(state="hidden")
        # page.wait_for_url("https://stage.woyage.ai/app#edit")
        
        #Pro select the saved resumes
        page.locator("xpath=(//div[@class='image-wrapper tw-relative  '])[1]").click(force=True)
        page.wait_for_url("https://stage.woyage.ai/app#edit")
        page.wait_for_timeout(2000)
        #edit resume name
        # Resumes_name = page.locator("xpath=//div[@class='edit-resume-name resume-name   tw-border-b-2 tw-pl-2']")
        # Resumes_name.wait_for(state="visible", timeout=2000)  # Wait up to 10s
        # Resumes_name.click(force=True)
        # Resumes_name.fill("Parsing Resume")
        Resumes_na = page.locator("xpath=//div[contains(@class, 'edit-resume-name') and contains(@class, 'resume-name')]")
        Resumes_na.click(force=True)
        Resumes_na.evaluate("el => el.textContent = ''")  # Clear old text
        Resumes_na.type("Resume edit testing")
        page.wait_for_timeout(5000)
        page.locator("xpath=//p[normalize-space()='introduction']").click()
        print("Pro click the introduction")
        
        #Resume content edit
        first_name=page.locator("xpath=//div[@data-section-element='firstname']")
        first_name.evaluate("el => el.innerHTML = ''")
        first_name.type("QATEST")
        page.wait_for_timeout(5000)
        
        page.locator("xpath=//span[@class='resume-icon icon']").click(force=True)
        page.wait_for_timeout(5000)
        page.wait_for_url("https://stage.woyage.ai/app#resume")
        page.wait_for_timeout(2000)
        browser.close()
        
        
        
        
        
        

# if __name__ == "__main__":
# run()
read_session_token()
stay_on_dashboard_page()