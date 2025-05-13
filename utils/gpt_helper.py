import openai
import os
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")  # 또는 직접 문자열로 삽입

def summarize_text(text, instruction):
    messages = [
        {"role": "system", "content": "당신은 발표 요약 전문가입니다."},
        {"role": "user", "content": f"{instruction}\n\n{text}"}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        max_tokens=1600
    )
    return response['choices'][0]['message']['content']
