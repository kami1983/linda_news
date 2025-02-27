import csv
from quart import Quart, make_response, request, jsonify
from datetime import datetime, timedelta, timezone
from openai import OpenAI
from functools import wraps
import jwt
import asyncio
import aiomysql
import os
from libs.ai_manager import constructAiActionOfExtractCategory, constructAiActionOfExtractConcepts, aiVModleAssister, aiRModleAssister, extractCategoryFromNews, extractConceptsFromNews
from .config import get_db_pool
from libs.constants import CONST_DB_PUBLIC_LABEL_CSV_LABEL_NAME, CSV_TYPE_CATEGORY, CSV_TYPE_CONCEPT
from libs.csv_manager import getCsvFilePath, getCsvValueByColname, makeCsvLablePath, modifyCsvHeaders, readCsvData  
from libs.auth import generate_token, decode_token, login_required
from dotenv import load_dotenv

from libs.db_conn import addCsvRecord, getScvLabel, readCsvRecordData, updatePublicLabel

# 加载环境变量
load_dotenv()

app = Quart(__name__)

# Mock database for user credentials
admin_user = os.getenv('ADMIN_USER', 'admin')
admin_password = os.getenv('ADMIN_PASSWORD', '123456')
USERS = {
    admin_user: admin_password
}

# Login endpoint
@app.route('/api/login', methods=['POST'])
async def login():
    data = await request.json
    username = data.get("username")
    password = data.get("password")

    # Validate user credentials
    if username in USERS and USERS[username] == password:
        token = generate_token(username)
        response = await make_response(jsonify({"message": "Login successful"}))
        response.set_cookie("auth_token", token, httponly=True)
        return response
    return jsonify({"error": "Invalid credentials"}), 401

# 获取当前登录的用户
@app.route('/api/current_user', methods=['GET'])
async def current_user():
    token = request.cookies.get("auth_token")
    if not token:
        # 如果没有 token，直接返回未授权状态
        return jsonify({"status": False, "message": "Unauthorized"}), 200

    try:
        # 解码 token，decode_token 应该是一个实现了 JWT 解码逻辑的方法
        user_data = decode_token(token)
        if not user_data:
            return jsonify({"status": False, "message": "Invalid or expired token"}), 200
        
        # 返回解码后的用户数据
        return jsonify({"status": True, "data": user_data}), 200
    except Exception as e:
        # 捕获潜在的解码异常（比如格式错误、过期等）
        return jsonify({"status": False, "message": str(e)}), 200


# Logout endpoint
@app.route('/api/logout', methods=['POST'])
async def logout():
    response = await make_response(jsonify({"message": "Logged out"}))
    response.delete_cookie("auth_token")
    return response


