# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os

from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from qichezhijia import settings

# class QichezhijiaPipeline:
#     def process_item(self, item, spider):
#         return item


class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        request_objs = super(MyImagesPipeline, self).get_media_requests(item,info)
        for request_obj in request_objs:
            request_obj.item = item
        return request_objs

    def file_path(self, request, response=None, info=None, *, item=None):
        path = super(MyImagesPipeline, self).file_path(request,response,info)
        category =request.item.get('category')
        category_path =os.path.join(settings.IMAGES_STORE,category)
        if not os.path.exists(category_path):
            os.makedirs(category_path)

        image_name =path.replace('full/','').replace('jpg','png')
        image_path = os.path.join(category_path,image_name)
        return image_path
