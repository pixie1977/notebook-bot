from aiogram import Router, types
from aiogram.filters import Command

from src.config.config import USER_REQUEST_MAX_LEN
from src.core.llm_utils import process_llm_request

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message) -> None:
    """
    Обработчик команды /start.
    Отправляет приветственное сообщение и список доступных команд.
    """
    await message.answer(
        "Привет! 🌟\n"
        "Я — пример многофункционального бота.\n"
        "Доступные команды:\n"
        "/start — приветствие\n"
        "/weather — погода в городах по выбору\n"
        "/eth — курс Ethereum\n"
        "/myage — прототип работы с состояниями\n"
        "/last — 5 последних сообщений в чате\n"
        f"/ask — запрос к LLM (максимум {USER_REQUEST_MAX_LEN} символов)\n"
    )


@router.message(Command("help"))
async def cmd_help(message: types.Message) -> None:
    """
    Обработчик команды /help.
    Отправляет краткую справку по использованию бота.
    """
    await message.answer("Помощь: просто используй команды из меню.")


@router.message(Command("faq"))
async def cmd_faq(message: types.Message) -> None:
    """
    Обработчик команды /faq.
    Отправляет заглушку для раздела FAQ.
    """
    await message.answer("Заглушка для FAQ")


@router.message(Command("ask"))
async def cmd_ask(message: types.Message) -> None:
    """
    Обработчик команды /ask.
    Передает запрос в LLM.
    """
    user_query = message.text[len("/ask "):].strip() if len(message.text) > len("/ask ") else ""
    if not user_query:
        await message.answer("Пожалуйста, введите запрос после команды /ask.")
        return

    if len(user_query) > int(USER_REQUEST_MAX_LEN):
        await message.answer(f"Запрос слишком длинный. Максимум — {USER_REQUEST_MAX_LEN} символов.")
        return

    try:
        response = process_llm_request(user_query)
        await message.answer(response)
    except Exception as e:
        await message.answer("Произошла ошибка при обработке запроса. Попробуйте позже.")
        raise e