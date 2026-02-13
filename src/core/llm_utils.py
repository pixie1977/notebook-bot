import logging
import requests

from src.config.config import (
    OLLAMA_PORT,
    OLLAMA_MODEL_NAME,
    SYS_PROMT,
    USER_REQUEST_MAX_LEN,
    OLLAMA_REQUEST_TIMEOUT,
)

URL = f"http://host.docker.internal:{OLLAMA_PORT}/api/chat"
DEFAULT_SYS_PROMT_MSG = {"role": "system", "content": "Ты — полезный помощник. Отвечай на русском языке."}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_request(user_request: str) -> dict:
    """Создаёт тело запроса к Ollama API на основе пользовательского ввода."""
    if not user_request:
        raise ValueError("Empty user request")

    trimmed_text = (
        user_request[:USER_REQUEST_MAX_LEN] + "..."
        if len(user_request) > USER_REQUEST_MAX_LEN
        else user_request
    )

    messages = [{"role": "user", "content": trimmed_text}]

    if SYS_PROMT:
        messages.insert(0, {"role": "system", "content": SYS_PROMT})
    else:
        messages.insert(0, DEFAULT_SYS_PROMT_MSG)

    data = {
        "model": OLLAMA_MODEL_NAME,
        "messages": messages,
        "stream": False,
    }
    return data


def process_llm_request(user_request: str) -> str:
    """Отправляет запрос к LLM и возвращает ответ или сообщение об ошибке."""
    try:
        data = create_request(user_request)
        response = requests.post(URL, json=data, timeout=OLLAMA_REQUEST_TIMEOUT)  # добавлен таймаут
        response.raise_for_status()

        result = response.json()
        return result["message"]["content"]

    except requests.exceptions.Timeout:
        logger.warning("Таймаут при запросе к Ollama")
        return "Прости, не успел получить ответ — задумался над глубоким вопросом!"

    except requests.exceptions.ConnectionError:
        logger.error(
            "Не удалось подключиться к Ollama. Убедитесь, что Ollama запущен и доступен по %s",
            URL,
        )
        return "Сервис искусственного интеллекта временно недоступен. Проверь, запущен ли Ollama!"

    except requests.exceptions.RequestException as e:
        logger.warning(f"Ошибка при запросе к Ollama: {e}")
        if 'response' in locals():
            logger.warning(f"Статус код: {response.status_code}")
            logger.warning(f"Тело ответа: {response.text}")
        return "Что-то пошло не так при общении с ИИ..."

    except KeyError:
        logger.warning("В ответе нет ожидаемого поля 'message.content'")
        return "ИИ ответил странно... ничего не понятно."