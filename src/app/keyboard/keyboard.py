"""
Модуль для создания клавиатур Telegram-бота.
"""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Клавиатура с основными командами (Reply)
main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="/start"),
            KeyboardButton(text="/help")
        ],
        [
            KeyboardButton(text="/weather"),
            KeyboardButton(text="/eth")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder="Выберите действие..."
)

# Инлайн-клавиатура для выбора города
weather_inline_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Москва", callback_data="weather_moscow"),
            InlineKeyboardButton(text="Санкт-Петербург", callback_data="weather_spb")
        ],
        [
            InlineKeyboardButton(text="Обнинск", callback_data="weather_obninsk"),
            InlineKeyboardButton(text="Малоярославец", callback_data="weather_maloyaroslavets")
        ]
    ]
)

# Инлайн-клавиатура для криптовалют
crypto_inline_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Ethereum (ETH)", callback_data="eth_price"),
            InlineKeyboardButton(text="Bitcoin (BTC)", callback_data="btc_price")
        ],
        [
            InlineKeyboardButton(text="Обновить", callback_data="refresh_price")
        ]
    ]
)