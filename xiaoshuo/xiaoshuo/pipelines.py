# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os



class XiaoshuoPipeline:
    base_dir = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(base_dir,'武林中文网小说')
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    def process_item(self, item, spider):
        novel_title = item['novel_title']
        with open(f'{self.file_path}/{novel_title}.txt','a',encoding='utf8')as f:
            f.write(f"{item['chapter_title']}:\n {item['article']}")
        return item

    def close_spider(self,spider):
        print('爬虫结束了')

