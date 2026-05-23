import pytest
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page


BASE_URL = "https://www.saucedemo.com"


@pytest.fixture(scope="session")
def browser():
    """Launch browser once for the entire test session."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=800)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def context(browser: Browser):
    """Fresh browser context for each test (clean cookies/storage)."""
    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
        record_video_dir="reports/videos/"
    )
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext):
    """Fresh page for each test."""
    page = context.new_page()
    page.goto(BASE_URL)
    yield page
    page.close()


@pytest.fixture(scope="function")
def logged_in_page(page: Page):
    """Page fixture that starts already logged in as standard user."""
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    page.wait_for_url("**/inventory.html")
    yield page