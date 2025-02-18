
import os
from openai import OpenAI

from libs.csv_manager import readCsvData

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_REQUEST_URI = os.getenv('OPENAI_REQUEST_URI')
OPENAI_MODEL = os.getenv('OPENAI_MODEL')
QWEN_2_5_32b_MODEL = os.getenv('QWEN_2_5_32b_MODEL')
GEMMA2_9b_MODEL = os.getenv('GEMMA2_9b_MODEL')

CSV_TYPE_CATEGORY = 1
CSV_TYPE_CONCEPT = 2

async def openaiAssister(content, action):
    return await aiAssister(content, action, OPENAI_MODEL)
    
async def gemma2Assister(content, action):
    return await aiAssister(content, action, GEMMA2_9b_MODEL)

async def qwenAssister(content, action):
    return await aiAssister(content, action, QWEN_2_5_32b_MODEL)

async def aiAssister(content, action, model):
    # print(f'aiAssister: {content}, {action}, {model}')
    # print(f'OPENAI_API_KEY: {OPENAI_API_KEY}')
    # print(f'OPENAI_REQUEST_URI: {OPENAI_REQUEST_URI}')
    client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_REQUEST_URI)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": action},
            {"role": "user", "content": content},
        ],
        stream=False
    )
    return response.choices[0].message


def constructAiActionOfExtractCategory():
    # 调用 read_csv_data 接口
    category_list = readCsvData(['行业'], CSV_TYPE_CATEGORY)
    if category_list is None or len(category_list) == 0:
        raise Exception('category_list is None')
    
    # category_list 是二维数组，需要转换成一维数组
    category_list = [item for sublist in category_list for item in sublist]
    category_str = '|'.join(category_list)
    
    return f'根据新闻内容，判断新闻与那个行业最相关，行业列表：{category_str}，输出一个最相关的行业名称，不要输出其他内容'

def constructAiActionOfExtractConcepts():
    # 调用 read_csv_data 接口
    concept_list = readCsvData(['行业'], CSV_TYPE_CONCEPT)
    if concept_list is None or len(concept_list) == 0:
        raise Exception('concept_list is None')
    
    # concept_list 是二维数组，需要转换成一维数组
    concept_list = [item for sublist in concept_list for item in sublist]
    concept_str = '|'.join(concept_list)
    return f'根据新闻内容，判断新闻与那个概念最相关，概念列表：{concept_str}，(输出不超过三个最相关的概念名称用,隔开)，不要输出其他内容'

async def extractCategoryFromNews(news_content):
    ai_action = constructAiActionOfExtractCategory()
    # message = await qwenAssister(data['content'], ai_action)
    message = await openaiAssister(news_content, ai_action)
    category = message.content.split('</think>')[1].strip().strip('\t')
    return category

async def extractConceptsFromNews(news_content):
    ai_action = constructAiActionOfExtractConcepts()
    message = await openaiAssister(news_content, ai_action)
    concepts = message.content.split('</think>')[1].strip().strip('\t')
    return concepts
