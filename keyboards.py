from aiogram import types

# Menu keyboard
start_keyboard = types.ReplyKeyboardMarkup()

key_help = types.KeyboardButton(text='/help', callback_data='/help', resize_keyboard=True)
start_keyboard.add(key_help)

key_pict = types.KeyboardButton(text='/pict', callback_data='/pict', resize_keyboard=True)
start_keyboard.add(key_pict)
