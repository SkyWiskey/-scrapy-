# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanBookItem(scrapy.Item):
    book_type = scrapy.Field()
    type_name = scrapy.Field()
    title = scrapy.Field()
    score = scrapy.Field()
    com_count = scrapy.Field()
    infos = scrapy.Field()
    intro = scrapy.Field()
    detail_url = scrapy.Field()
