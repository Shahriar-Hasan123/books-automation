import os
import pytest
from playwright.sync_api import sync_playwright, Page, Browser


BASE_URL = "https://books.toscrape.com/index.html"
SCREENSHOTS_DIR = "screenshots"
VIDEOS_DIR = "videos"
TRACES_DIR = "traces"


@pytest.fixture(scope="session")
def browser_instance():
    """Launch a single browser for the entire test session."""
    with sync_playwright() as playwright:
        browser: Browser = playwright.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser_instance: Browser, request) -> Page:
    """
    Create a fresh browser page (tab) for each test function.
    Records video for every test (PASS and FAIL).
    Records trace for every test (PASS and FAIL).
    Takes screenshot for every test (PASS and FAIL).
    """
    # create output folders
    os.makedirs(VIDEOS_DIR, exist_ok=True)
    os.makedirs(TRACES_DIR, exist_ok=True)
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

    # safe test name for filenames
    safe_name = request.node.nodeid.replace("/", "_").replace("::", "_")

    # create context with video recording
    context = browser_instance.new_context(
        ignore_https_errors=True,
        record_video_dir=VIDEOS_DIR,
        record_video_size={"width": 1280, "height": 720}
    )

    # start tracing for every test
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    page: Page = context.new_page()
    page.goto(BASE_URL)

    yield page

    # --- teardown: runs after every test regardless of result ---

    # get test result (PASS or FAIL)
    test_failed = (
        request.node.rep_call.failed
        if hasattr(request.node, "rep_call")
        else False
    )
    status = "FAIL" if test_failed else "PASS"

    # take screenshot for every test
    screenshot_path = f"{SCREENSHOTS_DIR}/{status}_{safe_name}.png"
    page.screenshot(path=screenshot_path)

    # save trace for every test
    trace_path = f"{TRACES_DIR}/{status}_{safe_name}.zip"
    context.tracing.stop(path=trace_path)

    # close context — finalizes video
    context.close()

    # rename video to meaningful name with PASS/FAIL prefix
    video_path = page.video.path() if page.video else None
    if video_path and os.path.exists(video_path):
        new_video_path = f"{VIDEOS_DIR}/{status}_{safe_name}.webm"
        os.rename(video_path, new_video_path)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook that runs after each test.
    Stores test result on the node so the page fixture teardown can read it.
    Attaches screenshot to HTML report on failure.
    """
    outcome = yield
    report = outcome.get_result()

    # store result on node so page fixture can read pass/fail status
    if report.when == "call":
        item.rep_call = report

    # attach screenshot to HTML report on failure
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            safe_name = item.nodeid.replace("/", "_").replace("::", "_")
            screenshot_path = f"{SCREENSHOTS_DIR}/FAIL_{safe_name}.png"

            # attach to HTML report
            pytest_html = item.config.pluginmanager.getplugin("html")
            if pytest_html:
                extra = getattr(report, "extra", [])
                extra.append(pytest_html.extras.image(screenshot_path))
                report.extra = extra