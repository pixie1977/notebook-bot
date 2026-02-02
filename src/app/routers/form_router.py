from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from src.infra.db_service import save_user, save_message

router = Router()

class Form(StatesGroup):
    """
    Класс, описывающий состояния формы.
    """
    name = State()
    age = State()


@router.message(Command("myage"))
async def cmd_start(message: Message, state: FSMContext):
    """
    Обработчик команды /start.
    Инициализирует машину состояний (FSM), устанавливает состояние Form.name.

    :param message: Объект входящего сообщения от пользователя.
    :param state: Контекст состояния FSM для хранения данных между шагами.
    """
    await state.set_state(Form.name)
    await message.answer("Привет! Как тебя зовут?")


@router.message(Form.name)
async def process_name(message: Message, state: FSMContext):
    """
    Обработчик ввода имени.
    Сохраняет имя в FSM-хранилище и переводит пользователя в состояние ожидания возраста.

    :param message: Сообщение с именем пользователя.
    :param state: Контекст состояния для обновления данных и смены состояния.
    """
    await state.update_data(name=message.text)
    await state.set_state(Form.age)
    await message.answer("Сколько тебе лет?")


@router.message(Form.age)
async def process_age(message: Message, state: FSMContext):
    """
    Обработчик ввода возраста.
    Сохраняет возраст, извлекает все данные из FSM, выводит персональное приветствие
    и завершает сессию, очищая состояние.

    :param message: Сообщение с возрастом пользователя.
    :param state: Контекст состояния для получения данных и очистки FSM.
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