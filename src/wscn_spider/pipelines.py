import json
from datetime import datetime

class JsonWriterPipeline:
    def open_spider(self, spider):
        # 爬虫启动时打开文件
        self.file = open('news.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        # 处理每一条数据
        item_dict = dict(item)
        item_dict['publish_time'] = item_dict['publish_time'].isoformat()
        line = json.dumps(item_dict, ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def close_spider(self, spider):
        # 爬虫结束时关闭文件
        self.file.close() 