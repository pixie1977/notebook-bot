import asyncio
import httpx
import logging
import os
from dotenv import load_dotenv

from src.core.utils import fetch_json, interpret_weather_code

# Загружаем переменные из .env
load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api_key = os.getenv("OPENWEATHER_API_KEY")
telegram_token = os.getenv("TELEGRAM_TOKEN")

control_param = os.getenv("CONTROL_PARAMETER", ".ENV NOT FOUND!")
print(control_param)



async def main():
    # URLs: погода (на примере OpenWeatherMap) и курс криптовалюты (CoinGecko)
    # Заметка: для OpenWeatherMap нужен API-ключ (бесплатный: https://openweathermap.org/api)
    # Используем публичные API без ключей, если возможно

    urls = {
        "https://api.open-meteo.com/v1/forecast?latitude=55.7558&longitude=37.6176&current=temperature_2m,weather_code&temperature_unit=celsius&timezone=Europe%2FMoscow": "weather_moscow",
        "https://api.open-meteo.com/v1/forecast?latitude=59.9386&longitude=30.3141&current=temperature_2m,weather_code&temperature_unit=celsius&timezone=Europe%2FMoscow": "weather_spb",
        "https://api.open-meteo.com/v1/forecast?latitude=55.09&longitude=36.62&current=temperature_2m,weather_code&temperature_unit=celsius&timezone=Europe%2FMoscow": "weather_obninsk",
        "https://api.open-meteo.com/v1/forecast?latitude=55.16&longitude=37.26&current=temperature_2m,weather_code&temperature_unit=celsius&timezone=Europe%2FMoscow": "weather_maloyaroslavets",
        "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd&include_24hr_change=true": "eth_price",
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        tasks = [fetch_json(client, url, name) for url, name in urls.items()]
        results = await asyncio.gather(*tasks)

    # Сводка
    summary = {}

    for name, data in results:
        if not data:
            continue

        if name.startswith("weather_"):
            city = name.split("_")[1].title()
            current = data.get("current", {})
            summary[f"weather_{city}"] = {
                "Температура": f"{current.get('temperature_2m')}°C",
                "Погода": interpret_weather_code(current.get("weather_code"))
            }

        elif name == "eth_price":
            eth = data.get("ethereum", {})
            summary["eth_price"] = {
                "Цена в долларах": f"${eth.get('usd')}",
                "За последние 24 часа": f"{eth.get('usd_24h_change'):.2f}%"
            }

    # Вывод
    for source, data in summary.items():
        print(f"\n--- {source.replace('_', ' ').upper()} ---")
        for key, value in data.items():
            print(f"{key}: {value}")

if __name__ == "__main__":
    asyncio.run(main())