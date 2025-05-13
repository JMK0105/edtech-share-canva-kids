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
prompt_input = st.text_area("✍️ GPT 프롬프트", """
PDF 전체 내용을 바탕으로 8~10장의 발표 슬라이드를 구성해주세요.

- '제목'과 '영문제목'은 모든 슬라이드에서 동일합니다 (국문/영문 세션 제목).
- 각 슬라이드의 '키워드'는 해당 슬라이드의 주제를 소제목 형태로 작성해주세요. (예: ROI 방법론을 통한 단계별 목표수립 과정)
- '내용'은 키워드에 대한 구체적 설명입니다. 발표자가 전달할 내용이라고 생각하고, 2~5문장 이내로 요약해주세요.
- 특히, 본문 내용은 자연스럽게 줄바꿈이 되도록 구성해주세요. (예: 문장마다 줄 바꿈)

다음 형식을 지켜 출력해주세요:

[슬라이드 1]
제목: 학습, TD의 영향력 및 ROI 입증 방법
영문제목: Demonstrate the Impact and ROI of Learning and Talent Development
키워드: ROI 방법론을 통한 단계별 목표수립 과정
내용: 각 단계별 교육 프로그램의 효과를 체계적으로 평가하고 명확한 데이터를 바탕으로 프로그램의 경제적 가치 입증 및 전략적 목표 달성에 기여

(슬라이드 개수는 적절히 조정해주세요)
""")

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
