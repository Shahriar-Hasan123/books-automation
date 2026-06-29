import allure
from playwright.sync_api import Page

from pages.base_page import BasePage


class DetailPage(BasePage):
    """
    Page Object for the Book Detail page on Books to Scrape.
    Handles all interactions and verifications on individual book pages.
    """

    # Selectors
    BOOK_TITLE_H1 = "h1"
    BOOK_INFO_TABLE = "table.table.table-striped"
    PRODUCT_MAIN = "div.product_main"

    def __init__(self, page: Page) -> None:
        """
        Initialize DetailPage with Playwright page.
        """
        super().__init__(page)

    def get_book_title(self) -> str:
        """
        Return the H1 title text of the book on the detail page.
        """
        self.wait_for_element(self.BOOK_TITLE_H1)
        return self.page.locator(self.BOOK_TITLE_H1).text_content().strip()

    def get_book_price(self) -> str:
        """
        Return the book price displayed on the detail page.
        """
        self.wait_for_element(self.PRODUCT_MAIN)
        return (
            self.page.locator(self.PRODUCT_MAIN)
            .locator(".price_color")
            .text_content()
            .strip()
        )

    def is_book_info_visible(self) -> bool:
        """
        Check if the book information table is visible on the detail page.
        """
        return self.is_element_visible(self.BOOK_INFO_TABLE)

    def is_loaded(self) -> bool:
        """
        Verify the detail page has loaded by checking the H1 and product section exist.
        """
        return (
            self.is_element_visible(self.BOOK_TITLE_H1)
            and self.is_element_visible(self.PRODUCT_MAIN)
        )

    def go_back_to_homepage(self) -> None:
        """Navigate back to the previous page (homepage) using browser back."""
        self.page.go_back()
        self.page.wait_for_load_state("domcontentloaded")