from quart import Quart, request, jsonify
from datetime import datetime
from openai import OpenAI
import asyncio
import aiomysql
import os
from config import get_db_pool  # 假设配置在 config.py 中

app = Quart(__name__)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_REQUEST_URI = os.getenv('OPENAI_REQUEST_URI')
OPENAI_MODEL = os.getenv('OPENAI_MODEL')
GEMMA2_9b_MODEL = os.getenv('GEMMA2_9b_MODEL')

@app.route('/api/ai/importance', methods=['POST'])
async def ai_importance():
    try:
        # 获取 post 请求的 input 参数
        data = await request.json
        if data['content'] == '':
            return jsonify({
                'code': 400,
                'message': 'content 不能为空'
            }), 400
        
        ai_action = '分析新闻对投资大影响程度，思考对于投资是利空还是利好，明确告诉这个新闻是利空还是利好，之后给出重要性评分，从1到100，1表示完全不重要，100表示非常重要，还需要给出其重要的原因，不重要的原因'

        client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_REQUEST_URI)
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": ai_action},
                {"role": "user", "content": data['content']},
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
    
@app.route('/api/ai/gemma2_9b_importance', methods=['POST'])
async def ai_gemma2_9b_importance():
     # 获取 post 请求的 input 参数
    try:
        data = await request.json
        if data['content'] == '':
            return jsonify({
                'code': 400,
                'message': 'content 不能为空'
            }), 400
        
        ai_action = '分析新闻对投资大影响程度，思考对于投资是利空还是利好，明确告诉这个新闻是利空还是利好，之后给出重要性评分，从1到100，1表示完全不重要，100表示非常重要，除了评分数字其他的不要输出，只输出分数数字'

        client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_REQUEST_URI)
        response = client.chat.completions.create(
            model=GEMMA2_9b_MODEL,
            messages=[
                {"role": "system", "content": ai_action},
                {"role": "user", "content": data['content']},
            ],
            stream=False
        )

        return jsonify({
            'code': 200,
            'message': int(response.choices[0].message.content)
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': str(e)
        }), 500


@app.route('/api/ai/news', methods=['POST'])
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
        if data['content'] == '':
            return jsonify({
                'code': 400,
                'message': 'content 不能为空'
            }), 400
        
        ai_action = '分析新闻：对宏观环境的影响，对微观行业的影响，对投资者情绪对影响。投资方面：提示可能的潜在风险，提出几个头脑风暴问题，给出几个投资机会和建议'

        client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_REQUEST_URI)
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": ai_action},
                {"role": "user", "content": data['content']},
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
        
        # 执行 SQL 查询，并且添加列信息
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

@app.route('/api/upload-csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({'message': '没有文件上传'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': '没有选择文件'}), 400

    if file and file.filename.endswith('.csv'):
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        return jsonify({'message': '文件上传成功'}), 200

    return jsonify({'message': '文件格式不正确'}), 400

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