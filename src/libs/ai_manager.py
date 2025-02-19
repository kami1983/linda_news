
import os
from openai import OpenAI

from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

from libs.constants import CSV_TYPE_CATEGORY, CSV_TYPE_CONCEPT
from libs.csv_manager import readCsvData

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_REQUEST_URI = os.getenv('OPENAI_REQUEST_URI')
AI_R_MODEL = os.getenv('AI_R_MODEL')
AI_V_MODEL = os.getenv('AI_V_MODEL')

async def aiRModleAssister(content, action):
    return await aiAssister(content, action, AI_R_MODEL)
    
async def aiVModleAssister(content, action):
    return await aiAssister(content, action, AI_V_MODEL)

async def aiAssister(content, action, model):
    print(f'AI_MODEL: {model}')
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


class ResponseObject:
    def __init__(self, content, reasoning_content):
        self.content = content
        self.reasoning_content = reasoning_content

async def streamAiAssister(input, action, model):
    client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_REQUEST_URI)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": action},
            {"role": "user", "content": input},
        ],
        stream=True
    )

    content=''
    reasoning_content=''

    # 逐步接收并处理响应
    for chunk in response:
        if chunk.choices[0].delta.content:
            content += chunk.choices[0].delta.content
        if chunk.choices[0].delta.reasoning_content:
            print({chunk.choices[0].delta.reasoning_content})
            reasoning_content += chunk.choices[0].delta.reasoning_content
    
    return ResponseObject(content, reasoning_content)


def constructAiActionOfExtractCategory():
    # 调用 read_csv_data 接口
    category_list = readCsvData(['行业'], CSV_TYPE_CATEGORY)
    if category_list is None or len(category_list) == 0:
        raise Exception('category_list is None')
    
    # category_list 是二维数组，需要转换成一维数组
    category_list = [item for sublist in category_list for item in sublist]
    category_str = '|'.join(category_list)
    
    # action= f'根据新闻内容，判断新闻与那个行业最相关，行业列表：{category_str}，输出一个最相关的行业名称，然后针对这个行业回答：利空|看平|利好，其中的一个，格式：行业名称 利空，输出的概念必须在行业列表中，不要输出其他内容'

    action= f'{category_str}'
    return action
def constructAiActionOfExtractConcepts():
    # 调用 read_csv_data 接口
    concept_list = readCsvData(['行业'], CSV_TYPE_CONCEPT)
    if concept_list is None or len(concept_list) == 0:
        raise Exception('concept_list is None')
    
    # concept_list 是二维数组，需要转换成一维数组
    concept_list = [item for sublist in concept_list for item in sublist]
    concept_str = '|'.join(concept_list)
    # action =  f'根据新闻内容，判断新闻与那个概念最相关，概念列表：{concept_str}，观点：利空|看平|利好，(输出不超过三个最相关的概念名称 观点，用|隔开)，格式：概念名称1 利空|概念名称2 看平|概念名称3 利好，不要输出其他内容'
    # action= f'概念列表用|分开如下：{concept_str}，输出三个与新闻最相关的概念名称，然后针对每个概念回答：利空|看平|利好，其中的一个，格式：概念名称1 利空|概念名称2 看平|概念名称3 利好，输出的概念必须在概念列表中，不要输出其他内容'
    action= f'{concept_str}'
    return action

async def extractCategoryFromNews(news_content):
    ai_action = constructAiActionOfExtractCategory()
    # message = await aiRModleAssister(news_content, ai_action)
    # category = message.content.split('</think>')[1].strip().strip('\t')
    message = await aiVModleAssister(f"新闻：{news_content}\n\n要求：根据新闻内容，判断新闻与那个行业最相关，行业从系统中选择已有的，没有就不输出不要随意输出，输出格式：行业名称，只输出一个最相关的行业，不要输出其他内容", f'行业列表 {ai_action}')
    category = message.content
    return category

async def extractConceptsFromNews(news_content):
    ai_action = constructAiActionOfExtractConcepts()
    # message = await aiRModleAssister(news_content, ai_action)
    # concepts = message.content.split('</think>')[1].strip().strip('\t')
    message = await aiVModleAssister(f"新闻：{news_content}\n\n要求：根据新闻内容，获取与新闻最相关的3个概念，概念系统中选择已有的，没有就不输出不要随意输出，输出格式：概念名称1,概念名称2,概念名称3，不要输出其他内容", f'概念列表 {ai_action}')
    concepts = message.content
    return concepts
