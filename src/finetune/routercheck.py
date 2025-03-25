import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

completion = client.chat.completions.create(
    extra_headers={
        # Optional. Site URL for rankings on openrouter.ai.
        "HTTP-Referer": os.getenv("SITE_URL"),
        # Optional. Site title for rankings on openrouter.ai.
        "X-Title": os.getenv("SITE_NAME"),
    },
    extra_body={},
    model="deepseek/deepseek-chat-v3-0324:free",
    messages=[{"role": "user", "content": "What is the meaning of life?"}],
)
print(completion.choices[0].message.content)
