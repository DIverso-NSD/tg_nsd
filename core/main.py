from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from loguru import logger
from aiogram.dispatcher.filters import Text

from settings import settings
from db.get import *


TOKEN = settings.token

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def process_start_command(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = types.KeyboardButton(text="Показать все файлы")
    keyboard.add(button_1)
    button_2 = "Общий обьем файлов"
    keyboard.add(button_2)
    await message.answer("Привет!\nНапиши мне что-нибудь!", reply_markup=keyboard)


@dp.message_handler(commands=["help"])
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что нибудь, бро")


@dp.message_handler(Text(equals="Общий обьем файлов"))
async def sum_files(message: types.Message):
    raw_id = await get_user_id(message.from_user.username)
    id = raw_id["id"]
    raw_sum = await get_files_size(id)
    sum = raw_sum["sum"]
    if id:
        await bot.send_message(message.from_user.id, f"Вес всех файлов - {sum}")
    else:
        await bot.send_message(
            message.from_user.id,
            f"Юзер с именем {message.from_user.username} не найден",
        )


@dp.message_handler(Text(equals="Показать все файлы"))
async def all_files(message: types.Message):
    id = await get_user_id(message.from_user.username)
    if id:
        await bot.send_message(
            message.from_user.id, f"{message.from_user.username} - {id}, салам!"
        )
    else:
        await bot.send_message(
            message.from_user.id,
            f"Юзер с именем {message.from_user.username} не найден",
        )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
