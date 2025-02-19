import asyncio
from datetime import datetime
import os
import time
import subprocess
import sys

from libs.ai_manager import extractCategoryFromNews, extractConceptsFromNews
from libs.csv_manager import filterCsvData
from libs.db_conn import getDbConn

CONST_MAX_FILL_COUNT = 10

async def run_ai_filler():
    '''
    填充新闻分类和概念
    '''
    conn = getDbConn()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id, news_id FROM linda_news_category WHERE status = 0 ORDER BY id DESC LIMIT %s", (CONST_MAX_FILL_COUNT,))
        # 获取最新的 news_id
        news_ids = cursor.fetchall()
        news_ids = [news[1] for news in news_ids]
        news_ids_str = ','.join(map(str, news_ids))
        # print(news_ids_str)

        # 查询 news_id 的新闻内容
        cursor.execute(f"SELECT id, content FROM linda_news WHERE id IN ({news_ids_str})")
        news_list = cursor.fetchall()
        for news in news_list:
            
            category = await extractCategoryFromNews(news[1])

            # 过滤 category
            category_list = filterCsvData(['行业'], 1, category)
            db_category = ','.join(category_list)
            
            print('>> category: ', news[0], 'original category=', category, 'record db_category=', db_category)
            cursor.execute("UPDATE linda_news_category SET category = %s, status = 1 WHERE news_id = %s", (db_category, news[0]))

            # 查询 news_id 的新闻概念
            concepts = await extractConceptsFromNews(news[1])
            concepts_list = filterCsvData(['行业'], 2, concepts)
            db_concepts = ','.join(concepts_list)
            print('## concepts: ', news[0], 'original concepts=', concepts, 'record db_concepts=', db_concepts)
            cursor.execute("UPDATE linda_news_concepts SET concepts = %s, status = 1 WHERE news_id = %s", (db_concepts, news[0]))
            conn.commit()

    except Exception as e:
        print(f"Error during query execution: {e}")
    finally:
        conn.close()
        
        
def run_query_news():
    '''
    查询未填充分类和概念的新闻，建立 status = 0 的 linda_news_category 和 linda_news_concepts 数据
    如果 status = 0 的 linda_news_category 和 linda_news_concepts 数据条数超过20条，则停止将更多的数据放到查询队列中
    '''
    conn = getDbConn()
    cursor = conn.cursor()

    try:
        # 查询 status = 0 的条数
        cursor.execute("SELECT COUNT(*) FROM linda_news_category WHERE status = 0")
        category_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM linda_news_concepts WHERE status = 0")
        concepts_count = cursor.fetchone()[0]

        if category_count >= CONST_MAX_FILL_COUNT or concepts_count >= CONST_MAX_FILL_COUNT:
            print("Too many pending entries, skipping fill queue. current queue: category_count: %s, concepts_count: %s" % (category_count, concepts_count))
            return
        
        fill_count = CONST_MAX_FILL_COUNT - category_count

        # 获取最新的 news_id
        # SELECT ln.*
        # FROM linda_news AS ln
        # LEFT JOIN linda_news_category AS lnc ON ln.id = lnc.news_id
        # WHERE lnc.news_id IS NULL
        # ORDER BY ln.id DESC
        # LIMIT 20;
        cursor.execute('''
            SELECT ln.*
            FROM linda_news AS ln
            LEFT JOIN linda_news_category AS lnc ON ln.id = lnc.news_id
            WHERE lnc.news_id IS NULL
            ORDER BY ln.id DESC
            LIMIT %s
        ''', (fill_count,))
       
        news_data = cursor.fetchall()

        # 插入数据到 linda_news_category 和 linda_news_concepts
        for news in news_data:
            news_id = news[0]
            # 检查是否已经存在
            cursor.execute("SELECT 1 FROM linda_news_category WHERE news_id = %s", (news_id,))
            if not cursor.fetchone():
                cursor.execute("INSERT INTO linda_news_category (news_id, category, status) VALUES (%s, %s, 0)", (news_id, '',))

            cursor.execute("SELECT 1 FROM linda_news_concepts WHERE news_id = %s", (news_id,))
            if not cursor.fetchone():
                cursor.execute("INSERT INTO linda_news_concepts (news_id, concepts, status) VALUES (%s, %s, 0)", (news_id, '',))

        conn.commit()
    except Exception as e:
        print(f"Error during query execution: {e}")
    finally:
        conn.close()


async def main():
    while True:
        try:
            print("Filler start at: ", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            # 运行新闻查询
            run_query_news()
            # 运行新闻填充的AI识别内容
            await run_ai_filler()
        except Exception as e:
            print(f"Filler error: {e}")
        
        # 等待指定时间
        time.sleep(int(os.getenv('AI_FILLER_INTERVAL_SECONDS', 60)))

if __name__ == '__main__':
    asyncio.run(main()) 