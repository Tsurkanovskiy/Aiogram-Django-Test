from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import aiohttp
import os



CHECK_URL = "..."
REGISTER_URL = "..."
TOKEN = "..."

bot =  Bot(token = TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class RegisterStates(StatesGroup):
	start = State()
	id_check = State()
	password_input = State()





@dp.message_handler(commands = ['start','help'])
async def echo_help(message: types.Message):
	await message.answer("Команда для реєстрації:\n/register")

@dp.message_handler(commands = ['register'], state = "*")
async def register_message(message: types.Message):
	await RegisterStates.id_check.set()
	await message.answer("Введіть свій User ID:")	

@dp.message_handler(state = RegisterStates.id_check)
async def check_user_id(message: types.Message, state: FSMContext):
	async with aiohttp.ClientSession() as session:
		async with session.post(CHECK_URL, data=str(message.text)) as response:
			resp = await response.json()
			if resp['id_status'] == True:
				login = resp['login']
				await message.answer(f"Ваш логін отриманий з серверу - {login}")
				await state.update_data(login = login)
				await RegisterStates.password_input.set()
				await message.answer(f"Введіть свій пароль щоб зареєструвати користувача:")
			else:
				await message.answer("User ID не був знайдено. У реєстрації відмовлено")
				await RegisterStates.start.set()
			
@dp.message_handler(state = RegisterStates.password_input)
async def check_user_id(message: types.Message, state: FSMContext):	
	data = await state.get_data()
	login = data.get('login')
	password = message.text
	await message.answer(f"{login}, {password}")
	async with aiohttp.ClientSession() as session:
		async with session.post(REGISTER_URL, json={"login": login, "password": password}) as response:
			resp = await response.json()
			print(resp["reg_status"])

	await RegisterStates.start.set()
	await message.answer("Вітаю! Вас зареєсторовано в системі!")



executor.start_polling(dp, skip_updates = True)