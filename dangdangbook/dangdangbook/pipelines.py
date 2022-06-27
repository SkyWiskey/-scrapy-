# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import JsonLinesItemExporter
import pymysql



class DangdangbookPipeline:
    params = {
        'host':'localhost','port':3306,'user':'root',
        'password':'123456','database':'crawl_spider',
        'charset':'utf8'
    }
    def __init__(self):
        self.conn = pymysql.connect(**self.params)
        self.cursor = self.conn.cursor()
        self._sql = None

    @property
    def sql(self):
        if not self._sql:
            self._sql = ''' insert into dangdangbook(category,title,book_name,book_price,
    book_author,pub_time,book_press,book_comment_count,book_intro) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
            return self._sql
        return self._sql

    def process_item(self, item, spider):
        self.cursor.execute(self.sql,(item['category'],item['title'],item['book_name'],item['book_price']
                                      ,item['book_author'],item['pub_time'],item['book_press'],
                                      item['book_comment_count'],item['book_intro']))
        self.conn.commit()
        return item
    def close_spider(self,spider):
        print('爬虫结束了')
