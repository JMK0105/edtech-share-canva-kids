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
PDF 전체 내용을 바탕으로 6~8장의 발표 슬라이드를 구성해주세요.

- '제목'과 '영문제목'은 모든 슬라이드에서 동일합니다 (국문/영문 세션 제목).
- 각 슬라이드의 '키워드'는 해당 슬라이드의 주제를 소제목 형태로 작성해주세요. (예: ROI 방법론을 통한 단계별 목표수립 과정)

🟧 '내용' 항목 작성 방식:
- 키워드에 대한 개념 정의, 학문적 혹은 전략적 의의, 실천적 시사점을 반드시 포함해주세요.
- 실무자들에게 도움이 되는 5문장 이상의 내용을 구체적으로 설명해주세요.
- 각각의 문장은 줄바꿈(\n)으로 구분해주세요.
- 핵심 주장 → 근거 → 적용 예시 → 시사점의 흐름을 따르세요.

출력 형식 예시:

[슬라이드 1]
제목: 학습, TD의 영향력 및 ROI 입증 방법
영문제목: Demonstrate the Impact and ROI of Learning and Talent Development
키워드: Phillips’ ROI Methodology (필립스의 ROI 방법론)
내용: 교육 프로그램에 투입되는 비용을 실제 성과와 연결하여 교육의 금전적 실제 가치 즉, 투자수익률(ROI)을 확인하기 위한 방법론이다.\n비생산적인, 수익률이 낮은 교육 프로그램을 예측하고 진행 여부를 결정하는 데 도움이 된다.\nPhillips 모델은 반응-학습-행동-성과-ROI의 5단계로 구성된다.\n정량적 결과뿐 아니라 정성적 지표도 함께 분석하여 설득력 있는 평가가 가능하다.\n교육 기획자는 ROI를 기준으로 의사결정을 내릴 수 있어 전략적 설계가 가능하다.
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
