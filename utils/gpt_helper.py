import openai
import os

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_text(text, instruction):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "당신은 발표용 자료 요약 전문가입니다."},
            {"role": "user", "content": f"{instruction}\n\n{text}"}
        ],
        max_tokens=1500
    )
    return response.choices[0].message.content
