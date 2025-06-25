import asyncio
from telegram import Bot
from dotenv import load_dotenv
import os

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def main():

    bot = Bot(token=TELEGRAM_BOT_TOKEN)

    updates = await bot.get_updates()

    if not updates:
        print("No updates found")
    else:
        for update in updates:
            if update.message:

                chat_id = update.message.chat.id
                chat_title = update.message.chat.title
                message_text = update.message.text
                print(f"Chat ID: {chat_id}  | Chat Title: {chat_title} | Message: {message_text}")

asyncio.run(main())