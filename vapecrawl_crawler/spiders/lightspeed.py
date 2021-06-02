import scrapy
from price_parser import parse_price
from ..items import ProductItem


class LightspeedSpider(scrapy.Spider):
    name = 'lightspeed'
    page = 1

    def __init__(self, base_url, vendor_id):
        self.vendor_url = base_url
        self.vendor_id = int(vendor_id)

    def start_requests(self):
        yield scrapy.Request(self.vendor_url + 'collection/page1.ajax', callback=self.parse)

    def parse(self, response):
        total_pages = response.json()['pages']
        products = response.json()['products']

        for product in products:
            name = product['title']
            url = product['url']
            unique_id = f"{product['id']}:{self.vendor_id}"
            price = parse_price(product['price']['price_money'])
            price = int(round(price.amount_float * 100))
            in_stock = product['available']
            image = product['image']

            item = ProductItem(name=name, price=price, image=image, in_stock=in_stock, url=url,
                               vendor_id=self.vendor_id, unique_id=unique_id)

            yield item

        if self.page < total_pages:
            self.page += 1
            next_page = response.url.replace('page' + str(self.page - 1) + '.ajax', 'page' + str(self.page) + '.ajax')
            yield response.follow(next_page, callback=self.parse)
