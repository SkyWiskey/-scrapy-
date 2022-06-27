# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os

from scrapy.pipelines.files import FilesPipeline
from kugou import settings

class MyKugouMusicPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        request_objs = super(MyKugouMusicPipeline, self).get_media_requests(item, info)
        for request_obj in request_objs:
            request_obj.item = item
        return request_objs

    def file_path(self, request, response=None, info=None, *, item=None):
        path = super(MyKugouMusicPipeline, self).file_path(request, response, info)
        category = request.item.get('title')
        name = request.item.get('song_name')
        category_path = os.path.join(settings.FILES_STORE, category)
        if not os.path.exists(category_path):
            os.makedirs(category_path)

        song_name = path.replace('full/', name)
        the_name,ext = os.path.splitext(song_name)
        song_name = the_name[:-40]+ext
        song_path = os.path.join(category_path, song_name)
        return song_path
