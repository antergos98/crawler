import scrapy
from price_parser import parse_price
from ..items import ProductItem


class VolusionSpider(scrapy.Spider):
    name = 'volusion'

    def __init__(self, base_url, vendor_id):
        self.vendor_url = base_url
        self.vendor_id = int(vendor_id)

    def start_requests(self):
        yield scrapy.Request(self.vendor_url + 'pindex.asp', callback=self.parse)

    def parse(self, response):
        links = response.css('#content_area tr:nth-child(2) table:nth-child(3) a::attr(href)').getall()
        for link in links:
            yield response.follow(link, callback=self.parse_product)

        next_page = response.css('#content_area tr:nth-child(2) table:nth-child(1) font + a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_product(self, response):
        name = response.css('span[itemprop="name"]::text').get()
        unique_id = f"{response.url.rsplit('/', 1)[-1]}:{self.vendor_id}"

        try:
            image = response.css('img#product_photo').attrib['src']
        except:
            image = None

        try:
            price = parse_price(response.css('span[itemprop="price"]::text').get())
            price = int(round(price.amount_float * 100))
        except:
            price = None

        in_stock = response.css('meta[itemprop="availability"]::attr(content)').get() == 'InStock'
        url = response.url

        item = ProductItem(name=name, price=price, image=image, in_stock=in_stock, url=url, vendor_id=self.vendor_id, unique_id=unique_id)

        yield item
