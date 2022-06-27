# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo


class News163Pipeline:
    def open_spider(self,spider):
        print('爬虫开始咯')
        self.conn = pymongo.MongoClient(
            host='localhost',port=27017
        )
        self.collection = self.conn['News163']['hotModule']

    def process_item(self, item, spider):
        try:
            self.collection.insert_one(item)
        except Exception as e:
            print(e)
            pass
        print(item)
        return item

    def close_spider(self,spider):
        self.conn.close()
        print('爬虫结束了')