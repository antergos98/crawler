import scrapy
from ..items import ProductItem
from price_parser import parse_price


class DashvapesSpider(scrapy.Spider):
    name = 'dashvapes'
    start_urls = ['https://dashvapes.com/tools/search.php?key=']
    vendor_url = "https://dashvapes.com/"
    vendor_id = 1

    def parse(self, response):
        products = response.json()

        for product in products:
            price = parse_price(product['price'])
            name = product['name']
            price = int(round(price.amount_float * 100))
            image = product['image']
            in_stock = product['availability'] == 'In Stock'
            url = product['url']
            unique_id = f"{product['sku']}:{self.vendor_id}"

            item = ProductItem(name=name, price=price, image=image, in_stock=in_stock, url=url,
                               vendor_id=self.vendor_id, unique_id=unique_id)

            yield item
