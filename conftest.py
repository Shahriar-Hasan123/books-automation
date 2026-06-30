import os
import re
import pytest
import allure
from playwright.sync_api import sync_playwright, Page, Browser


BASE_URL = "https://books.toscrape.com/index.html"
SCREENSHOTS_DIR = "screenshots"
VIDEOS_DIR = "videos"
TRACES_DIR = "traces"


def make_safe_filename(name: str) -> str:
    """
    Convert a test node ID into a filesystem-safe and
    GitHub Actions artifact-safe filename.
    Removes all characters invalid on Windows/NTFS and GitHub Actions uploads.
    """
    name = name.replace("/", "_").replace("::", "_")
    name = re.sub(r'[":<>|*?\r\n]', "_", name)
    name = re.sub(r'_+', "_", name)
    return name


@pytest.fixture(scope="session")
def browser_instance():
    """Launch the browser for the test session."""
    with sync_playwright() as playwright:
        browser: Browser = playwright.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser_instance: Browser, request) -> Page:
    """Create a fresh browser page and capture test evidence."""
    # create output folders
    os.makedirs(VIDEOS_DIR, exist_ok=True)
    os.makedirs(TRACES_DIR, exist_ok=True)
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

    # safe test name for filenames
    safe_name = make_safe_filename(request.node.nodeid)

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

    # Take initial screenshot at test start (homepage baseline)
    initial_screenshot_path = f"{SCREENSHOTS_DIR}/INIT_{safe_name}.png"
    page.screenshot(path=initial_screenshot_path)

    # Attach initial screenshot to Allure
    with open(initial_screenshot_path, "rb") as image:
        allure.attach(
            image.read(),
            name="initial_state",
            attachment_type=allure.attachment_type.PNG
        )

    yield page

    # --- teardown: runs after every test regardless of result ---

    # get test result (PASS or FAIL) from pytest hook
    test_failed = (
        request.node.rep_call.failed
        if hasattr(request.node, "rep_call")
        else False
    )
    status = "FAIL" if test_failed else "PASS"

    # Only take failure screenshot if test failed
    if test_failed:
        failure_screenshot_path = f"{SCREENSHOTS_DIR}/FAIL_{safe_name}.png"
        page.screenshot(path=failure_screenshot_path)

        with open(failure_screenshot_path, "rb") as image:
            allure.attach(
                image.read(),
                name="failure_state",
                attachment_type=allure.attachment_type.PNG
            )

    # save trace for every test
    trace_path = f"{TRACES_DIR}/{status}_{safe_name}.zip"
    context.tracing.stop(path=trace_path)

    if os.path.exists(trace_path):
        with open(trace_path, "rb") as trace_file:
            allure.attach(
                trace_file.read(),
                name="playwright_trace",
                attachment_type="application/zip"
            )

    # close context — finalizes video
    context.close()

    # rename video to meaningful name with PASS/FAIL prefix
    video_path = page.video.path() if page.video else None
    if video_path and os.path.exists(video_path):
        new_video_path = f"{VIDEOS_DIR}/{status}_{safe_name}.webm"
        os.rename(video_path, new_video_path)

        with open(new_video_path, "rb") as video:
            allure.attach(
                video.read(),
                name="test_video",
                attachment_type="video/webm"
            )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Store test result and attach failure screenshot."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        item.rep_call = report

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            safe_name = make_safe_filename(item.nodeid)
            screenshot_path = f"{SCREENSHOTS_DIR}/FAIL_{safe_name}.png"

            pytest_html = item.config.pluginmanager.getplugin("html")
            if pytest_html:
                extra = getattr(report, "extra", [])
                extra.append(pytest_html.extras.image(screenshot_path))
                report.extra = extra