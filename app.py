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
PDF 전체 내용을 분석하고, 해당 내용에 대해 발표할 8~10장의 슬라이드를 구성해주세요.

🟩 공통 조건:
- '제목'과 '영문제목'은 모든 슬라이드에서 동일합니다 (국문/영문 세션 제목).
- 각 슬라이드는 하나의 주제(소제목)를 중심으로 구성되어야 하며, 해당 소제목은 '키워드' 항목에 작성해주세요.

🟦 '키워드' 항목 작성 방식:
- 슬라이드에서 강조하고 싶은 중심 주제를 한 문장 소제목 형식으로 작성
- 예: 조직 내 Phillips ROI 모델 활용 효과

🟧 '내용' 항목 작성 방식:
- 해당 키워드에 대해 설명하는 발표용 본문입니다.
- 아래 3가지 요소를 모두 포함해주세요:
  1. 핵심 개념이나 이론의 정의 또는 필요성
  2. 관련 통계, 사례, 시사점 (있는 경우)

- 전체 3~5문장 이상 작성해주세요.
- 각 문장 끝에는 줄바꿈(\n)을 넣어 주세요.

📝 출력 형식 예시:

[슬라이드 1]
제목: 학습, TD의 영향력 및 ROI 입증 방법
영문제목: Demonstrate the Impact and ROI of Learning and Talent Development
키워드: 시사점
내용: ROI Institute 연구에 따르면 조직 내 리더들은 교육 진행을 위한 예산 수립에 있어, \n
가장 먼저 교육이 실제 비즈니스 성과로 이어질 수 있는지에 대한 교육투자 가치에 대해 가장 중요하게 생각하고 있으며, \n
실제로 96%의 리더들은 교육 계획 수립 시 사전에 교육투자 가치(R0I)가 평가되어야 한다고 함.\n
ROI 측정을 통해 실제 교육 효과에 대한 평가를 체계적으로 관리하고, \n
무엇보다 교육 기획 단계에서 R0I를 고려하여 진행여부를 판단한다면 효율적 예산 관리 및 긍정적인 학습 문화조성에 기여할 수 있을 것임.

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
