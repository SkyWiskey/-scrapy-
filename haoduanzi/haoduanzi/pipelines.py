# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import JsonLinesItemExporter
from scrapy.exporters import CsvItemExporter


class HaoduanziPipeline:
    def __init__(self):
        self.fp = open('haoduanzi.csv','wb')
        self.csv_head = ['title','article']
        self.exporter = CsvItemExporter(self.fp,fields_to_export = self.csv_head)
        self.exporter.start_exporting()
    def start_spider(self,spider):
        print('爬虫开始了')

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.fp.close()
        print('爬虫结束了')
