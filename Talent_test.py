from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser =p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://talent.woyage.ai/")
    page.wait_for_timeout(5000)
    browser.close()
    