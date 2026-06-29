import allure
import pytest

from pages.home_page import HomePage
from utils.helpers import build_full_url


@allure.feature("Broken Link Validation")
class TestBrokenLinks:
    """
    Test Case 4: Broken Link Validation
    Verifies that all hyperlinks on the homepage return HTTP 200.
    Uses Playwright's API request context to check links — consistent
    with the browser session already used throughout the framework.
    """

    HTTP_OK = 200

    @allure.story("All Homepage Links Return HTTP 200")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.broken_links
    def test_no_broken_links_on_homepage(self, page):
        """
        Collect all unique href values from the homepage,
        send HTTP GET request to each using Playwright's request context,
        and verify all return HTTP 200.
        """
        home = HomePage(page)

        # Step 1: collect all unique hrefs from homepage
        raw_hrefs = home.get_all_links()

        assert len(raw_hrefs) > 0, "No links found on the homepage."

        # Step 2: convert all relative URLs to absolute
        full_urls = [build_full_url(href) for href in raw_hrefs]

        with allure.step(f"Checking {len(full_urls)} unique links"):

            broken_links = []

            # Step 3: use Playwright's built-in request context
            # This reuses the same browser session — handles SSL and headers correctly
            for url in full_urls:
                try:
                    response = page.request.get(
                        url, timeout=15000  # Playwright uses milliseconds
                    )
                    if response.status != self.HTTP_OK:
                        broken_links.append({"url": url, "status": response.status})

                except Exception as error:
                    broken_links.append({"url": url, "status": f"ERROR: {str(error)}"})

        # Step 4: assert no broken links were found
        if broken_links:
            failure_details = "\n".join(
                f"  [{item['status']}] {item['url']}" for item in broken_links
            )
            pytest.fail(f"Found {len(broken_links)} broken link(s):\n{failure_details}")
