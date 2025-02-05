from quart import Quart, request, jsonify
from datetime import datetime
import asyncio
import aiomysql
import os
from config import get_db_pool  # 假设配置在 config.py 中

app = Quart(__name__)

@app.route('/api/news', methods=['GET'])
async def get_news():
    try:
        # 获取查询参数
        date = request.args.get('date', '')
        columns = request.args.get('list', 'content,uri,publish_time').split(',')

        # 验证日期格式
        try:
            if date:
                datetime.strptime(date, '%Y-%m-%d')
            else:
                date = datetime.now().strftime('%Y-%m-%d')
        except ValueError:
            return jsonify({
                'code': 400,
                'message': '日期格式错误，请使用 YYYY-MM-DD 格式'
            }), 400

        print(date)

        # 构建 SQL 查询 
        # SELECT * 
        # FROM linda_news.linda_news 
        # WHERE 
        # publish_time >= CURDATE() 
        # AND publish_time < CURDATE() + INTERVAL 1 DAY
        # ORDER BY 
        # publish_time DESC;
        allowed_columns = {'id', 'item_id', 'title', 'content', 'publish_time', 'author', 'uri'}
        valid_columns = [col for col in columns if col in allowed_columns]
        
        # 获取数据库连接池
        pool = await get_db_pool()
        
        # 构建 SQL 查询
        query = f"SELECT {', '.join(valid_columns)} FROM linda_news.linda_news"
        
 
        # 添加日期过滤条件
        if date:
            query += f" WHERE publish_time >= '{date}'"
            query += f" AND publish_time < '{date}' + INTERVAL 1 DAY"

        query += " ORDER BY publish_time DESC"

        print(query)
        
        # 执行 SQL 查询
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query)
                result = await cur.fetchall()

        return jsonify(result)  
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': str(e)
        }), 500

        

@app.errorhandler(404)
async def not_found(error):
    return jsonify({
        'code': 404,
        'message': '接口不存在'
    }), 404

@app.errorhandler(405)
async def method_not_allowed(error):
    return jsonify({
        'code': 405,
        'message': '请求方法不允许'
    }), 405

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)