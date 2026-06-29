import allure
import pytest
import requests
import certifi
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from pages.home_page import HomePage
from utils.helpers import build_full_url


@allure.feature("Broken Link Validation")
class TestBrokenLinks:
    """
    Test Case 4: Broken Link Validation
    Verifies that all hyperlinks on the homepage return HTTP 200.
    No broken links should exist.
    """

    HTTP_OK = 200
    REQUEST_TIMEOUT = 10

    @allure.story("All Homepage Links Return HTTP 200")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.broken_links
    def test_no_broken_links_on_homepage(self, page):
        """
        Collect all unique href values from the homepage,
        send HTTP GET request to each, and verify all return HTTP 200.
        """
        home = HomePage(page)

        # collect all unique hrefs from homepage
        raw_hrefs = home.get_all_links()

        assert len(raw_hrefs) > 0, "No links found on the homepage."

        # convert all relative URLs to absolute
        full_urls = [build_full_url(href) for href in raw_hrefs]

        with allure.step(f"Checking {len(full_urls)} unique links"):

            broken_links = []

            # prepare a session with retries and certifi-backed verification
            session = requests.Session()
            session.verify = certifi.where()
            retries = Retry(
                total=1,
                backoff_factor=0.2,
                status_forcelist=(429, 500, 502, 503, 504),
                allowed_methods=("GET", "HEAD"),
            )
            adapter = HTTPAdapter(max_retries=retries)
            session.mount("https://", adapter)
            session.mount("http://", adapter)
            session.trust_env = False
            session.headers.update({
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
            })

            # send request to each URL using the session
            for url in full_urls:
                try:
                    response = session.get(url, timeout=self.REQUEST_TIMEOUT, allow_redirects=True)
                    if response.status_code != self.HTTP_OK:
                        broken_links.append({"url": url, "status": response.status_code})

                except requests.exceptions.RequestException as error:
                    broken_links.append({"url": url, "status": f"ERROR: {str(error)}"})

        # assert no broken links were found
        if broken_links:
            failure_details = "\n".join(
                f"  [{item['status']}] {item['url']}" for item in broken_links
            )
            pytest.fail(f"Found {len(broken_links)} broken link(s):\n{failure_details}")
