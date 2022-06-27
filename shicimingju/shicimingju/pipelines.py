# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
import psycopg2

class ShicimingjuPipeline:
    def open_spider(self,spider):
        # MongoDB配置
        self.mgConn = pymongo.MongoClient(
            host='localhost',port=27017
        )
        self.collection = self.mgConn['Shicimingju']['Poems']

        # PostgreSQL配置
        self.pqConn = psycopg2.connect(
            host='127.0.0.1',port=5432,
            user='postgres',password='postgresql',
            database='testdb'
        )
        self.cursor = self.pqConn.cursor()
        print('爬虫开始咯')

    def process_item(self, item, spider):
        # 插入到MongoDB数据库中
        try:
            self.collection.insert_one(item)
        except:
            pass

        # 插入到PostgreSQL数据库中
        sql = f"insert into poems values({int(item['_id'])},'{item['poet']}','{item['poem_title']}','{item['poem']}');"
        try:
            self.cursor.execute(sql)
            self.pqConn.commit()
        except:
            self.pqConn.rollback()
            pass
        print(f'{item}\n成功写入到MongoDB和PostgreSQL数据库中！')
        return item
    def close_spider(self,spider):
        self.mgConn.close()
        self.pqConn.close()
        print('爬虫结束了')