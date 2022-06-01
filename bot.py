from os import getenv, path
from sys import exit
import time

import logging
from aiogram import Bot, Dispatcher, executor, types

from keyboards import start_keyboard
from script import ocr_core


def help_menu(bot, chat_id):
    bot.send_message(chat_id, 'Welcome! You can use this keyboards: ')


# TODO Сделать выбор языков для скана
def main():
    bot_token = getenv("BOT_TOKEN")
    if not bot_token:
        exit("Error: no token provided")

    bot = Bot(token=bot_token)
    dp = Dispatcher(bot)
    logging.basicConfig(level=logging.INFO)
    print(' STARTED! ')

    # start command
    @dp.message_handler(commands="start")
    async def cmd_start(message: types.Message):
        await message.answer("Welcome! You can use this keyboards: ", reply_markup=start_keyboard)

    @dp.message_handler(lambda message: message.text == "/pict")
    async def pictures(message: types.Message):
        await message.reply("Send me you pictures!", reply_markup=types.ReplyKeyboardRemove())

        @dp.message_handler(content_types=['photo'])
        async def handle_docs_photo(message: types.Message):
            file_info = await bot.get_file(message.photo[-1].file_id)
            await message.photo[-1].download(destination=path.join(
                path.abspath(path.dirname(__file__)) + r'\tmp\files'))
            src = f'/tmp/files/{file_info.file_path}'
            await message.answer(ocr_core(src))

        @dp.message_handler(content_types=['document'])
        async def scan_message(message: types.Message):
            file_info = await bot.get_file(message.document.file_id)
            await message.document.download(destination=path.join(
                path.abspath(path.dirname(__file__)) + r'\tmp\files'))
            src = f'/tmp/files/{file_info.file_path}'
            time.sleep(2)
            await message.answer(ocr_core(src))

    @dp.message_handler(commands="help")
    async def cmd_start(message: types.Message):
        await message.answer('Help:', reply_markup=types.ReplyKeyboardRemove())
        # TODO

    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()
