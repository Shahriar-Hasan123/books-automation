import os
import pytest
from playwright.sync_api import sync_playwright, Page, Browser


BASE_URL = "https://books.toscrape.com/index.html"
SCREENSHOTS_DIR = "screenshots"


@pytest.fixture(scope="session")
def browser_instance():
    """Launch a single browser for the entire test session."""
    with sync_playwright() as playwright:
        browser: Browser = playwright.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser_instance: Browser) -> Page:
    """
    Create a fresh browser page (tab) for each test function.
    Overrides pytest-playwright's default page fixture to use
    our session-scoped browser instance for performance.
    """
    context = browser_instance.new_context(
        # explicitly ignore HTTPS errors for test site
        ignore_https_errors=True
    )
    page: Page = context.new_page()
    page.goto(BASE_URL)
    yield page
    context.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook that runs after each test.
    Captures a screenshot automatically if a test fails.
    Attaches screenshot to both HTML report and Allure report.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
            safe_name = item.nodeid.replace("/", "_").replace("::", "_")
            screenshot_path = f"{SCREENSHOTS_DIR}/{safe_name}.png"
            page.screenshot(path=screenshot_path)

            pytest_html = item.config.pluginmanager.getplugin("html")
            if pytest_html:
                extra = getattr(report, "extra", [])
                extra.append(pytest_html.extras.image(screenshot_path))
                report.extra = extra