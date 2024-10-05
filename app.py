import asyncio
import logging
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from src.config import load_config
from src.services.chat_service import ChatService

# Load configuration
config = load_config()
TOKEN = config['TELEGRAM_API_KEY']

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Chat Service
chat_service = ChatService()

# Create a router
router = Router()

# Define states for FSM
class ChatStates(StatesGroup):
    chatting = State()

# Handler for /start command
@router.message(Command('start'))
async def command_start_handler(message):
    await message.answer(
        f"Hello, {message.from_user.full_name}! Welcome to Questbot. Use /chat to interact with our AI model. "
        f"Type /help to see all available commands."
    )

# Handler for /help command
@router.message(Command('help'))
async def command_help_handler(message):
    help_text = (
        "Welcome to Questbot! Here are the available commands:\n"
        "/start - Display welcome message\n"
        "/chat - Start chatting with Questbot AI\n"
        "/quit - Exit chat mode\n"
        "/help - Show this help message"
    )
    await message.answer(help_text)

# Handler for /chat command (enters chat mode)
@router.message(Command('chat'))
async def start_chat_handler(message, state):
    await state.set_state(ChatStates.chatting)
    await message.answer("You're now in chat mode with Questbot AI! Send any message, and I'll respond. Type /quit to exit.")

# Handler for chatting messages
@router.message(ChatStates.chatting, ~F.text.startswith("/"))
async def chat_handler(message):
    user_input = message.text.strip()

    if not user_input:
        await message.answer("Please send a message to Questbot.")
        return

    # Get AI response from chat service
    ai_response = await chat_service.get_response(user_input)
    await message.answer(ai_response)

# Handler for /quit command (exits chat mode)
@router.message(Command('quit'))
async def quit_chat_handler(message, state):
    current_state = await state.get_state()
    if current_state == ChatStates.chatting:
        await state.clear()
        await message.answer("You've exited Questbot chat mode. Type /chat to start chatting again or /help for more commands.")
    else:
        await message.answer("You're not in Questbot chat mode. Type /chat to start chatting or /help for more commands.")

# Default handler for messages when not in chat mode
@router.message(F.text)
async def default_handler(message):
    await message.answer(
        "Welcome to Questbot! Use /chat to start chatting with our AI or /help to see the list of commands."
    )

# Error handler
@dp.errors()
async def error_handler(event):
    logging.error(f"An error occurred in Questbot: {event.exception}")

# Main function to start the bot
async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    # Register router
    dp.include_router(router)

    # Start polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())