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
당신은 글로벌 HRD 컨퍼런스 발표 자료를 분석하여 국내 금융사 L&D 담당자에게 제공할 디브리핑 보고서를 작성하는 전문가입니다.

지금부터 제공하는 ATD 25 세션의 PDF 발표 자료를 기반으로 아래 기준에 따라 요약 보고서를 작성해주세요:

---

1️⃣ [세션 개요 요약]
- 세션의 목적, 핵심 화두, 전체 흐름을 간단히 요약해주세요.
- 세션의 영어 제목과 그에 해당하는 자연스러운 한국어 제목 번역을 함께 제공해주세요.

---

2️⃣ [핵심 슬라이드 요약]
- 전체 슬라이드 중 핵심 슬라이드 3~5장을 선택해주세요. (더 많아도 괜찮습니다)
- 각 슬라이드별로 슬라이드 번호를 표시하고, 원문 핵심 메시지를 자연스럽게 한국어로 번역해 설명해주세요.
- 설명은 '핵심 메시지 + 의미 해석'의 흐름을 따르며, 실무자가 이해할 수 있는 깊이로 작성해주세요.
- '제목'과 '영문제목'은 모든 슬라이드에서 동일합니다 (국문/영문 세션 제목).
- 각 슬라이드의 '키워드'는 해당 슬라이드의 주제를 소제목 형태로 작성해주세요. (예: ROI 방법론을 통한 단계별 목표수립 과정)
---

3️⃣ [국내 금융사 L&D 시사점]
- 국내 금융 산업에 종사하는 L&D 담당자가 참고할 만한 시사점을 정리해주세요.
- 전략 수립, 프로그램 설계, 교육성과 보고 측면에서 실용적 인사이트를 제시해주세요.

---

출력 형식 예시:

[세션 개요]
영문 제목: Demonstrate the Impact and ROI of Learning and Talent Development
국문 제목: 학습, TD의 영향력 및 ROI 입증 방법
요약: ROI Instiute,lnc의 공동창립자이며 CEO이자 교육측정 및 평가분야에서 국제적으로 인정받는 리더이며, 교육 프로그램의 경제적 가치를 평가하는데 큰 기여를한 Patti P. Phillips의 세션

[핵심 슬라이드 요약]
(슬라이드 3)
영문 제목: Demonstrate the Impact and ROI of Learning and Talent Development
국문 제목: 학습, TD의 영향력 및 ROI 입증 방법
키워드: ROI 방법론을 통한 단계별 목표수립 과정
내용: 각 단계별 교육 프로그램의 효과를 체계적으로 평가하고 명확한 데이터를 u卜탕으로 프로그램의 경제적 가치 입증 및 전략적 목표 달성에 기여

(슬라이드 5)
영문 제목: Demonstrate the Impact and ROI of Learning and Talent Development
국문 제목: 학습, TD의 영향력 및 ROI 입증 방법
키워드: Phillips’ ROI Methodology (필립스의 ROI 방법론)
내용: 교육 프로그램에 투입되는 비용을 실제 성과와 연결하여 교육의 금전적 실제 가치 즉, 투자수익률(R0I)을 확인하기 위한 방법론
비생산적인, 수익률이 낮은 교육 프로그램을 예측하고 진행 여부를 결정하는데 도움이 됨.

[시사점]
- 기존에 평가 및 분석의 어려움으로 R0I 측정을 망설였다면 Phillips ROI 모델을 참고/적용하여 교육 프로그램을 기획/수행해 볼 것을 권함. 
- 다만 ROI측정이 교육 효과성 평가의 만능이 될 수 없기 때문에 다양한평가 방법(설문조사, 시험, 직무 수행, 실습 평가)을 적절히 활용하여 비즈니스 성과를 높이고 조직의 성장과 발전을 이끌어 나갈 수 있는 교육을 기획할 수 있음.
""")

if st.button("🔄 슬라이드 생성") and pdf_file:
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(pdf_file.read())
        pdf_text = extract_text_from_pdf(tmp.name)

    with st.spinner("🤖 GPT가 내용을 요약하고 있습니다..."):
        gpt_response = summarize_text_to_slides(pdf_text, prompt_input)
        st.session_state["gpt_response"] = gpt_response
        slides_data = parse_structured_slides(gpt_response)

    with st.spinner("🧩 슬라이드에 내용 삽입 중..."):
        prs = insert_structured_content(template_path, slides_data)
        output_path = "generated_slides.pptx"
        prs.save(output_path)

    st.success("✅ 슬라이드 생성 완료!")
    with open(output_path, "rb") as f:
        st.download_button("📥 PPTX 파일 다운로드", f, file_name="ATD_Debriefing.pptx")

if "gpt_response" in st.session_state:
    st.text_area("📋 GPT 응답 미리보기", st.session_state["gpt_response"], height=400)
