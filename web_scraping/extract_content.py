from bs4 import BeautifulSoup
import re
import os

def extract_content(html_path: str, page_files_path: str):
    """
    Extract search result content from an HTML page.
    """

    # Open the local HTML file
    with open(html_path, "r", encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # Extract search result items
    # TODO: Create enum of class IDs
    result_divs = soup.find_all('div', class_="vIjFZ Gi o VOEhq")

    # Extract name and image filepath
    for result_div in result_divs:
        # Extract the name and link
        result_link = result_div.find('a', class_="BMQDV _F Gv wSSLS SwZTJ FGwzt ukgoS")
        result_name = result_link.text

        # Get image source name
        picture_tag = result_div.find('picture', class_='NhWcC _R mdkdE afQPz eXZKw')
        img_tag = picture_tag.find('img')
        src_value = img_tag['src']
        file_name_search = re.search(r"[^\/]+$", src_value)
        file_name = file_name_search.group()
        print(file_name)

        # Clean name
        result_name = re.sub(r"\n", " ", result_name) # Replace new line with space
        result_name = re.sub(r" +", " ", result_name) # Remove duplicate spaces
        result_name = re.sub(r"\d+\.\s*", "", result_name) # Remove leading enumeration
        print(result_name)

if __name__=="__main__":

    search_dumps_dir = "web_scraping\search_dumps"
    for search_page in os.listdir(search_dumps_dir):
        if search_page.endswith(".html"):
            search_page_name = search_page.split(".html")[0]
            extract_content(os.path.join(search_dumps_dir, search_page), os.path.join(search_dumps_dir, f"{search_page_name}_files"))
