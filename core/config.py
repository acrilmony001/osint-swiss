"""Конфигурация проекта"""

import os
from dotenv import load_dotenv

load_dotenv()

TIMEOUT = 15

# API ключи
HIBP_KEY = os.getenv("HIBP_KEY", "")

# Прокси
PROXY = os.getenv("PROXY", "")
PROXIES = {"http": PROXY, "https": PROXY} if PROXY else {}

# Юзер-агент
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
