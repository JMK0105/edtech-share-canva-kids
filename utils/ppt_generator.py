from pptx import Presentation

def insert_content_to_template(template_path, slides_text):
    prs = Presentation(template_path)
    for i, text in enumerate(slides_text):
        if i < len(prs.slides):
            slide = prs.slides[i]
            for shape in slide.shapes:
                if shape.has_text_frame:
                    shape.text_frame.clear()
                    shape.text_frame.text = text
    return prs
