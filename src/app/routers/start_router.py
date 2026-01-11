from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! 🌟\n"
        "Я — пример многофункционального бота.\n"
        "Доступные команды:\n"
        "/start — приветствие\n"
        "/weather — погода в городах по выбору\n"
        "/eth — курс Ethereum\n"
        "/myage — прототип работы с состояниями\n"
    )

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer("Помощь: просто используй команды из меню.")

@router.message(Command("faq"))
async def cmd_help(message: types.Message):
    await message.answer("Заглушка для FAQ (1)")

@router.message(Command("FAQ"))
async def cmd_help(message: types.Message):
    await message.answer("Заглушка для FAQ (2)")