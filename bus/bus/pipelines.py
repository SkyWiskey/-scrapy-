# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter


class BusPipeline:
    def __init__(self):
        self.fp = open('bus_line.csv','wb')
        head = ['city_name','line_name','line_sites']
        self.exporter = CsvItemExporter(self.fp,fields_to_export=head)
        self.exporter.start_exporting()
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.fp.close()
