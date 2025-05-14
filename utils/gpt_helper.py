# 📁 utils/gpt_helper.py
from openai import OpenAI
import streamlit as st

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def summarize_text_to_slides(text, instruction):
    """
    GPT에게 텍스트와 프롬프트를 입력하여 슬라이드 형식 응답을 생성합니다.
    """
    messages = [
        {"role": "system", "content": "당신은 ATD25의 세션 자료를 기반으로 핵심 메시지, 적용 사례, 전략적 의미, 수치 근거를 구조화하여 설득력 있는 발표 슬라이드를 구성하는 HRD전문가입니다."},
        {"role": "user", "content": f"{instruction.strip()}\n\n{text.strip()}"}
    ]
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=messages,
        max_tokens=3000
    )
    return response.choices[0].message.content


def parse_structured_slides(gpt_response):
    """
    GPT 응답 문자열을 슬라이드 딕셔너리 리스트로 파싱합니다.
    줄바꿈(\n)은 문자열로 그대로 유지되어야 합니다.
    """
    slides = []
    title_kr_global = ""
    title_en_global = ""
    slide_blocks = gpt_response.strip().split("[슬라이드")

    for block in slide_blocks[1:]:  # 첫 조각은 빈 문자열이므로 무시
        title_kr, title_en, content, keywords = "", "", "", ""
        lines = block.splitlines()
        content_lines = []
        content_started = False

        for line in lines:
            line = line.strip()
            if line.startswith("국문제목:"):
                title_kr = line.replace("국문제목:", "").strip()
                if not title_kr_global:
                    title_kr_global = title_kr
            elif line.startswith("영문제목:"):
                title_en = line.replace("영문제목:", "").strip()
                if not title_en_global:
                    title_en_global = title_en
            elif line.startswith("키워드:"):
                keywords = line.replace("키워드:", "").strip()
            elif line.startswith("내용:"):
                content_line = line.replace("내용:", "").strip()
                if content_line:
                    content_lines.append(content_line)
                content_started = True
            elif content_started:
                content_lines.append(line)

        # 핵심: 줄바꿈을 문자열 "\\n"으로 유지해야 PPT 삽입 시 줄바꿈 가능
        content = "\\n".join([l.strip() for l in content_lines if l.strip()])

        slides.append({
            "title_kr": title_kr_global,
            "title_en": title_en_global,
            "content": content,
            "keywords": keywords
        })

    return slides
