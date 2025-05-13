# 📁 utils/ppt_generator.py
from pptx import Presentation
from pptx.enum.text import MSO_AUTO_SIZE
from pptx.dml.color import RGBColor

def replace_text_preserve_style(text_frame, new_text):
    new_text = new_text.replace("\\n", "\n")
    lines = [line.strip() for line in new_text.split("\n") if line.strip()]
    if not lines:
        return

    # 스타일 복사용 템플릿 문단 찾기
    style_template = None
    if text_frame.paragraphs:
        style_template = text_frame.paragraphs[0]

    text_frame.clear()

    for line in lines:
        p = text_frame.add_paragraph()
        p.text = line
        if style_template and style_template.runs:
            run = p.runs[0]
            template_run = style_template.runs[0]
            run.font.name = template_run.font.name
            run.font.size = template_run.font.size
            run.font.bold = template_run.font.bold
            run.font.italic = template_run.font.italic
            if template_run.font.color.type == 1:  # RGB
                run.font.color.rgb = template_run.font.color.rgb

    text_frame.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE


def insert_structured_content(template_path, structured_slides):
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
