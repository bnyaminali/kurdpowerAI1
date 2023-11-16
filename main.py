from os import environ
import asyncio
from telebot.async_telebot import AsyncTeleBot
from Bard import Chatbot

# get config
token = "dAiFw9V-jARNFOgg_YXrkuTriDFubWKk45MpxNg6IIz51PxiaMWIqrjOUqvWbFDgb2zzAw."

# init telegram bot
bot_token = "6941072328:AAFAgxMp0-nDf7TQsm3TV19f5hYG3Uwjk4w"
bot = AsyncTeleBot(bot_token, parse_mode="MARKDOWN")

# init chatbot
chatbot = Chatbot(token)
print("Initializing bot...")

# define a message handler to send a message when the command /start is issued
@bot.message_handler(commands=["start", "hello"])
async def send_welcome(message):
    await bot.reply_to(message, "This bot uses the Google Bard.")

@bot.message_handler(func=lambda m: True)
async def send_gpt(message):
    print("Getting response...")
    try:
        await bot.send_chat_action(message.chat.id, 'typing')
        response = chatbot.ask(message.text)
        await bot.reply_to(message, response["content"])
    except BaseException as e:
        await bot.reply_to(message, str(e))

async def run_bot():
    await bot.delete_webhook()  # Disable any existing webhook
    await bot.polling()  # Start the bot in polling mode

# run the bot
if __name__ == "__main__":
    asyncio.run(run_bot())
