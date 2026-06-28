from urllib.parse import urljoin

BASE_URL = "https://books.toscrape.com/"


def build_full_url(href: str) -> str:
    """
    Convert a relative href to an absolute URL.
    If already absolute, return as-is.

    Args:
        href: The raw href value from an anchor element.

    Returns:
        A fully qualified absolute URL string.

    Examples:
        >>> build_full_url("catalogue/book_1/index.html")
        'https://books.toscrape.com/catalogue/book_1/index.html'
        >>> build_full_url("https://books.toscrape.com/index.html")
        'https://books.toscrape.com/index.html'
    """
    return urljoin(BASE_URL, href)
