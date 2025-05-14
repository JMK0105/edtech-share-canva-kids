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
영문 제목: Making Sense of Metrics: Proving the Value of Leadership Development
국문 제목: 리더십 개발의 가치와 효과, 데이터를 통해 입증하기
요약: 이 세션은 리더십 개발이 실제 비즈니스 성과와 어떻게 연결되는지를 데이터 기반으로 입증하는 전략을 다룹니다. ROI 관점에서 교육의 설계와 효과 측정을 논의하며, L&D 활동의 전략적 기여를 정량화하는 방법론을 제시합니다.

[핵심 슬라이드 요약]
(슬라이드 3)
핵심 메시지: “Stakeholders care most about behavior change, not just learning satisfaction.”
한국어 번역 및 해석: 이해관계자들은 학습 만족도보다는 실제 행동 변화에 더 큰 가치를 둔다.
의미: 리더십 개발의 결과는 행동 변화로 이어져야 하며, 단순 만족도 조사로는 교육의 효과를 충분히 입증할 수 없다.

(슬라이드 5)
핵심 메시지: “ROI 모델은 리더십 개발의 정당성을 설명하는 데 매우 효과적이다.”
한국어 번역 및 해석: ROI 접근법은 리더십 개발 프로그램의 투자 대비 효과를 명확하게 설명해주는 도구다.
의미: 정량적 지표가 부족한 리더십 교육 분야에서도 ROI 프레임워크를 활용하면 경영진을 설득할 수 있다.

[시사점]
- 국내 금융사들은 교육 투자에 매우 민감하므로, ROI 기반 리더십 교육 설계는 설득력 있는 전략이 될 수 있습니다.
- 만족도 위주의 기존 리더십 교육 평가 방식을 재정비하고, 행동 변화나 업무 성과 연계 지표를 중심으로 전환하는 것이 필요합니다.
- 교육 콘텐츠 설계 초기 단계에서부터 측정 가능한 기대성과를 명확히 정의하는 것이 향후 ROI 보고서 작성에 유리합니다.
""")
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
