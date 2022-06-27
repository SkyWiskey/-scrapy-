# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os.path

import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline


class BaiduimagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for url in item['image_urls']:
            yield scrapy.Request(url)

    def file_path(self, request, response=None, info=None, *, item=None):
        file_name = item['category']
        image_name = '-'.join(request.url.split('u=')[-1].split('&')[0].split(',')) + '.png'
        image_path = os.path.join(file_name,image_name)
        return image_path

    def item_completed(self, results, item, info):
        return item
