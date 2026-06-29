import allure
import pytest

from pages.home_page import HomePage


@allure.feature("Product Image Validation")
class TestImageValidation:
    """
    Test Case 5: Product Image Validation
    Verifies that all product images are rendered correctly
    and contain required attributes across multiple pages.
    Maximum of 5 pages are validated or until pagination ends.
    """

    MAX_PAGES = 5

    @allure.story("Image Attributes Validation Across Pages")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.images
    def test_product_images_are_valid(self, page):
        """
        Validate all product images on up to 5 pages.
        Each image must be visible and have non-empty src, alt,
        and a class attribute containing 'thumbnail'.
        """
        home = HomePage(page)

        page_number = 1

        while page_number <= self.MAX_PAGES:

            with allure.step(f"Validating images on page {page_number}"):

                # get all product images on current page
                images = home.get_all_product_images()
                image_count = images.count()

                assert image_count > 0, (
                    f"No product images found on page {page_number}."
                )

                # ✨ Take screenshot showing all images on this page
                home.take_screenshot(f"images_page_{page_number}")

                # validate each image
                image_failures = []

                for i in range(image_count):
                    image = images.nth(i)

                    # check visibility
                    if not image.is_visible():
                        image_failures.append(
                            f"Page {page_number} | Image {i + 1}: not visible"
                        )
                        continue

                    # check src attribute
                    src = image.get_attribute("src")
                    if not src or not src.strip():
                        image_failures.append(
                            f"Page {page_number} | Image {i + 1}: src is empty or missing"
                        )

                    # check alt attribute
                    alt = image.get_attribute("alt")
                    if not alt or not alt.strip():
                        image_failures.append(
                            f"Page {page_number} | Image {i + 1}: alt is empty or missing"
                        )

                    # check class contains thumbnail
                    class_attr = image.get_attribute("class")
                    if not class_attr or "thumbnail" not in class_attr:
                        image_failures.append(
                            f"Page {page_number} | Image {i + 1}: "
                            f"class does not contain 'thumbnail' (got: '{class_attr}')"
                        )

                # Step 3: report all image failures for this page at once
                if image_failures:
                    failure_details = "\n".join(image_failures)
                    pytest.fail(
                        f"Image validation failed on page {page_number}:\n"
                        f"{failure_details}"
                    )

            # Step 4: try to go to next page
            has_next = home.click_next_page()

            if not has_next:
                # no more pages - stop gracefully
                break

            page_number += 1