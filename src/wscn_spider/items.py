import scrapy

class NewsItem(scrapy.Item):
    item_id = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()
    publish_time = scrapy.Field()
    uri = scrapy.Field() 