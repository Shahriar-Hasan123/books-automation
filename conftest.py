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
    """Create a fresh browser page (tab) for each test function."""
    context = browser_instance.new_context()
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

    # only capture on actual test failure (not setup/teardown)
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            # create screenshots folder if it doesn't exist
            os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

            # safe filename from test name
            safe_name = item.nodeid.replace("/", "_").replace("::", "_")
            screenshot_path = f"{SCREENSHOTS_DIR}/{safe_name}.png"

            # save screenshot
            page.screenshot(path=screenshot_path)

            # attach to HTML report
            pytest_html = item.config.pluginmanager.getplugin("html")
            if pytest_html:
                extra = getattr(report, "extra", [])
                extra.append(pytest_html.extras.image(screenshot_path))
                report.extra = extra