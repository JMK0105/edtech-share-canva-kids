import streamlit as st
from utils.pdf_parser import extract_text_from_pdf
from utils.gpt_helper import summarize_text
from utils.ppt_generator import insert_content_to_template
import tempfile
import os

st.set_page_config(page_title="📊 PDF → PPT 자동 생성기")
st.title("📄 PDF 세션 요약 → 🧑‍🏫 발표 PPT 자동 생성")

# 📤 파일 업로드
pdf_file = st.file_uploader("🗂️ 세션 요약 PDF 업로드", type="pdf")
prompt_input = st.text_area("✍️ GPT 요약 프롬프트", "금융 산업 종사자 대상 15분 발표용 PPT를 요약해주세요.")

template_path = "templates/atd_template.pptx.pptx"

if st.button("🔄 슬라이드 생성 시작") and pdf_file:
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(pdf_file.read())
        pdf_text = extract_text_from_pdf(tmp.name)

    with st.spinner("📖 PDF 읽고 GPT 요약 중..."):
        summary = summarize_text(pdf_text, prompt_input)
        slides = summary.strip().split("\n\n")

    with st.spinner("🧩 슬라이드 구성 중..."):
        prs = insert_content_to_template(template_path, slides)
        output_path = "output_slides.pptx"
        prs.save(output_path)

    st.success("✅ PPT 생성 완료!")
    with open(output_path, "rb") as f:
        st.download_button("📥 PPTX 다운로드", f, file_name="debriefing_slides.pptx")
