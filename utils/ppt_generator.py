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
            if shape.name == "TitleBox":
                shape.text_frame.text = title
            elif shape.name == "BodyBox":
                shape.text_frame.text = body
            elif shape.name == "KeywordBox" or "Keyword" in shape.text_frame.text:
                shape.text_frame.text = keyword
            elif shape.is_placeholder:
                if shape.placeholder_format.idx == 0:
                    shape.text_frame.text = title
                elif shape.placeholder_format.idx == 1:
                    shape.text_frame.text = body
    return prs
