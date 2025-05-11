from requests import get
from bs4 import BeautifulSoup

BASE_URL = "https://data.gov.ua"
URL = f"{BASE_URL}/group/iustytsiia"
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
}

page = get(URL, headers=HEADERS)
soup = BeautifulSoup(page.content, "html.parser")

info_list = soup.find(class_="info-list")

for li in info_list.find_all("li"):
    a = li.find("a")
    description_tag = li.find("div")
    if a:
        info_name = a.get_text(strip=True)
        if info_name and len(info_name) > 5:
            info_link = BASE_URL + a.get("href")
            print(f"Info name: {info_name}")
            print(f"URL: {info_link}")

            description = description_tag.get_text(strip=True)
            print(f"Description: {description}")

            other_page = get(info_link, headers=HEADERS)
            other_soup = BeautifulSoup(other_page.content, "html.parser")

            data_items = other_soup.find_all(class_="resource-list__item")

            for item in data_items:
                title = item.find(class_="resource-list__item-container-title")
                download_label = item.find(class_="label")

                if title:
                    data_link_tag = title.find("a")
                    if data_link_tag:
                        data_name = data_link_tag.get_text(strip=True)
                        data_url = BASE_URL + data_link_tag.get("href")
                        print(f"  Data name: {data_name}")
                        print(f"  Data URL: {data_url}")

                if download_label:
                    download_type = download_label.get_text(strip=True)
                    print(f"  Download type: {download_type}")
