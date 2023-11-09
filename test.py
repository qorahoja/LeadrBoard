import logging
from aiogram import Bot, types
import asyncio

# Set up logging
logging.basicConfig(level=logging.INFO)

# Replace 'YOUR_BOT_TOKEN' with your actual bot token obtained from @BotFather on Telegram
BOT_TOKEN = '6487765756:AAGwUvqglUMxsw0tVZ_DY29VRe_AQf-a4-s'  # Replace with your actual bot token

# Initialize the bot
bot = Bot(token=BOT_TOKEN)

async def send_message_to_user(user_id, message_text):
    try:
        await bot.send_message(chat_id=user_id, text=message_text)
        print(f"Message sent to user with ID {user_id}")
    except Exception as e:
        print(f"Error sending message to user with ID {user_id}: {str(e)}")

# Example user ID and message text
user_id = 5286893504  # Replace with the actual user ID you want to send a message to
message_text = "Yozmizmi"

# Send the message to the user
loop = asyncio.get_event_loop()
loop.run_until_complete(send_message_to_user(user_id, message_text))
