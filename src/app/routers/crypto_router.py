from aiogram import Router, types
import httpx
from aiogram.filters import Command

router = Router()

async def get_eth_price() -> str:
    url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd&include_24hr_change=true"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            return "Не удалось получить цену ETH."
        data = response.json()
        price = data["ethereum"]["usd"]
        change = data["ethereum"]["usd_24h_change"]
        change_str = f"📈 +{change:.2f}%" if change >= 0 else f"📉 {change:.2f}%"
        return f"${price:,} ({change_str})"

@router.message(Command("eth"))
async def cmd_eth(message: types.Message):
    await message.answer("Запрашиваю курс Ethereum...")
    price = await get_eth_price()
    await message.answer(f"Курс ETH: {price}")