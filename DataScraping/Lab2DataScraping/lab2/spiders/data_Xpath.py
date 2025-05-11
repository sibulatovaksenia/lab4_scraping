import scrapy
from lab2.items import InfoItem, DataItem

class Lab2Item(scrapy.Spider):
    name = "data_xpath"
    allowed_domains = ["data.gov.ua"]
    start_urls = ["https://data.gov.ua//group/iustytsiia"]

    def parse(self, response):
        for li in response.xpath("//ul[contains(@class, 'info-list')]/li"):
            a = li.xpath(".//a")
            description_tag = li.xpath(".//div[not(@class)]//text()")

            if a:
                info_name = a.xpath("normalize-space(text())").get()
                if info_name and len(info_name) > 5:
                    info_link = response.urljoin(a.xpath("@href").get())
                    description_info = description_tag.get(default="").strip()


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
        for item in response.xpath("//div[contains(@class, 'resource-list__item')]"):
            title = item.xpath(".//div[contains(@class, 'resource-list__item-container-title')]/a")
            if title:
                data_name = title.xpath("normalize-space(text())").get()
                data_url = response.urljoin(title.xpath("@href").get())

                yield DataItem(
                    name=data_name,
                    url=data_url,
                    info=response.meta.get("data")
                )
