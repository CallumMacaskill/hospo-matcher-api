import os
import re
from enum import Enum

from bs4 import BeautifulSoup


class DivClassIDs(str, Enum):
    LIST_ITEM = "vIjFZ Gi o VOEhq"
    VENUE_LINK = "BMQDV _F Gv wSSLS SwZTJ FGwzt ukgoS"
    IMAGE = "NhWcC _R mdkdE afQPz eXZKw"


def extract_page_content(html_path: str, page_files_path: str) -> list[dict]:
    """
    Extract search result content from an HTML page.

    Args:
        html_path (str): file path of the HTML search results
        page_files_path (str): dir path of the search page's extra files

    Returns:
        list[dict]: extracted venues from search results
    """

    # Open the local HTML file
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # Extract search result items
    result_divs = soup.find_all("div", class_=DivClassIDs.LIST_ITEM)

    # Extract name and image filepath
    # TODO: handle missing content
    for result_div in result_divs:
        # Extract the name and link
        result_link = result_div.find("a", class_=DivClassIDs.VENUE_LINK)
        result_name = result_link.text

        # Get image source name
        picture_tag = result_div.find("picture", class_=DivClassIDs.IMAGE)
        img_tag = picture_tag.find("img")
        src_value = img_tag["src"]
        file_name_search = re.search(r"[^\/]+$", src_value)
        file_name = file_name_search.group()
        print(file_name)

        # Clean name
        result_name = re.sub(r"\n", " ", result_name)  # Replace new line with space
        result_name = re.sub(r" +", " ", result_name)  # Remove duplicate spaces
        result_name = re.sub(r"\d+\.\s*", "", result_name)  # Remove leading enumeration
        print(result_name)


def process_search_pages() -> list[dict]:
    """
    Extract search result content from all local pages.

    Returns:
        list[dict]: extracted venues from search results
    """
    search_dumps_dir = "web_scraping\search_dumps"
    # TODO: Flatten this to a single os.walk() call
    for parent_dir in os.listdir(search_dumps_dir):
        for root, dirs, files in os.walk(os.path.join(search_dumps_dir, parent_dir)):
            if dirs and files:
                html_page_path = os.path.join(root, files[0])
                page_files_path = os.path.join(root, dirs[0])
                extract_page_content(html_page_path, page_files_path)


if __name__ == "__main__":
    process_search_pages()
