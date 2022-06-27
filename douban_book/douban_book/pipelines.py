# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter

class DoubanBookPipeline:
    def __init__(self):
        self.fp = open('douban_book.csv','wb')
        self.csv_head = ['book_type','type_name','title','score','com_count','infos','intro','detail_url']
        self.exporter = CsvItemExporter(self.fp,fields_to_export = self.csv_head,encoding = 'utf8')
        self.exporter.start_exporting()
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.fp.close()
        print('爬取完成')
