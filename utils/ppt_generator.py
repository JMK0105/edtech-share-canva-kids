# 📁 utils/ppt_generator.py
from pptx import Presentation

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
                shape.text_frame.text = title_kr
            elif shape.name == "TitleENBox":
                shape.text_frame.text = title_en
            elif shape.name == "BodyBox":
                shape.text_frame.text = content
            elif shape.name == "KeywordBox":
                shape.text_frame.text = keywords
    return prs
