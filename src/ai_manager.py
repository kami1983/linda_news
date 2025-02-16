
import os
from openai import OpenAI

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_REQUEST_URI = os.getenv('OPENAI_REQUEST_URI')
OPENAI_MODEL = os.getenv('OPENAI_MODEL')
GEMMA2_9b_MODEL = os.getenv('GEMMA2_9b_MODEL')

async def openaiAssister(content, action):
    return await aiAssister(content, action, OPENAI_MODEL)
    
async def gemma2Assister(content, action):
    return await aiAssister(content, action, GEMMA2_9b_MODEL)

async def aiAssister(content, action, model):
    print(f'aiAssister: {content}, {action}, {model}')
    print(f'OPENAI_API_KEY: {OPENAI_API_KEY}')
    print(f'OPENAI_REQUEST_URI: {OPENAI_REQUEST_URI}')
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