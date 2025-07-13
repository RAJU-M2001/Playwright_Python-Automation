from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import os
from pathlib import Path
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

# Paths to JSON files
CONTENT_JSON_PATH = Path(r"C:\Users\rajut\OneDrive\Desktop\Projectss\Playwright_Automation\STAGE_PRO\Content_Json\28section_content.json")
SESSION_TOKEN_PATH = Path(r"C:\Users\rajut\OneDrive\Desktop\Projectss\Playwright_Automation\STAGE_PRO\Session_Token_JSON\woyage_session.json")

# Constants
AUTH_USERNAME = os.getenv("USERNAME")
AUTH_PASSWORD = os.getenv("PASSWORD")

# Load resume data
with CONTENT_JSON_PATH.open("r", encoding="utf-8") as file:
    resume_data = json.load(file)

skills_data = resume_data.get("skills", {}).get("items", [])

# Utility function
def clear_and_type(page, selector, value):
    element = page.locator(selector)
    element.click()
    element.fill("")  # Clears the input field properly
    page.wait_for_timeout(300)
    element.type(value or "")
    page.wait_for_timeout(300)

# Section filling functions
def fill_introduction_section(page, data):
    page.locator("xpath=//p[normalize-space()='introduction']").click()
    clear_and_type(page, "xpath=//div[@data-section-element='firstname']", data.get("first_name", ""))
    clear_and_type(page, "xpath=//div[@data-section-element='lastname']", data.get("last_name", ""))
    clear_and_type(page, "xpath=//div[@data-section-element='title']", data.get("title", ""))
    clear_and_type(page, "xpath=//div[@data-section-element='tagline']", data.get("tagline", ""))
    page.locator("xpath=//span[@class='edit-custom-label tw-cursor-pointer']").click(force=True)
    clear_and_type(page, "xpath=//div[contains(@class, 'edit-custom-field')]", str(data.get("custom_field", [])))
    print("Introducation field success")

def fill_contact_section(page, data):
    page.locator("xpath=//p[normalize-space()='contact']").click()
    clear_and_type(page, "xpath=//div[@id='address']", data.get("address_line", ""))
    clear_and_type(page, "xpath=//div[@id='city']", data.get("address_city", ""))
    clear_and_type(page, "xpath=//div[@id='state']", data.get("address_state", ""))
    clear_and_type(page, "xpath=//div[@id='country']", data.get("address_country", ""))
    clear_and_type(page, "xpath=//div[@id='email']", data.get("email", ""))
    clear_and_type(page, "xpath=//div[@id='phone']", data.get("phone", ""))
    clear_and_type(page, "xpath=//div[@id='linkedin']", data.get("linkedin", ""))
    clear_and_type(page, "xpath=//div[@id='pronoun']", data.get("pronouns", ""))
    clear_and_type(page, "xpath=//div[@id='pincode']", data.get("address_zipcode", ""))
    clear_and_type(page, "xpath=//div[@id='work-authorization']", data.get("work_authorization", ""))
    clear_and_type(page, "xpath=//div[@id='website']", data.get("website", ""))
    page.locator("xpath=//span[@class='edit-custom-label tw-cursor-pointer']").click(force=True)
    clear_and_type(page, "xpath=//div[contains(@class, 'edit-custom-field')]", str(data.get("custom_field", [])))
    print("contact field success")

def fill_summary_section(page, data):
    page.locator("xpath=//p[normalize-space()='summary']").click()
    clear_and_type(page, "xpath=(//div[@id='summary-description'])[1]", data.get("description", ""))
    page.locator("xpath=(//p[@class='tw-flex tw-m-0 tw-justify-center tw-items-center '])[1]").click(force=True)
    page.locator("xpath=//p[@class='tw-flex tw-m-0 tw-justify-center tw-items-center tw-pe-4']").wait_for(state="hidden", timeout=10000)
    page.locator("xpath=(//p[normalize-space()='Apply'])[1]").click(force=True)
    page.wait_for_timeout(1000)
    print("summary field success")
    
