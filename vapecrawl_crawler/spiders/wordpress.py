import scrapy
from ..items import ProductItem


class WordpressSpider(scrapy.Spider):
    name = 'wordpress'
    start_urls = []
    page = 1

    def __init__(self, base_url, vendor_id):
        self.vendor_url = base_url
        self.vendor_id = int(vendor_id)

    def start_requests(self):
        yield scrapy.Request(self.vendor_url + 'wp-json/wc/store/products?per_page=100&page=1', callback=self.parse)

    def parse(self, response):
        products = response.json()
        for product in products:

            name = product['name']
            price = product['prices']['price']
            in_stock = product['is_in_stock']
            url = product['permalink']
            unique_id = f"{product['id']}:{self.vendor_id}"

            try:
                image = product['images'][0]['src']
            except:
                image = None

            item = ProductItem(name=name, price=price, image=image, in_stock=in_stock, url=url,
                               vendor_id=self.vendor_id, unique_id=unique_id)

            yield item

        if len(products) > 0:
            self.page += 1
            next_page = response.url.replace('&page=' + str(self.page - 1), '&page=' + str(self.page))
            yield response.follow(next_page, callback=self.parse)
