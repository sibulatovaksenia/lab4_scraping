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
if info_list:
    for li in info_list.find_all("li"):
        a = li.find("a")
        if a:
            info_name = a.get_text(strip=True)
            if len(info_name) > 5:
                info_link = BASE_URL + a.get("href")
                print(f"Info name: {info_name}")
                print(f"URL: {info_link}")

                other_page = get(info_link, headers=HEADERS)
                soup = BeautifulSoup(other_page.content, "html.parser")

                data_list = soup.find_all(class_="resource-list__item-container-title")

                if data_list:
                    for item in data_list:
                        data_link = item.find("a", href=True)
                        if data_link:
                            data_name = data_link.get_text(strip=True)
                            data_url = BASE_URL + data_link["href"]

                            print(f"  Data name: {data_name}")
                            print(f"  Data URL: {data_url}")
