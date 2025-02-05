BOT_NAME = 'wscn_spider'

SPIDER_MODULES = ['wscn_spider.spiders']
NEWSPIDER_MODULE = 'wscn_spider.spiders'

# 遵守 robots.txt 规则
ROBOTSTXT_OBEY = True

# 配置 pipeline
ITEM_PIPELINES = {
   'wscn_spider.pipelines.MySQLPipeline': 300,
}

# 设置下载延迟
DOWNLOAD_DELAY = 1

# 请求头
DEFAULT_REQUEST_HEADERS = {
   'Accept': 'application/json',
   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
} 