# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter
import pymysql

class ScwzPipelineMysql:
    def __init__(self):
        self.conn = pymysql.Connect(
            host='localhost',port=3306,user='root',
            password='123456',database='scwz',charset='utf8'
        )
        self.cursor = self.conn.cursor()
        self._sql = None

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
                insert into wzrd(title,reply_time,article,href) values(%s,%s,%s,%s);
            """
            return self._sql
        return self._sql

    def process_item(self, item, spider):
        print(item)
        try:
            self.cursor.execute(self.sql,(item['title'],item['reply_time'],
                                          item['article'],item['href']))
            self.conn.commit()
        except:
            self.conn.rollback()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()

class ScwzPipelineCsv:
    def __init__(self):
        self.fp = open('scwz.csv','wb')
        head = ['href','title','reply_time','article']
        self.exporter = CsvItemExporter(self.fp,fields_to_export = head)
        self.exporter.start_exporting()
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.fp.close()
