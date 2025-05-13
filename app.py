# 📁 app.py
import streamlit as st
import tempfile
import os
from utils.pdf_parser import extract_text_from_pdf
from utils.gpt_helper import summarize_text_to_slides, parse_structured_slides
from utils.ppt_generator import insert_structured_content

st.set_page_config(page_title="📊 PDF → PPT 슬라이드 생성기")
st.title("🧠 GPT 기반 발표 슬라이드 자동 생성")

pdf_file = st.file_uploader("📄 세션 PDF 파일 업로드", type="pdf")
template_path = "templates/atd_template.pptx"
prompt_input = st.text_area("✍️ GPT 프롬프트", "다음 세션 요약 내용을 기반으로 8~10장의 발표 슬라이드를 작성해주세요.

각 슬라이드는 다음 형식으로 출력해주세요:

[슬라이드 1]  
제목: 세션의 핵심 내용을 한국어로 요약한 제목  
영문제목: 세션의 원문 제목  
내용: 발표에 사용할 1~2문단 분량의 설명  
키워드: 소제목
")

if st.button("🔄 슬라이드 생성") and pdf_file:
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(pdf_file.read())
        pdf_text = extract_text_from_pdf(tmp.name)

    with st.spinner("🤖 GPT가 내용을 요약하고 있습니다..."):
        gpt_response = summarize_text_to_slides(pdf_text, prompt_input)
        slides_data = parse_structured_slides(gpt_response)

    with st.spinner("🧩 슬라이드에 내용 삽입 중..."):
        prs = insert_structured_content(template_path, slides_data)
        output_path = "generated_slides.pptx"
        prs.save(output_path)

    st.success("✅ 슬라이드 생성 완료!")
    with open(output_path, "rb") as f:
        st.download_button("📥 PPTX 파일 다운로드", f, file_name="ATD_Debriefing.pptx")

