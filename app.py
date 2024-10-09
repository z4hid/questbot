import asyncio
import logging
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from src.config import load_config
from src.services.chat_service import ChatService
from src.services.travel_service import plan_optimized_trip

config = load_config()
TOKEN = config['TELEGRAM_API_KEY']
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
chat_service = ChatService()

router = Router()

class ChatStates(StatesGroup):
    chatting = State()

class TravelStates(StatesGroup):
    waiting_for_start_location = State()
    waiting_for_destination = State()
    waiting_for_travel_dates = State()

@router.message(Command('start'))
async def command_start_handler(message):
    await message.answer(
        f"Hello, {message.from_user.full_name}! Welcome to Questbot. Use /chat to interact with our AI model or /travel to plan a trip. "
        f"Type /help to see all available commands."
    )

@router.message(Command('help'))
async def command_help_handler(message):
    help_text = (
        "Welcome to Questbot! Here are the available commands:\n"
        "/start - Display welcome message\n"
        "/chat - Start chatting with Questbot AI\n"
        "/travel - Start planning a trip\n"
        "/quit - Exit mode\n"
        "/help - Show this help message"
    )
    await message.answer(help_text)

@router.message(Command('chat'))
async def start_chat_handler(message, state):
    await state.set_state(ChatStates.chatting)
    await message.answer("You're now in chat mode with Questbot AI! Send any message, and I'll respond. Type /quit to exit.")

@router.message(ChatStates.chatting, ~F.text.startswith("/"))
async def chat_handler(message):
    user_input = message.text.strip()
    if not user_input:
        await message.answer("Please send a message to Questbot.")
        return
    ai_response = await chat_service.get_response(user_input)
    await message.answer(ai_response)

@router.message(Command('travel'))
async def start_travel_handler(message, state):
    await message.answer("Let's plan your trip! Where are you starting from?")
    await state.set_state(TravelStates.waiting_for_start_location)

@router.message(TravelStates.waiting_for_start_location)
async def capture_start_location(message, state):
    start_location = message.text.strip()
    await state.update_data(start_location=start_location)
    await message.answer("Great! What's your destination?")
    await state.set_state(TravelStates.waiting_for_destination)

@router.message(TravelStates.waiting_for_destination)
async def capture_destination(message, state):
    destination = message.text.strip()
    await state.update_data(destination=destination)
    await message.answer("Awesome! When are you traveling? (e.g., 2024-10-15 to 2024-10-20)")
    await state.set_state(TravelStates.waiting_for_travel_dates)

@router.message(TravelStates.waiting_for_travel_dates)
async def capture_travel_dates(message, state):
    travel_dates = message.text.strip()
    user_data = await state.get_data()
    start_location = user_data['start_location']
    destination = user_data['destination']
    try:
        
        trip_plan = plan_optimized_trip(start_location=start_location, destination=destination, travel_dates=travel_dates)
        await message.answer(f"Here is your optimized trip plan:\n\n{trip_plan}")
    except Exception as e:
        await message.answer(f"An error occurred while generating the trip plan: {str(e)}")
    await state.clear()

@router.message(Command('quit'))
async def quit_chat_handler(message, state):
    await message.answer("You have exited. Type /start to start again.")
    await state.clear()

# Start the bot
if __name__ == '__main__':
    dp.include_router(router)
    asyncio.run(dp.start_polling(bot))
