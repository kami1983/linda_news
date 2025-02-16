import csv
from quart import Quart, request, jsonify
from datetime import datetime
from openai import OpenAI
import asyncio
import aiomysql
import os
from ai_manager import gemma2Assister, openaiAssister
from config import get_db_pool
from csv_manager import getCsvFilePath, readCsvData  

app = Quart(__name__)

# OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
# OPENAI_REQUEST_URI = os.getenv('OPENAI_REQUEST_URI')
# OPENAI_MODEL = os.getenv('OPENAI_MODEL')
# GEMMA2_9b_MODEL = os.getenv('GEMMA2_9b_MODEL')

# UPLOAD_FOLDER = os.getenv('CSV_UPLOAD_FOLDER')
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

CSV_TYPE_CATEGORY = 1
CSV_TYPE_CONCEPT = 2

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

        message = await openaiAssister(data['content'], ai_action)

        return jsonify({
            'code': 200,
            'message': message.content
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

        message = await gemma2Assister(data['content'], ai_action)

        return jsonify({
            'code': 200,
            'message': int(message.content)
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

        message = await openaiAssister(data['content'], ai_action)
        return jsonify({
            'code': 200,
            'message': message.content
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
        columns = request.args.get('list', 'content,uri,publish_time').split(',')

        # 获取查询参数
        start = request.args.get('start', 0, type=int)
        size = request.args.get('size', 10, type=int)


        # # 验证日期格式
        # try:
        #     if date:
        #         datetime.strptime(date, '%Y-%m-%d')
        #     else:
        #         date = datetime.now().strftime('%Y-%m-%d')
        # except ValueError:
        #     return jsonify({
        #         'code': 400,
        #         'message': '日期格式错误，请使用 YYYY-MM-DD 格式'
        #     }), 400

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
 
        # # 添加日期过滤条件
        # if date:
        #     query += f" WHERE publish_time >= '{date}'"
        #     query += f" AND publish_time < '{date}' + INTERVAL 1 DAY"

        query += f" ORDER BY publish_time DESC LIMIT {start}, {size}"

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
    

@app.route('/api/what_category', methods=['POST'])
async def what_category():
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
    
    # 调用 read_csv_data 接口
    category_list = readCsvData(['行业'], CSV_TYPE_CATEGORY)
    if category_list is None or len(category_list) == 0:
        raise Exception('category_list is None')
    
    # category_list 是二维数组，需要转换成一维数组
    category_list = [item for sublist in category_list for item in sublist]
    category_str = '|'.join(category_list)
    
    ai_action = f'根据新闻内容，判断新闻与那个行业最相关，行业列表：{category_str}，输出行业名称，不要输出其他内容'
    message = await openaiAssister(data['content'], ai_action)
    category = message.content.split('</think>')[1].strip().strip('\t')

    return jsonify({
        'code': 200,
        'message': category
    }), 200
    
@app.route('/api/what_concepts', methods=['POST'])
async def what_concepts():
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
    return jsonify({
        'code': 200,
        'message': ['Financial', 'Economy', 'Politics'] 
    }), 200

@app.route('/api/upload_csv', methods=['POST'])
async def upload_csv():
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
    if type not in [1, 2]:
        return jsonify({'code': 400, 'message': 'Invalid type parameter'}), 400

    try:
        data = readCsvData(columns, type)
        return jsonify({'code': 200, 'data': data})
    except Exception as e:
        return jsonify({'code': 500, 'message': str(e)}), 500

    # if type == 1:
    #     filename = 'concept.csv'
    # elif type == 2:
    #     filename = 'category.csv'

    # file_path = os.path.join(UPLOAD_FOLDER, filename)
    # if not os.path.exists(file_path):
    #     return jsonify({'code': 404, 'message': 'File not found'}), 404

    # try:
    #     with open(file_path, mode='r', encoding='utf-8') as csvfile:
    #         reader = csv.DictReader(csvfile)
    #         # 获取所有行的  columns 列 
    #         data = []
    #         for row in reader:
    #             # data.append({col: row[col] for col in columns})
    #             data.append([row[col] for col in columns])
            
    #     return jsonify({'code': 200, 'data': data})
    # except Exception as e:
    #     return jsonify({'code': 500, 'message': f'Error reading file: {str(e)}'}), 500
    


@app.errorhandler(404)
async def not_found(error):
    return jsonify({'code': 404, 'message': '接口不存在'}), 404

@app.errorhandler(405)
async def method_not_allowed(error):
    return jsonify({'code': 405, 'message': '请求方法不允许'}), 405

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)