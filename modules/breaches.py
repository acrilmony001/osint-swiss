"""Проверка email на утечки"""

import requests
from core.utils import section, ok, err, info, warn
from core import config


class BreachModule:
    """Проверка через Have I Been Pwned"""

    def __init__(self):
        self.key = config.HIBP_KEY

    def check_email(self, email):
        section(f"Утечки: {email}")

        if not self.key:
            warn("HIBP API ключ не настроен")
            info("Получить ключ: https://haveibeenpwned.com/API/Key")
            return {"email": email, "breaches": [], "count": 0, "note": "no_api_key"}

        try:
            r = requests.get(
                f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}",
                headers={
                    "hibp-api-key": self.key,
                    "User-Agent": "OSINT-Swiss-Knife"
                },
                timeout=config.TIMEOUT
            )

            if r.status_code == 404:
                ok("Утечек не найдено")
                return {"email": email, "breaches": [], "count": 0}

            if r.status_code == 200:
                data = r.json()
                warn(f"Найдено {len(data)} утечек!")
                for b in data[:5]:
                    info(f"  • {b.get('Name')} ({b.get('BreachDate')})")
                if len(data) > 5:
                    info(f"  ... и ещё {len(data) - 5}")

                return {
                    "email": email,
                    "breaches": data,
                    "count": len(data)
                }

            err(f"HIBP ответил {r.status_code}")
            return {}

        except Exception as e:
            err(f"Ошибка запроса: {e}")
            return {}

    def run(self, target):
        return self.check_email(target)
