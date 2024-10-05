import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')
bot = Bot(token=TELEGRAM_API_KEY)
dp = Dispatcher()

# Initialize Groq LLM
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
llm = ChatGroq(
    model='mixtral-8x7b-32768',
    temperature=0.1,
    max_tokens=4096,
    timeout=None,
    max_retries=2,
)

@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    await message.reply("Hi! I'm a chatbot powered by z4hid's LLM. How can I assist you today?")

@dp.message()
async def echo(message: types.Message):
    user_input = message.text
    messages = [
        ("system", "You are a helpful assistant that answers questions based on the given context."),
        ("human", user_input),
    ]
    
    try:
        ai_msg = llm.invoke(messages)
        await message.answer(ai_msg.content)
    except Exception as e:
        logging.error(f"Error in processing message: {e}")
        await message.answer("Sorry, I encountered an error while processing your request.")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())