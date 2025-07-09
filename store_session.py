from playwright.sync_api import sync_playwright

# def store_session():
with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        #go to login page
        page.goto("https://talent.woyage.ai/")
        
        page.locator("xpath=//input[@id='email']").fill("offshoreqa@woyage.ai")
        page.locator("xpath=//input[@id='password']").fill("Woyage!2")
        page.locator("xpath=//button[@type='submit']").click()
        
        page.wait_for_url("https://talent.woyage.ai/app/#interview")
        
        context.storage_state(path="auth.json")
        
        browser.close()
# store_session
        