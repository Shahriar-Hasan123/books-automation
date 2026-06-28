import random
from typing import Optional
from playwright.sync_api import Page, Locator

from pages.base_page import BasePage


class HomePage(BasePage):
    """
    Page Object for the Books to Scrape homepage.
    Contains all selectors and interactions specific to the homepage.
    """

    # Selectors (defined as class constants - easy to update if site changes)
    BOOKS_SECTION = "section"
    BOOK_ITEMS = "article.product_pod"
    BOOK_TITLE = "h3 a"
    BOOK_PRICE = ".price_color"
    BOOK_IMAGE = "img.thumbnail"
    NEXT_BUTTON = "li.next a"
    ALL_HEADINGS = "h1, h2, h3, h4, h5, h6"
    ALL_LINKS = "a[href]"

    def __init__(self, page: Page) -> None:
        """
        Initialize HomePage with Playwright page.

        Args:
            page: The Playwright Page object.
        """
        super().__init__(page)

    def is_books_section_visible(self) -> bool:
        """Check if the main books section container is visible on the page."""
        return self.is_element_visible(self.BOOKS_SECTION)

    def get_all_book_items(self) -> Locator:
        """Return a Locator containing all book article elements on the current page."""
        return self.wait_for_element(self.BOOK_ITEMS)

    def get_book_count(self) -> int:
        """Return the total number of books visible on the current page."""
        return self.get_all_book_items().count()

    def get_all_headings(self) -> Locator:
        """Return a Locator for all heading elements (h1 through h6) on the page."""
        return self.page.locator(self.ALL_HEADINGS)

    def get_random_books(self, count: int = 5) -> list[dict]:
        """
        Randomly select a given number of books from the current page.
        Captures each book's title and price before clicking.

        Args:
            count: Number of books to randomly select. Defaults to 5.

        Returns:
            A list of dicts, each containing 'title', 'price', and 'index'.
        """
        all_books = self.get_all_book_items()
        total = all_books.count()
        selected_indices = random.sample(range(total), min(count, total))

        books_data = []
        for index in selected_indices:
            book = all_books.nth(index)
            title = book.locator(self.BOOK_TITLE).get_attribute("title")
            price = book.locator(self.BOOK_PRICE).text_content().strip()
            books_data.append({
                "title": title,
                "price": price,
                "index": index
            })

        return books_data

    def click_book_by_index(self, index: int) -> None:
        """
        Click a book item by its position index on the page.

        Args:
            index: Zero-based index of the book to click.
        """
        book = self.get_all_book_items().nth(index)
        book.locator(self.BOOK_TITLE).click()
        self.page.wait_for_load_state("domcontentloaded")

    def get_all_links(self) -> list[str]:
        """
        Collect all unique href values from anchor elements on the homepage.

        Returns:
            A list of unique, non-empty href strings.
        """
        all_anchors = self.page.locator(self.ALL_LINKS).all()
        hrefs = set()
        for anchor in all_anchors:
            href = anchor.get_attribute("href")
            if href and href.strip():
                hrefs.add(href.strip())
        return list(hrefs)

    def get_all_product_images(self) -> Locator:
        """Return a Locator for all product thumbnail images on the current page."""
        return self.wait_for_element(self.BOOK_IMAGE)

    def click_next_page(self) -> bool:
        """
        Click the Next pagination button if it exists.

        Returns:
            True if Next button was found and clicked, False if no next page exists.
        """
        next_btn = self.page.locator(self.NEXT_BUTTON)
        if next_btn.count() > 0:
            next_btn.click()
            self.page.wait_for_load_state("domcontentloaded")
            return True
        return False