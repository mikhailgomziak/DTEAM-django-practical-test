import openai
from django.conf import settings

client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

def translate_text(text_items: dict, target_language: str) -> dict:
    prompt = f"Translate the following fields to {target_language}. Keep the keys unchanged:\n"
    for key, value in text_items.items():
        prompt += f"{key}: {value}\n"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a professional CV translator. Return translations using the same field labels."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
        max_tokens=3000
    )

    output = response.choices[0].message.content.strip()
    translations = {}

    for line in output.split("\n"):
        if ": " in line:
            key, value = line.split(": ", 1)
            translations[key.strip()] = value.strip()

    return translations
