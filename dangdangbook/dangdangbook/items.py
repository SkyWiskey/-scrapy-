# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DangdangbookItem(scrapy.Item):
    category = scrapy.Field()
    title = scrapy.Field()
    book_name = scrapy.Field()
    book_price = scrapy.Field()
    book_author = scrapy.Field()
    pub_time = scrapy.Field()
    book_press = scrapy.Field()
    book_comment_count = scrapy.Field()
    book_intro = scrapy.Field()
