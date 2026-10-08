import requests
from bs4 import BeautifulSoup


def web_search(query, limit=5):
    """
    Search the web using Bing HTML results.
    Returns titles, URLs and snippets.
    """

    url = "https://www.bing.com/search"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(
            url,
            params={"q": query},
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        results = []

        for item in soup.select("li.b_algo"):
            title_element = item.select_one("h2 a")
            snippet_element = item.select_one(".b_caption p")

            if not title_element:
                continue

            title = title_element.get_text(
                " ",
                strip=True
            )

            link = title_element.get("href")

            snippet = ""

            if snippet_element:
                snippet = snippet_element.get_text(
                    " ",
                    strip=True
                )

            results.append({
                "title": title,
                "url": link,
                "snippet": snippet
            })

            if len(results) >= limit:
                break

        return {
            "success": True,
            "query": query,
            "results": results
        }

    except Exception as error:
        return {
            "success": False,
            "query": query,
            "results": [],
            "error": str(error)
        }