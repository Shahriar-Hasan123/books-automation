import allure
import pytest

from pages.home_page import HomePage
from pages.detail_page import DetailPage


@allure.feature("Book Data Consistency")
class TestDataConsistency:
    """
    Test Case 3: Book Data Consistency Validation
    Verifies that book title and price shown on the homepage
    exactly match the title and price shown on the detail page.
    """

    BOOKS_TO_SELECT = 5

    @allure.story("Title and Price Consistency Across Pages")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.consistency
    def test_book_data_is_consistent(self, page):
        """
        Randomly select 5 books and verify that title and price
        on the homepage match exactly with the detail page.
        """
        home = HomePage(page)
        detail = DetailPage(page)

        # collect 5 random books (title + price + index)
        selected_books = home.get_random_books(self.BOOKS_TO_SELECT)

        assert (
            len(selected_books) == self.BOOKS_TO_SELECT
        ), f"Expected {self.BOOKS_TO_SELECT} books. Got: {len(selected_books)}"

        for book_data in selected_books:
            homepage_title = book_data["title"]
            homepage_price = book_data["price"]
            book_index = book_data["index"]

            with allure.step(f"Checking consistency for: '{homepage_title}'"):

                # click the book to open detail page
                home.click_book_by_index(book_index)

                # verify detail page loaded
                assert (
                    detail.is_loaded()
                ), f"Detail page did not load for book: '{homepage_title}'"

                # capture detail page data
                detail_title = detail.get_book_title()
                detail_price = detail.get_book_price()

                # compare titles
                assert homepage_title == detail_title, (
                    f"Title mismatch!\n"
                    f"Homepage title : '{homepage_title}'\n"
                    f"Detail title   : '{detail_title}'"
                )

                # compare prices
                assert homepage_price == detail_price, (
                    f"Price mismatch!\n"
                    f"Homepage price : '{homepage_price}'\n"
                    f"Detail price   : '{detail_price}'"
                )

                # go back to homepage for next book
                detail.go_back_to_homepage()
