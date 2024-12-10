import json
from channels.generic.websocket import AsyncWebsocketConsumer
from openai import OpenAI
from django.conf import settings
from .prompt_engineering import prompt
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # OpenAI API 호출
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": message}
            ]
        )

        ai_response = response.choices[0].message.content

        # 응답 전송
        await self.send(text_data=json.dumps({
            'message': ai_response,
            'is_bot': True
        }))
