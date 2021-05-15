from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from loguru import logger

from settings import settings


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


@dp.message_handler()
async def echo_message(msg: types.Message):
    logger.info(msg)
    await bot.send_message(msg.from_user.id, f"{msg.from_user.first_name}, салам!")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
