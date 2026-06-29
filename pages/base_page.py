import os
import allure
from playwright.sync_api import Page, Locator


class BasePage:
    """
    Base class for all page objects.
    Contains reusable methods shared across every page of the website.
    All other page classes must inherit from this class.
    """

    def __init__(self, page: Page) -> None:
        """
        Initialize BasePage with a Playwright Page instance.
        """
        self.page = page

    def get_current_url(self) -> str:
        """Return the current browser URL."""
        return self.page.url

    def get_page_title(self) -> str:
        """Return the current page title (browser tab text)."""
        return self.page.title()

    def wait_for_element(self, selector: str) -> Locator:
        """
        Wait for an element to be visible on the page and return it.
        """
        locator = self.page.locator(selector)
        locator.first.wait_for(state="visible")
        return locator

    def is_element_visible(self, selector: str) -> bool:
        """
        Check if an element is visible on the page.
        """
        return self.page.locator(selector).first.is_visible()

    def navigate_to(self, url: str) -> None:
        """
        Navigate the browser to a given URL and wait for it to load.
        """
        self.page.goto(url)
        self.page.wait_for_load_state("domcontentloaded")

    def take_screenshot(self, name: str) -> str:
        """
        Take a screenshot at a critical test point and attach to Allure report.
        Saved as STEP_{name}.png for organization and evidence.
        """
        screenshots_dir = "screenshots"
        os.makedirs(screenshots_dir, exist_ok=True)
        screenshot_path = f"{screenshots_dir}/STEP_{name}.png"
        self.page.screenshot(path=screenshot_path)
        
        # Attach screenshot to Allure report
        with open(screenshot_path, "rb") as image:
            allure.attach(
                image.read(),
                name=f"step_{name}",
                attachment_type=allure.attachment_type.PNG
            )
        
        return screenshot_path