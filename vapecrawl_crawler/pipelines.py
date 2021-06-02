from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import os


class PricePipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        price = adapter.get('price')

        if price is None:
            raise DropItem(f"Price is not valid in {item}")

        return item


class ImagePipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        image_url = adapter['image']
        if not image_url:
            raise DropItem(f"No image found for {item}")

        if spider.vendor_url not in image_url \
                and not image_url.startswith('//') and not image_url.startswith('http'):
            adapter['image'] = spider.vendor_url + image_url

        return item
