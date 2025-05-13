import streamlit as st
from utils.pdf_parser import extract_text_from_pdf
from utils.gpt_helper import summarize_text
from utils.ppt_generator import insert_content_to_template
import tempfile

st.title("📊 PDF → PPT 자동 생성 시스템")

pdf_file = st.file_uploader("PDF 세션 파일 업로드", type="pdf")
ppt_template = "templates/atd_template.pptx"
prompt_input = st.text_area("슬라이드 요약 지시 프롬프트", "15분 발표용으로 요약해줘. 슬라이드당 핵심 문장 중심으로 작성해줘.")

if pdf_file:
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(pdf_file.read())
        text = extract_text_from_pdf(tmp.name)

    summary = summarize_text(text, prompt_input)
    slides = summary.strip().split("\n\n")  # 슬라이드별로 나눔

    prs = insert_content_to_template(ppt_template, slides)
    
    pptx_path = "generated_output.pptx"
    prs.save(pptx_path)

    st.success("✅ PPT 슬라이드 생성 완료!")
    with open(pptx_path, "rb") as f:
        st.download_button("📥 PPTX 다운로드", f, file_name="debriefing_output.pptx")
