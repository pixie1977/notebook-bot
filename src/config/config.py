from dotenv import load_dotenv
import os

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    raise ValueError("Не задан TELEGRAM_TOKEN в .env")

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
if not WEBHOOK_URL:
    raise ValueError("Не задан WEBHOOK_URL в .env")

COINGECKO_URL = os.getenv("COINGECKO_URL")
if not COINGECKO_URL:
    raise ValueError("Не задан COINGECKO_URL в .env")

DB_ADDR = os.getenv("DB_ADDR")
if not DB_ADDR:
    raise ValueError("Не задан DB_ADDR в .env")

OLLAMA_HOST= os.getenv("OLLAMA_HOST")
if not OLLAMA_HOST:
    raise ValueError("Не задан OLLAMA_HOST в .env")

OLLAMA_PORT= int(os.getenv("OLLAMA_PORT"))
if not OLLAMA_PORT:
    raise ValueError("Не задан OLLAMA_PORT в .env")

OLLAMA_MODEL_NAME= os.getenv("OLLAMA_MODEL_NAME")
if not OLLAMA_MODEL_NAME:
    raise ValueError("Не задан OLLAMA_MODEL_NAME в .env")

SYS_PROMT= os.getenv("SYS_PROMT")
if not SYS_PROMT:
    raise ValueError("Не задан SYS_PROMT в .env")

USER_REQUEST_MAX_LEN= int(os.getenv("USER_REQUEST_MAX_LEN"))
if not USER_REQUEST_MAX_LEN:
    raise ValueError("Не задан USER_REQUEST_MAX_LEN в .env")

OLLAMA_REQUEST_TIMEOUT= int(os.getenv("OLLAMA_REQUEST_TIMEOUT"))
if not OLLAMA_REQUEST_TIMEOUT:
    raise ValueError("Не задан OLLAMA_REQUEST_TIMEOUT в .env")