from pptx import Presentation
from pptx.enum.text import MSO_AUTO_SIZE
from pptx.dml.color import RGBColor
from pptx.util import Pt
import textwrap


def wrap_text(text, max_length=50):
    """
    주어진 텍스트를 max_length 기준으로 줄바꿈 삽입
    """
    wrapped_lines = []
    for paragraph in text.split("\n"):
        paragraph = paragraph.strip()
        if paragraph:
            wrapped = textwrap.wrap(paragraph, width=max_length)
            wrapped_lines.extend(wrapped)
        else:
            wrapped_lines.append("")  # 빈 줄 유지
    return wrapped_lines


def replace_text_preserve_style(text_frame, new_text, max_length=50):
    # 줄바꿈 기준 분리 (GPT가 '\\n'으로 줄을 구분하는 경우가 많음)
    lines = new_text.split("\\n")
    lines = [line.strip() for line in lines if line.strip()]
    if not lines:
        return

    # 기존 스타일 백업
    template_run = None
    template_align = None
    if text_frame.paragraphs and text_frame.paragraphs[0].runs:
        template_run = text_frame.paragraphs[0].runs[0]
        template_align = text_frame.paragraphs[0].alignment

    # 기존 텍스트 제거
    text_frame.clear()

    # 첫 문단에 직접 삽입 (불필요한 비어있는 문단 남기지 않기 위해)
    for i, line in enumerate(lines):
        p = text_frame.add_paragraph()
        p.alignment = template_align or None
        run = p.add_run()
        run.text = line

        if template_run:
            run.font.name = template_run.font.name
            run.font.size = template_run.font.size or Pt(18)
            run.font.bold = template_run.font.bold
            run.font.italic = template_run.font.italic
            try:
                if template_run.font.color and template_run.font.color.type == 1:
                    run.font.color.rgb = template_run.font.color.rgb
            except Exception:
                pass

        if i > 0:
            p.space_before = Pt(6)

    text_frame.word_wrap = True
    text_frame.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE


def insert_structured_content(template_path, structured_slides):
    """
    지정된 템플릿에 structured_slides 내용을 삽입
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
