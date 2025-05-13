# 📁 utils/ppt_generator.py
from pptx import Presentation
from pptx.enum.text import MSO_AUTO_SIZE

def replace_text_preserve_style(text_frame, new_text):
    new_text = new_text.replace("\\n", "\n")
    if not text_frame.paragraphs:
        return
    para = text_frame.paragraphs[0]
    if para.runs:
        para.runs[0].text = new_text
    else:
        para.add_run().text = new_text

    # 자동 박스 확장 설정
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
