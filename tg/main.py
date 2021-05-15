from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor
from hurry.filesize import size

from tg.core import psql
from tg.core.settings import settings

TOKEN = settings.token

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

mysystem = [
    (1024 ** 5, " ПБ"),
    (1024 ** 4, " ТБ"),
    (1024 ** 3, " ГБ"),
    (1024 ** 2, " МБ"),
    (1024 ** 1, " КБ"),
    (1024 ** 0, " Б"),
]

statuses = {"created": "грузится", "loading": "грузится", "done": "загружен"}


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
    raw_id = await psql.get_user_id(message.from_user.username)
    user_id = raw_id["id"]

    raw_sum = await psql.get_files_size(user_id)
    sum = raw_sum["sum"]

    raw_count = await psql.get_files_count(user_id)
    count = raw_count["count"]

    if user_id:
        await bot.send_message(
            message.from_user.id, f"У тебя {count} загруженных файлов"
        )
        await bot.send_message(
            message.from_user.id,
            f"Вес всех загруженных файлов - {size(sum, system=mysystem)}",
        )
    else:
        await bot.send_message(
            message.from_user.id,
            f"Юзер с именем {message.from_user.username} не найден",
        )


@dp.message_handler(Text(equals="Показать все файлы"))
async def all_files(message: types.Message):
    raw_id = await psql.get_user_id(message.from_user.username)
    files = await psql.get_files(raw_id["id"])

    template = "{name}\nРазмер: {file_size}\nСтатус: {status}\n"

    md_string = "\n".join(
        [
            template.format(
                name=file["name"],
                file_size=size(file["size"], system=mysystem),
                status=statuses[file["status"]],
            )
            for file in files
        ]
    )

    if id:
        if len(files) == 0:
            await bot.send_message(
                message.from_user.id,
                f"{message.from_user.username}, у тебя нет загруженных файлов",
            )

        await bot.send_message(
            message.from_user.id, f"{message.from_user.username}, твои файлы:"
        )

        await bot.send_message(message.from_user.id, md_string)
    else:
        await bot.send_message(
            message.from_user.id,
            f"Юзер с именем {message.from_user.username} не найден",
        )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
