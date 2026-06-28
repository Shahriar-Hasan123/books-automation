import pytest
from playwright.sync_api import sync_playwright, Page, Browser


BASE_URL = "https://books.toscrape.com/index.html"


@pytest.fixture(scope="session")
def browser_instance():
    """Launch a single browser for the entire test session."""
    with sync_playwright() as playwright:
        browser: Browser = playwright.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser_instance: Browser) -> Page:
    """Create a fresh browser page (tab) for each test function."""
    context = browser_instance.new_context()
    page: Page = context.new_page()
    page.goto(BASE_URL)
    yield page
    context.close()
