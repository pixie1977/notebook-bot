from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from src.infra.db_service import save_user, save_message


router = Router()


class Form(StatesGroup):
    """
    Машина состояний для сбора данных пользователя.
    Состояния: ввод имени → ввод возраста.
    """
    name = State()
    age = State()


@router.message(Command("myage"))
async def cmd_start(message: Message, state: FSMContext) -> None:
    """
    Обработчик команды /myage.
    Инициализирует FSM и запрашивает имя пользователя.

    :param message: Входящее сообщение от пользователя.
    :param state: Контекст машины состояний.
    """
    await state.set_state(Form.name)
    await message.answer("Привет! Как тебя зовут?")


@router.message(Form.name)
async def process_name(message: Message, state: FSMContext) -> None:
    """
    Обработчик ввода имени.
    Сохраняет имя и переходит к состоянию ввода возраста.

    :param message: Сообщение с именем.
    :param state: Контекст состояния.
    """
    await state.update_data(name=message.text)
    await state.set_state(Form.age)
    await message.answer("Сколько тебе лет?")


@router.message(Form.age)
async def process_age(message: Message, state: FSMContext) -> None:
    """
    Обработчик ввода возраста.
    Сохраняет данные в БД, отправляет подтверждение и очищает состояние.

    :param message: Сообщение с возрастом.
    :param state: Контекст состояния.
    """
    data = await state.update_data(age=message.text)
    name = data.get("name")
    age = data.get("age")

    tg_id: str = str(message.from_user.id)

    saved_user = save_user(tg_id=tg_id, name=name, age=age)
    if saved_user:
        save_message(tg_id, text=f"Анкета заполнена пользователем {saved_user.name}")
        await message.answer(f"Приятно познакомиться, {saved_user.name}! Тебе {saved_user.age}.")
    else:
        await message.answer("Произошла ошибка при сохранении данных.")

    await state.clear()