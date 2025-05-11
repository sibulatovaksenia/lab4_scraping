# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re


class PriceCleaningPipeline:
    def process_item(self, item, spider):
        if 'price' in item:
            price = item['price']
            if isinstance(price, str):
                price = re.sub(r'[^\d,\.]', '', price)
                price = price.replace(',', '')

                try:
                    price = float(price)
                except ValueError:
                    price = None

            item['price'] = price if price is not None else 0

        return item