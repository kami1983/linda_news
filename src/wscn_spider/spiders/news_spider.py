import scrapy
import json
from ..items import NewsItem
from datetime import datetime

class NewsSpider(scrapy.Spider):
    name = 'wscn_news'
    allowed_domains = ['api-one-wscn.awtmt.com']
    start_urls = ['https://api-one-wscn.awtmt.com/apiv1/content/lives?channel=global-channel']
    
    def parse(self, response):
        data = json.loads(response.text)
        
        for item in data['data']['items']:
            news = NewsItem()
            news['item_id'] = item['id']
            news['title'] = item['title']
            news['content'] = item['content_text']
            news['author'] = 'WSCN'
            news['publish_time'] = datetime.fromtimestamp(item['display_time'])
            news['uri'] = item['uri']
            
            yield news 