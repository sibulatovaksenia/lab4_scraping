import scrapy
from module.items import HotlineLaptopItem, HotlineStoreItem

class HotlineLaptopSpider(scrapy.Spider):
    name = "laptops"
    allowed_domains = ["hotline.us"]
    start_urls = [f"https://hotline.ua/ua/computer/noutbuki-netbuki/?p={page}" for page in range(1, 5)]


    def parse(self, response):
        products = response.css('div.flex content list-body__slice-wrapper list-body__slice-wrapper--no-division-bb')

        for product in products:
            title = product.css('a.item-title::text').get()
            price = product.css('div.list-item__value-price::text').get()
            link = product.css('a.item-title::attr(href)').get()
            image_url = product.css('list-item__img::attr(src)').get()

            if title and price and link:
                yield response.follow(
                    response.urljoin(link),
                    callback=self.parse_store,
                    meta={
                        'title': title.strip(),
                        'price': price.strip(),
                        'link': response.urljoin(link),
                        'image_url': image_url if image_url else None
                    }
                )

        next_page = response.css('a.item-title::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_store(self, response):
        item = HotlineLaptopItem()
        item['title'] = response.meta['title']
        item['price'] = response.meta['price']
        item['link'] = response.meta['link']
        item['image_url'] = response.meta.get('image_url')

        stores = response.css('div.list')
        for store in stores:
            store_name = store.css('a.shop__title::text').get()
            store_link = store.css('a.shop__title::attr(href)').get()
            store_price = self.get_store_price(store)
            if store_name and store_link and store_price:
                store_item = HotlineStoreItem()
                store_item['store_name'] = store_name.strip()
                store_item['store_url'] = response.urljoin(store_link.strip())
                store_item['product_link'] = response.url
                store_item['price'] = store_price.strip()

                yield store_item
        yield item

    def get_store_price(self, store):
        price_div = store.css('div.price-values')
        prices=price_div.css('span::text').getall()
        if prices:
            return prices[0].strip()
        return 'None'