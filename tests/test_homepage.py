import allure
import pytest

from pages.home_page import HomePage


@allure.feature("Homepage Validation")
class TestHomepage:
    """
    Test Case 1: Homepage Validation
    Verifies that the homepage loads correctly and displays all expected content.
    """

    EXPECTED_URL = "https://books.toscrape.com/index.html"
    EXPECTED_TITLE = "All products | Books to Scrape - Sandbox"

    @allure.story("URL Validation")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.homepage
    def test_url_is_correct(self, page):
        """Verify the homepage URL matches the expected URL exactly."""
        home = HomePage(page)

        current_url = home.get_current_url()

        assert current_url == self.EXPECTED_URL, (
            f"Expected URL: {self.EXPECTED_URL}\n" f"Actual URL:   {current_url}"
        )

    @allure.story("Page Title Validation")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.homepage
    def test_page_title_is_correct(self, page):
        """Verify the browser tab title matches the expected page title."""
        home = HomePage(page)

        actual_title = home.get_page_title()

        assert actual_title == self.EXPECTED_TITLE, (
            f"Expected title: {self.EXPECTED_TITLE}\n" f"Actual title:   {actual_title}"
        )

    @allure.story("Headings Visibility")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.homepage
    def test_all_headings_are_visible(self, page):
        """Verify every h1-h6 heading on the page is visible to the user."""
        home = HomePage(page)

        headings = home.get_all_headings()
        heading_count = headings.count()

        assert heading_count > 0, "No headings found on the homepage."

        for i in range(heading_count):
            heading = headings.nth(i)
            assert heading.is_visible(), f"Heading at index {i} is not visible."

    @allure.story("Headings Non-Empty Text")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.homepage
    def test_all_headings_have_non_empty_text(self, page):
        """Verify every heading contains non-empty text content."""
        home = HomePage(page)

        headings = home.get_all_headings()
        heading_count = headings.count()

        assert heading_count > 0, "No headings found on the homepage."

        for i in range(heading_count):
            heading = headings.nth(i)
            text = heading.text_content().strip()
            assert text != "", f"Heading at index {i} has empty text."

    @allure.story("Books Section Visibility")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.homepage
    def test_books_section_is_visible(self, page):
        """Verify the main books section container is visible on the homepage."""
        home = HomePage(page)

        assert (
            home.is_books_section_visible()
        ), "Books section is not visible on the homepage."

    @allure.story("Books Section Has Books")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.homepage
    def test_books_section_has_at_least_one_book(self, page):
        """Verify the books section contains at least one book item."""
        home = HomePage(page)

        book_count = home.get_book_count()

        assert (
            book_count >= 1
        ), f"Expected at least 1 book on homepage. Found: {book_count}"
