import openai
import os
from dotenv import load_dotenv

class OpenAIService:
    def __init__(self):
        load_dotenv()
        openai.api_key = os.getenv('OPENAI_API_KEY')

    async def generate_response(self, context):
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": f"Generate a Twitter reply for: {context}"
            }],
            max_tokens=60,
            temperature=0.7
        )
        return completion.choices[0].message.content
