from aiogram import Router, types
from aiogram.filters import Command
import httpx

from src.config.config import COINGECKO_URL

router = Router()


async def get_eth_price() -> str:
    """
    Асинхронно получает текущую цену Ethereum с API CoinGecko.

    :return: строка с ценой ETH в USD и изменением за 24 часа.
    """
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(COINGECKO_URL)
            response.raise_for_status()
            data = response.json()
            if "ethereum" not in data or "usd" not in data["ethereum"]:
                return "⚠️ Неверный формат ответа от API"
            price = data["ethereum"]["usd"]
            change = data["ethereum"]["usd_24h_change"]
            change_str = f"📈 +{change:.2f}%" if change >= 0 else f"📉 {change:.2f}%"
            return f"${price:,} ({change_str})"
        except Exception as e:
            return f"⚠️ Не удалось получить цену ETH: {e}"


@router.message(Command("eth"))
async def cmd_eth(message: types.Message) -> None:
    """
    Обработчик команды /eth.
    Запрашивает и отправляет текущий курс Ethereum.
    """
    await message.answer("Запрашиваю курс Ethereum...")
    price = await get_eth_price()
    await message.answer(f"Курс ETH: {price}")