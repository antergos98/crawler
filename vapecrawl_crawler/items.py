import scrapy


class ProductItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    image = scrapy.Field()
    in_stock = scrapy.Field()
    url = scrapy.Field()
    vendor_id = scrapy.Field()
    unique_id = scrapy.Field()
