import os
import pymysql
from datetime import datetime
from libs.db_conn import getDbConn


class MySQLPipeline:
    def __init__(self):
        self.conn = None
        self.cur = None

    def open_spider(self, spider):
        self.conn = getDbConn()
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        sql = """
        INSERT INTO linda_news (item_id, title, content, author, publish_time, uri) 
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        title = VALUES(title),
        content = VALUES(content),
        author = VALUES(author),
        publish_time = VALUES(publish_time),
        uri = VALUES(uri)
        """
        try:
            self.cur.execute(sql, (
                item['item_id'],
                item['title'],
                item['content'],
                item['author'],
                item['publish_time'],
                item['uri']
            ))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            spider.logger.error(f"Error saving item to MySQL: {e}")
        return item

    def close_spider(self, spider):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close() 