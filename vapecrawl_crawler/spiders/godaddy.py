import scrapy
from price_parser import parse_price
from ..items import ProductItem


class GodaddySpider(scrapy.Spider):
    name = 'godaddy'
    page = 1

    def __init__(self, base_url, vendor_id, api_url):
        self.vendor_url = base_url
        self.vendor_id = int(vendor_id)
        self.api_url = api_url

    def start_requests(self):
        yield scrapy.Request(self.api_url + 'api/v2/products?per_page=99999', callback=self.parse)

    def parse(self, response):
        products = response.json()['products']

        for product in products:
            price = parse_price(product['price']['display'])
            
            name = product['name']
            url = self.vendor_url + product['relative_url'].replace('/', '', 1)
            unique_id = f"{product['id']}:{self.vendor_id}"
            price = int(round(price.amount_float * 100))
            in_stock = product['in_stock']
            image = product['default_asset_url']

            item = ProductItem(name=name, price=price, image=image, in_stock=in_stock, url=url,
                               vendor_id=self.vendor_id, unique_id=unique_id)

            yield item
