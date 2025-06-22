from telegram import Bot, InputFile
import asyncio
import os
from PIL import Image
import io

class MyBot:
    def __init__(self, telegram_bot_token, chat_id):
        self.token = telegram_bot_token
        self.chat_id = chat_id

        if self.token is None or self.chat_id is None:
            raise ValueError("Environment variables TELEGRAM_BOT_TOKEN or CHAT_ID are not set.")

        self.bot = Bot(token=self.token)

    async def _send(self, text: str):
        async with self.bot:
            await self.bot.send_message(chat_id=self.chat_id, text=text)

    async def _send_photo(self, image_path: str):
        async with self.bot:
            with open(image_path, 'rb') as f:
                await self.bot.send_photo(chat_id=self.chat_id, photo=InputFile(f))

    async def _send_pil_image(self, pil_image: Image.Image):
        buf = io.BytesIO()
        pil_image.save(buf, format='PNG')
        buf.seek(0)
        async with self.bot:
            await self.bot.send_photo(chat_id=self.chat_id, photo=InputFile(buf, filename="image.png"))

    def send_message(self, messages: list[str]):
        if isinstance(messages, list):
            text = '\n'.join(messages)
        else:
            text = str(messages)
        asyncio.run(self._send(text))

    def send_photo_from_path(self, image_path: str):
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"No image found at path: {image_path}")
        asyncio.run(self._send_photo(image_path))

    def send_pil_image(self, pil_image: Image.Image):
        if not isinstance(pil_image, Image.Image):
            raise TypeError("Expected a PIL.Image.Image object")
        asyncio.run(self._send_pil_image(pil_image))
