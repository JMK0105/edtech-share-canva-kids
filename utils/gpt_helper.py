import openai

openai.api_key = "YOUR_API_KEY"

def summarize_text(text, prompt_instruction):
    messages = [
        {"role": "system", "content": "당신은 발표자료 요약 전문가입니다."},
        {"role": "user", "content": f"{prompt_instruction}\n\n{text}"}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        max_tokens=1500
    )
    return response['choices'][0]['message']['content']
