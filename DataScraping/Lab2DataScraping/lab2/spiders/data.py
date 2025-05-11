import scrapy
from bs4 import BeautifulSoup
from lab2.items import InfoItem, DataItem


class Lab2Item(scrapy.Spider):
    name = "data"
    allowed_domains = ["data.gov.ua"]

    start_urls = ["https://data.gov.ua//group/iustytsiia"]

    def parse(self, response):
        soup = BeautifulSoup(response.body, "html.parser")
        info_list = soup.find(class_="info-list")

        for li in info_list.find_all("li"):
            a = li.find("a")
            description_tag = li.find("div")
            if a:
                info_name = a.get_text(strip=True)
                if info_name and len(info_name) > 5:
                    info_link = f"https://data.gov.ua{a.get('href')}"
                    description_info = description_tag.get_text(strip=True)
                    yield InfoItem(
                        name=info_name,
                        url=info_link,
                        description=description_info

                    )

                    yield scrapy.Request(
                        url=info_link,
                        callback=self.parse_data,
                        meta={
                            "data": InfoItem
                        }
                    )

    def parse_data(self, response):
        other_soup = BeautifulSoup(response.body, "html.parser")


        data_items = other_soup.find_all(class_="resource-list__item")
        for item in data_items:
            title = item.find(class_="resource-list__item-container-title")


            if title:
                data_link_tag = title.find("a")
                if data_link_tag:
                    data_name = data_link_tag.get_text(strip=True)
                    data_url = f"https:data.gov.ua{item.a.get('href')}"

                yield DataItem(
                    name=data_name,
                    url=data_url,
                    info=response.meta.get("data")
                )
