import allure
import pytest

from pages.home_page import HomePage
from pages.detail_page import DetailPage


@allure.feature("Random Book Navigation")
class TestBookNavigation:
    """
    Test Case 2: Random Book Navigation Validation
    Verifies that randomly selected books open the correct detail pages
    and that all detail page content is properly displayed.
    """

    BOOKS_TO_SELECT = 5

    @allure.story("Random Book Navigation and Detail Validation")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.navigation
    def test_random_book_navigation(self, page):
        """
        Randomly select 5 books from homepage, click each one,
        verify the detail page loads with correct H1 title and book info,
        then navigate back to homepage after each book.
        """
        home = HomePage(page)
        detail = DetailPage(page)

        # collect 5 random books with their titles and indices
        selected_books = home.get_random_books(self.BOOKS_TO_SELECT)

        assert len(selected_books) == self.BOOKS_TO_SELECT, (
            f"Expected {self.BOOKS_TO_SELECT} books to be selected. "
            f"Got: {len(selected_books)}"
        )

        for book_data in selected_books:
            expected_title = book_data["title"]
            book_index = book_data["index"]

            with allure.step(f"Validating book: '{expected_title}'"):

                # click the book
                home.click_book_by_index(book_index)

                # verify detail page loaded successfully
                assert (
                    detail.is_loaded()
                ), f"Detail page did not load for book: '{expected_title}'"

                # ✨ Take screenshot showing detail page with book info
                safe_title = expected_title[:30].replace(" ", "_").replace("/", "_")
                detail.take_screenshot(f"navigation_detail_{book_index}_{safe_title}")

                # verify H1 matches the title captured on homepage
                actual_title = detail.get_book_title()
                assert actual_title == expected_title, (
                    f"Title mismatch!\n"
                    f"Expected (homepage): '{expected_title}'\n"
                    f"Actual (detail H1):  '{actual_title}'"
                )

                # verify book information table is visible
                assert (
                    detail.is_book_info_visible()
                ), f"Book info table not visible for: '{expected_title}'"

                # go back to homepage for next iteration
                detail.go_back_to_homepage()
