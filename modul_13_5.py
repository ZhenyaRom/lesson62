from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

api = '7437488643:AAFdBCkUqmfh7EYCa4qSpvSMwObBmDwl9Ls'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
kp = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
kp.row(button1, button2)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text='Информация')
async def info(massage):
    await massage.answer('рассчитываю суточную норму калорий на основании вашего возраста, роста и веса',
                         reply_markup=kp)


@dp.message_handler(text='Рассчитать')
async def set_age(massage):
    await massage.answer('Введите свой возраст: ')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост: ')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес: ')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    try:
        c = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161
        await message.answer(f'Ваша норма калорий - {c}')
    except ValueError:
        await message.answer('Возраст, рост и вес нухно вводить арабскими цифрами', reply_markup=kp)
    await state.finish()


@dp.message_handler(commands='start')
async def start(massage):
    await massage.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kp)


@dp.message_handler()
async def all_massages(massage):
    await massage.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