def clear_existing_skills(page):
    while True:
        delete_button = page.locator("span[data-index='0']")
        count = delete_button.count()
        if count == 0:
            break
        delete_button.click()
        page.wait_for_timeout(500)
        
def fill_skill_section(page, skills_data):
    page.locator("xpath=(//p[normalize-space()='skills'])[1]").click()
    clear_existing_skills(page)  # Clear all existing skills before adding new ones

    for skill in skills_data:
        skill_name = skill.get("name", "").strip()
        if not skill_name:
            continue
        clear_and_type(page, "xpath=(//input[contains(@placeholder,'Enter to Add Skills')])[1]", skill_name)
        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)
        print("Skill field success")
        

    
def fill_education_section(page, data):
    # Click on the Education section
    page.locator("xpath=(//p[normalize-space()='education'])[1]").click()
    page.wait_for_timeout(1000)
    # Extract the first education entry
    education_items = data.get("items")
    if not education_items:
        return
    edu = education_items[0]

    # Fill in each field
    clear_and_type(page, "xpath=(//div[contains(@class,'edit-degree education_0_degree')])[1]", edu.get("degree", ""))
    clear_and_type(page, "xpath=(//div[contains(@class,'edit-school education_0_school')])[1]", edu.get("school", ""))
    clear_and_type(page, "xpath=(//div[contains(@class,'edit-field-of-study education_0_field_of_study')])[1]", edu.get("field_of_study", ""))
    clear_and_type(page, "xpath=(//div[contains(@class,'edit-description education_0_description')])[1]", edu.get("description", ""))
    clear_and_type(page, "xpath=(//div[contains(@class,'edit-grade education_0_grade')])[1]", edu.get("grade", ""))
    clear_and_type(page, "xpath=(//div[contains(@class,'edit-city education_0_city')])[1]", edu.get("city", ""))
    clear_and_type(page, "xpath=(//div[contains(@class,'edit-state education_0_state')])[1]", edu.get("state", ""))
    clear_and_type(page, "xpath=(//div[contains(@class,'edit-country education_0_country')])[1]", edu.get("country", ""))
    clear_and_type(page, "xpath=(//input[contains(@type,'text')])[1]", edu.get("start_month", ""))
    clear_and_type(page, "xpath=(//input[contains(@type,'text')])[2]", edu.get("start_year", ""))
    clear_and_type(page, "xpath=(//input[contains(@type,'text')])[3]", edu.get("end_month", ""))
    clear_and_type(page, "xpath=(//input[contains(@type,'text')])[4]", edu.get("end_year", ""))
    page.wait_for_timeout(5000)

        
# Main automation function
def stay_on_dashboard_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={"width": 1400, "height": 800},
            storage_state=SESSION_TOKEN_PATH,
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

            # Navigate to Resume page
        page.locator("xpath=(//span[contains(@class,'resume-icon icon')])[1]").click(force=True)
        page.wait_for_url("https://stage.woyage.ai/app#resume", timeout=10000)
        page.wait_for_timeout(1000)
        page.locator("xpath=(//div[contains(@class,'image-wrapper')])[1]").click(force=True)
        page.wait_for_url("https://stage.woyage.ai/app#edit", timeout=10000)
        page.locator("xpath=//div[contains(@class,'edit-page-loader')]").wait_for(state="hidden", timeout=10000)

        # Edit resume name
        resume_name_elem = page.locator("xpath=//div[contains(@class, 'edit-resume-name') and contains(@class, 'resume-name')]")
        resume_name_elem.click(force=True)
        resume_name_elem.evaluate("el => el.textContent = ''")
        resume_name_elem.type("Resume edit testing")

        # Fill resume sections
        # fill_introduction_section(page, resume_data.get("introduction", {}))
        # fill_contact_section(page, resume_data.get("contact", {}))
        # fill_summary_section(page, resume_data.get("summary", {}))
        # fill_skill_section(page, skills_data)
        # fill_experience_section(page, resume_data.get("experience", {}) )
        fill_education_section(page, resume_data.get("education",{}))
        


        print("Success")
        browser.close()
        
if __name__ == "__main__":
    stay_on_dashboard_page()
