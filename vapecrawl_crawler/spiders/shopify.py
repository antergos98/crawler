import scrapy
from price_parser import parse_price

from ..items import ProductItem


class ShopifySpider(scrapy.Spider):
    name = 'shopify'
    page = 1

    def __init__(self, base_url, vendor_id):
        self.vendor_url = base_url
        self.vendor_id = int(vendor_id)

    def start_requests(self):
        yield scrapy.Request(self.vendor_url + 'products.json?limit=200&page=1', callback=self.parse)

    def parse(self, response):
        products = response.json()['products']

        for product in products:

            name = product['title']
            url = self.vendor_url + 'products/' + product['handle']
            unique_id = f"{product['id']}:{self.vendor_id}"

            try:
                price = parse_price(product['variants'][0]['price'])
                price = int(round(price.amount_float * 100))
                in_stock = product['variants'][0]['available']
            except IndexError:
                price = 0
                in_stock = False

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
