# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WxappunionItem(scrapy.Item):
    _id = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    pub_date = scrapy.Field()
    focus_num = scrapy.Field()
    block_quote = scrapy.Field()
    article = scrapy.Field()
