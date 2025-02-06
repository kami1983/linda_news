from quart import Quart, request, jsonify
from datetime import datetime
from openai import OpenAI
import asyncio
import aiomysql
import os
from config import get_db_pool  # 假设配置在 config.py 中

app = Quart(__name__)

DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')

@app.route('/api/ai', methods=['POST'])
async def ai():
    '''
    # Please install OpenAI SDK first: `pip3 install openai`
    from openai import OpenAI
    client = OpenAI(api_key="<DeepSeek API Key>", base_url="https://api.deepseek.com")
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "Hello"},
        ],
        stream=False
    )
    print(response.choices[0].message.content)
    '''
    try:
        # 获取 post 请求的 input 参数
        data = await request.json
        print(data)

        client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": "Hello"},
            ],
            stream=False
        )
        return jsonify({
            'code': 200,
            'message': response.choices[0].message.content
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': str(e)
        }), 500
    

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