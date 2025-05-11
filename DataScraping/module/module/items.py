# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HotlineLaptopItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    link = scrapy.Field()
    stores = scrapy.Field()
    store_links = scrapy.Field()
    image_url = scrapy.Field()

class HotlineStoreItem(scrapy.Item):
    store_name = scrapy.Field()
    store_url = scrapy.Field()
    product_link = scrapy.Field()
    price = scrapy.Field()