import scrapy
from lab2.items import InfoItem, DataItem

class Lab2Item(scrapy.Spider):
    name = "data_css"
    allowed_domains = ["data.gov.ua"]
    start_urls = ["https://data.gov.ua//group/iustytsiia"]

    def parse(self, response):
        for li in response.css(".info-list li"):
            a = li.css("a")
            description_tag = li.css("div::text")

            if a:
                info_name = a.css("::text").get(default="").strip()
                if info_name and len(info_name) > 5:
                    info_link = response.urljoin(a.attrib["href"])
                    description_info = " ".join(description_tag.getall()).strip()

                    yield InfoItem(
                        name=info_name,
                        url=info_link,
                        description=description_info
                    )

                    yield response.follow(
                        url=info_link,
                        callback=self.parse_data,
                        meta={"data": info_name}
                    )

    def parse_data(self, response):
        for item in response.css(".resource-list__item"):
            title = item.css(".resource-list__item-container-title a")
            if title:
                data_name = title.css("::text").get(default="").strip()
                data_url = response.urljoin(title.attrib["href"])

                yield DataItem(
                    name=data_name,
                    url=data_url,
                    info=response.meta.get("data")
                )
