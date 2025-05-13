# 📁 utils/gpt_helper.py
import openai
import os

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_text_to_slides(text, instruction):
    messages = [
        {"role": "system", "content": "당신은 발표 슬라이드를 구조화하는 전문가입니다."},
        {"role": "user", "content": f"{instruction}\n\n{text}"}
    ]
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        max_tokens=2000
    )
    return response.choices[0].message.content


def parse_structured_slides(gpt_response):
    slides = []
    slide_blocks = gpt_response.strip().split("[슬라이드")
    for block in slide_blocks[1:]:
        title, content, keywords = "", "", ""
        lines = block.splitlines()
        for line in lines:
            if line.startswith("제목:"):
                title = line.replace("제목:", "").strip()
            elif line.startswith("내용:"):
                content = line.replace("내용:", "").strip()
            elif line.startswith("키워드:"):
                keywords = line.replace("키워드:", "").strip()
        slides.append({"title": title, "content": content, "keywords": keywords})
    return slides
