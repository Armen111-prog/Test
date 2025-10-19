import re
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telegram import Bot

# ================= НАСТРОЙКИ =================
API_ID = 123456                 # твой API_ID
API_HASH = 'your_api_hash'      # твой API_HASH
SESSION_STRING = 'тут_твоя_строка_сессии'  # StringSession
BOT_TOKEN = 'твой_bot_token'    # токен бота @testbot
CHAT_ID = 123456789             # id юзера, которому бот будет пересылать коды
DELETE_AFTER = 20               # сек. до удаления сообщения у получателя (0 чтобы не удалять)
CODE_MIN_LEN = 4
CODE_MAX_LEN = 8
# ============================================

# Регулярка для поиска кода (только цифры)
CODE_RE = re.compile(r'\b\d{' + str(CODE_MIN_LEN) + r',' + str(CODE_MAX_LEN) + r'}\b')

# Клиент Telethon для аккаунта пользователя
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

# Бот для пересылки кода юзеру
bot = Bot(token=BOT_TOKEN)

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    try:
        sender = await event.get_sender()
        if getattr(sender, "id", None) == 777000:  # системный Telegram
            text = event.raw_text or ""
            match = CODE_RE.search(text)
            if match:
                code = match.group()
                # отправляем через бота @testbot
                bot.send_message(chat_id=CHAT_ID, text=f"{code}")
                print("Sent code via bot:", code)
            else:
                print("No code found in the message.")
    except Exception as e:
        print("Handler error:", e)

async def main():
    await client.start()
    me = await client.get_me()
    print(f"Running as: {me.id} ({me.username or me.first_name})")
    print("Listening for Telegram service messages...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