# Protected API endpoint
@app.route('/api/protected', methods=['GET'])
@login_required
async def protected(user_data):
    token = request.cookies.get("auth_token")
    if not token:
        return jsonify({"error": "Unauthorized"}), 401
    
    user_data = decode_token(token)
    if not user_data:
        return jsonify({"error": "Invalid or expired token"}), 401

    return jsonify({"message": f"Hello, {user_data['username']}!"})


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

        # client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_REQUEST_URI)
        # response = client.chat.completions.create(
        #     model=OPENAI_MODEL,
        #     messages=[
        #         {"role": "system", "content": ai_action},
        #         {"role": "user", "content": data['content']},
        #     ],
        #     stream=False
        # )

        message = await aiRModleAssister(data['content'], ai_action)

        return jsonify({
            'code': 200,
            'message': message
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

        message = await aiVModleAssister(data['content'], ai_action)

        return jsonify({
            'code': 200,
            'message': int(message)
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

        message = await aiRModleAssister(data['content'], ai_action)
        return jsonify({
            'code': 200,
            'message': message
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
        # date = request.args.get('date', '')
        columns = request.args.get('list', 'content,uri,publish_time,id').split(',')

        # 获取查询参数
        start = request.args.get('start', 0, type=int)
        size = request.args.get('size', 10, type=int)

        # 构建 SQL 查询 
        # SELECT * 
        # FROM linda_news.linda_news 
        # WHERE 
        # publish_time >= CURDATE() 
        # AND publish_time < CURDATE() + INTERVAL 1 DAY
        # ORDER BY 
        # publish_time DESC;
        allowed_columns = {'id', 'title', 'content', 'publish_time', 'author', 'uri'}
        valid_columns = [col for col in columns if col in allowed_columns]
        
        # 获取数据库连接池
        pool = await get_db_pool()
        
        # 构建 SQL 查询
        query = f"SELECT {', '.join(valid_columns)} FROM linda_news.linda_news"
        query += f" ORDER BY publish_time DESC LIMIT {start}, {size}"
        
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
    

@app.route('/api/ai_category', methods=['POST'])
async def ai_category():
    '''
    This API is used to determine the category of the news.
    Input: 
    {
        "content": "Text"
    }
    Output:
    {
        "category": "Text"
    }
    '''
    data = await request.json
    if data['content'] == '':
        return jsonify({
            'code': 400,
            'message': 'content 不能为空'
        }), 400
    
    # 从OpenAI获取行业
    # message = await aiVModleAssister(f"新闻：{data['content']}\n\n要求：根据新闻内容，判断新闻与那个行业最相关，行业从系统中选择已有的，没有就不输出不要随意输出，输出格式：行业名称 利空|看平|利好，其中的一个，不要输出其他内容",f'行业列表：{constructAiActionOfExtractCategory()}')
    message = await extractCategoryFromNews(data['content'])
    print('DEBUG: message', message)
    return jsonify({
        'code': 200,
        'message': message
    }), 200
    
@app.route('/api/ai_concepts', methods=['POST'])
async def ai_concepts():
    '''
    This API is used to determine the concepts of the news.
    Input: 
    {
        "content": "Text"
    }
    Output:
    {
        "concepts": ["Text1", "Text2", "Text3"]
    }
    '''
    data = await request.json
    if data['content'] == '':
        return jsonify({
            'code': 400,
            'message': 'content 不能为空'
        }), 400
    
    # 从OpenAI获取概念
    # message = await aiVModleAssister(f"新闻：{data['content']}\n\n要求：根据新闻内容，获取与新闻最相关的3个概念，概念系统中选择已有的，没有就不输出不要随意输出，输出格式：概念名称1 利空|看平|利好, 概念名称2 利空|看平|利好, 概念名称3 利空|看平|利好，不要输出其他内容", f'概念列表 {constructAiActionOfExtractConcepts()}')
    message = await extractConceptsFromNews(data['content'])
    print('DEBUG: message', message)
    return jsonify({
        'code': 200,
        'message': message
    }), 200
    
@app.route('/api/what_category', methods=['POST'])
async def what_category():
    '''
    This API is used to determine the category of the news.
    Input: 
    {
        "news_id": "Text"
    }
    Output:
    {
        "category": "Text"
    }
    '''
    data = await request.json
    if data['news_id'] == '':
        return jsonify({
            'code': 400,
            'message': 'news_id 不能为空'
        }), 400
    
    # 从数据表 linda_news_category 中查询 news_id 对应的 category
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT category, csv_label FROM linda_news_category WHERE news_id = %s", (data['news_id'],))
            result = await cur.fetchone()
            category = result[0] if result else '-'
            csv_label = int(result[1]) if result else 0
            if csv_label > 0:
                pb_values = getCsvValueByColname('行业', category, ['PB.加权','PB.加权.百分位','股息','ROE'], CSV_TYPE_CATEGORY, csv_label)
            else:
                pb_values = []

            if result and result[0] != '':
                return jsonify({
                    'code': 200,
                    'message': [category, pb_values]
                }), 200
            else:
                return jsonify({
                    'code': 200,
                    'message': []
                }), 200
            
@app.route('/api/what_concepts', methods=['POST'])
async def what_concepts():
    '''
    This API is used to determine the concepts of the news.
    Input: 
    {
        "news_id": "Text"
    }
    Output:
    {
        "concepts": ["Text1", "Text2", "Text3"]
    }
    '''
    data = await request.json
    if data['news_id'] == '':
        return jsonify({
            'code': 400,
            'message': 'news_id 不能为空'
        }), 400
    
    # 从数据表 linda_news_concepts 中查询 news_id 对应的 concepts
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT concepts, csv_label FROM linda_news_concepts WHERE news_id = %s", (data['news_id'],))
            result = await cur.fetchone()
            concepts = result[0].split(',') if result else []
            csv_label = int(result[1]) if result else 0
            pb_values = []
            if csv_label > 0:
                for concept in concepts:
                    _pb_values = getCsvValueByColname('行业', concept, ['PB.加权','PB.加权.百分位','股息','ROE'], CSV_TYPE_CONCEPT, csv_label)
                    pb_values.append((concept, _pb_values))

            if result and result[0] != '':
                return jsonify({
                    'code': 200,
                    'message': pb_values
                }), 200
            else:
                return jsonify({
                    'code': 200,
                    'message': []
                }), 200

@app.route('/api/get_csv_record_data', methods=['GET'])
async def get_csv_record_data():
    '''
    This API is used to get the CSV record data.
    '''
    start = request.args.get('start', 0, type=int)
    limit = request.args.get('limit', 10, type=int)
    # 读取csv record 记录 
    csv_record_data = readCsvRecordData(start, limit)
    return jsonify({
        'code': 200,
        'message': csv_record_data
    }), 200

@app.route('/api/get_csv_label', methods=['GET'])
async def get_csv_label():  
    '''
    This API is used to get the CSV label.
    CSV label is used to determine the CSV file version.
    '''
    return jsonify({
        'code': 200,
        'message': getScvLabel()
    }), 200

@app.route('/api/rebuild_csv_heads', methods=['GET'])
@login_required
async def rebuild_csv_heads(user_data):
    '''
    This API is used to reconstruct the CSV file.
    '''
    csv_label = request.args.get('label', 0, type=int)
    system_csv_label = getScvLabel()

    if system_csv_label >= csv_label:
        return jsonify({
            'code': 400,
            'message': f'CSV label is not greater than the system [{system_csv_label}] CSV label [{csv_label}]'
        }), 400

    # modifyCsvHeaders
    modifyCsvHeaders(getCsvFilePath(CSV_TYPE_CATEGORY), makeCsvLablePath(CSV_TYPE_CATEGORY, csv_label))
    modifyCsvHeaders(getCsvFilePath(CSV_TYPE_CONCEPT), makeCsvLablePath(CSV_TYPE_CONCEPT, csv_label))
    updatePublicLabel(CONST_DB_PUBLIC_LABEL_CSV_LABEL_NAME, csv_label)
    addCsvRecord(csv_label, datetime.now().strftime('%Y-%m-%d'))

    return jsonify({
        'code': 200,
        'message': f'CSV 文件头重建成功，当前版本号：{csv_label}'
    }), 200

@app.route('/api/upload_csv', methods=['POST'])
@login_required
async def upload_csv(user_data):
    '''
    # 上传概念数据 CSV
    curl -F "file=@path/to/your/concept.csv" -F "type=1" http://localhost:5001/api/upload_csv

    # 上传行业数据 CSV
    curl -F "file=@path/to/your/category.csv" -F "type=2" http://localhost:5001/api/upload_csv

    # 上传无效类型
    curl -F "file=@path/to/your/file.csv" -F "type=3" http://localhost:5001/api/upload_csv
    '''
    
    files = await request.files
    if 'file' not in files:
        return jsonify({'code': 400, 'message': 'No file part'}), 400

    file = files['file']
    if file.filename == '':
        return jsonify({'code': 400, 'message': 'No selected file'}), 400

    form = await request.form
    type = form.get('type', type=int)
    file_path = getCsvFilePath(type)
    await file.save(file_path)

    return jsonify({'code': 200, 'message': 'File uploaded successfully'})

@app.route('/api/read_csv_data', methods=['GET'])
async def read_csv_data():
    '''
    This API is used to read the category data.
    '''
    columns = request.args.get('list', '行业').split(',')
    type = request.args.get('type', 1, type=int)
    label = request.args.get('label', 0, type=int)

    if type not in [1, 2]:
        return jsonify({'code': 400, 'message': 'Invalid type parameter'}), 400

    try:
        data = readCsvData(columns, type, label)
        return jsonify({'code': 200, 'data': data})
    except Exception as e:
        return jsonify({'code': 500, 'message': str(e)}), 500


@app.errorhandler(404)
async def not_found(error):
    return jsonify({'code': 404, 'message': 'Interface not found'}), 404

@app.errorhandler(405)
async def method_not_allowed(error):
    return jsonify({'code': 405, 'message': 'Request method not allowed'}), 405

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)