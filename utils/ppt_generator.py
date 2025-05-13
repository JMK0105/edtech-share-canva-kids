# 📁 utils/ppt_generator.py
from pptx import Presentation

def insert_structured_content(template_path, structured_slides):
    prs = Presentation(template_path)

    for i, slide_data in enumerate(structured_slides):
        if i >= len(prs.slides):
            break
        slide = prs.slides[i]
        title, body, keyword = slide_data["title"], slide_data["content"], slide_data["keywords"]

        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            if shape.placeholder_format.idx == 0:
                shape.text_frame.text = title
            elif shape.placeholder_format.idx == 1:
                shape.text_frame.text = body
            elif "Keyword" in shape.text_frame.text or "키워드" in shape.text_frame.text:
                shape.text_frame.text = keyword
    return prs
