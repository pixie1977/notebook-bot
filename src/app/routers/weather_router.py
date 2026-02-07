from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
import httpx

from src.app.keyboard.keyboard import weather_inline_kb
from src.core.utils import interpret_weather_code


router = Router()

# Координаты городов для запроса погоды
CITY_COORDS = {
    "moscow": (55.7558, 37.6176),
    "spb": (59.9386, 30.3141),
    "obninsk": (55.09, 36.62),
    "maloyaroslavets": (55.16, 37.26),
}


async def get_weather(latitude: float, longitude: float) -> str:
    """
    Асинхронно запрашивает текущую погоду для заданных координат.

    :param latitude: широта местоположения.
    :param longitude: долгота местоположения.
    :return: строка с эмодзи погоды и температурой.
    """
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}"
        f"&current=temperature_2m,weather_code&temperature_unit=celsius"
    )
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            temp = data["current"]["temperature_2m"]
            code = data["current"]["weather_code"]
            emoji = interpret_weather_code(code)
            return f"{emoji} {temp}°C"
        except Exception as e:
            return f"⚠️ Ошибка получения погоды: {e}"


@router.message(Command("weather"))
async def cmd_weather(message: Message) -> None:
    """
    Обработчик команды /weather.
    Отправляет пользователю инлайн-клавиатуру с выбором города.
    """
    await message.answer("Выберите город:", reply_markup=weather_inline_kb)


@router.callback_query(lambda c: c.data.startswith("weather_"))
async def callback_weather(callback: CallbackQuery) -> None:
    """
    Обработчик нажатия на кнопку выбора города.
    Запрашивает погоду и отправляет результат.
    """
    city_code = callback.data.replace("weather_", "")
    city_names = {
        "moscow": "Москва",
        "spb": "Санкт-Петербург",
        "obninsk": "Обнинск",
        "maloyaroslavets": "Малоярославец",
    }
    city = city_names.get(city_code, "неизвестный город")

    await callback.answer(f"Запрос погоды для {city}...")

    latitude, longitude = CITY_COORDS[city_code]
    result = await get_weather(latitude, longitude)

    await callback.message.answer(f"🌤 Погода в {city}: {result}")