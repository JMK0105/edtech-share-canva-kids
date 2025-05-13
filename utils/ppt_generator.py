from pptx import Presentation
from pptx.enum.text import MSO_AUTO_SIZE
from pptx.dml.color import RGBColor
from pptx.util import Pt
import textwrap


def replace_text_preserve_style(text_frame, new_text, max_length=50):
    """
    텍스트를 슬라이드 텍스트 상자에 입력하되, 줄바꿈, 스타일, 위치, 색상 등을 모두 유지합니다.
    """
    # 기본 스타일 정의 (run이 존재하지 않을 경우 fallback용)
    DEFAULT_FONT_NAME = "맑은 고딕"
    DEFAULT_FONT_SIZE = Pt(16)
    DEFAULT_FONT_COLOR = RGBColor(0, 0, 0)

    # \n → \\n 통일 후 줄 나누기
    lines = new_text.replace("\n", "\\n").split("\\n")
    lines = [line.strip() for line in lines if line.strip()]
    if not lines:
        return

    # 기존 스타일 백업 (첫 문단의 첫 run 기준)
    template_run = None
    template_align = None
    if text_frame.paragraphs and text_frame.paragraphs[0].runs:
        template_run = text_frame.paragraphs[0].runs[0]
        template_align = text_frame.paragraphs[0].alignment

    # 기존 텍스트 제거
    text_frame.clear()

    # 줄별로 문단 + run 삽입
    for i, line in enumerate(lines):
        p = text_frame.add_paragraph()
        p.alignment = template_align or None
        run = p.add_run()
        run.text = line

        # 스타일 복사 또는 기본 적용
        if template_run:
            run.font.name = template_run.font.name
            run.font.size = template_run.font.size or DEFAULT_FONT_SIZE
            run.font.bold = template_run.font.bold
            run.font.italic = template_run.font.italic
            try:
                if template_run.font.color and template_run.font.color.type == 1:
                    run.font.color.rgb = template_run.font.color.rgb
                else:
                    run.font.color.rgb = DEFAULT_FONT_COLOR
            except:
                run.font.color.rgb = DEFAULT_FONT_COLOR
        else:
            run.font.name = DEFAULT_FONT_NAME
            run.font.size = DEFAULT_FONT_SIZE
            run.font.color.rgb = DEFAULT_FONT_COLOR

        if i > 0:
            p.space_before = Pt(6)

    text_frame.word_wrap = True
    text_frame.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE


def insert_structured_content(template_path, structured_slides):
    """
    템플릿 파일을 불러와 슬라이드에 structured_slides 내용을 삽입합니다.
    """
    prs = Presentation(template_path)

    for i, slide_data in enumerate(structured_slides):
        if i >= len(prs.slides):
            break

        slide = prs.slides[i]
        title_kr = slide_data.get("title_kr", "")
        title_en = slide_data.get("title_en", "")
        content = slide_data.get("content", "")
        keywords = slide_data.get("keywords", "")

        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue

            if shape.name == "TitleKRBox":
                replace_text_preserve_style(shape.text_frame, title_kr)
            elif shape.name == "TitleENBox":
                replace_text_preserve_style(shape.text_frame, title_en)
            elif shape.name == "BodyBox":
                replace_text_preserve_style(shape.text_frame, content)
            elif shape.name == "KeywordBox":
                replace_text_preserve_style(shape.text_frame, keywords)

    return prs
