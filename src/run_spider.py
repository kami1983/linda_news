import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from wscn_spider.spiders.news_spider import NewsSpider as WscnNewsSpider

def run_spider():
    # 设置项目根目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # 创建新的 CrawlerProcess
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(WscnNewsSpider)
    process.start()

if __name__ == '__main__':
    run_spider() 