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