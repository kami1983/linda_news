import scrapy
import json
from ..items import NewsItem
from datetime import datetime, timedelta, timezone

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
            
            # 创建北京时间的时区对象
            tz_utc_8 = timezone(timedelta(hours=8))
            
            # 将时间戳转换为北京时间
            published_at = datetime.fromtimestamp(item['display_time'], tz=tz_utc_8)
            news['publish_time'] = published_at.strftime('%Y-%m-%d %H:%M:%S')
            
            news['uri'] = item['uri']
            
            yield news 