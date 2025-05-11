# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InfoItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    description = scrapy.Field()


class DataItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    info = scrapy.Field()
