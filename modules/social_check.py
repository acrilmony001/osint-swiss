"""Проверка никнейма на платформах"""

import requests
from core.utils import section, ok, err, info


class SocialCheckModule:
    """Проверка занятости username на популярных платформах"""

    PLATFORMS = {
        "GitHub": "https://github.com/{}",
        "Twitter/X": "https://x.com/{}",
        "Instagram": "https://instagram.com/{}",
        "Reddit": "https://reddit.com/user/{}",
        "TikTok": "https://tiktok.com/@{}",
        "Telegram": "https://t.me/{}",
        "YouTube": "https://youtube.com/@{}",
        "Twitch": "https://twitch.tv/{}",
    }

    def check(self, username):
        section(f"Проверка username: @{username}")

        results = {}
        session = requests.Session()
        session.headers.update({"User-Agent": "Mozilla/5.0"})
        session.timeout = 10

        for name, url_template in self.PLATFORMS.items():
            url = url_template.format(username)
            try:
                r = session.get(url, allow_redirects=False)
                # Если 200 — скорее всего занят, если 404 — свободен
                if r.status_code == 200:
                    results[name] = {"status": "occupied", "url": url}
                    ok(f"{name}: занят ({url})")
                elif r.status_code == 404:
                    results[name] = {"status": "free", "url": url}
                    info(f"{name}: свободен")
                else:
                    results[name] = {"status": "unknown", "code": r.status_code}
                    info(f"{name}: неизвестно (код {r.status_code})")
            except Exception as e:
                results[name] = {"status": "error", "error": str(e)}
                err(f"{name}: ошибка")

        occupied = [k for k, v in results.items() if v["status"] == "occupied"]
        free = [k for k, v in results.items() if v["status"] == "free"]

        info(f"\nЗанято: {len(occupied)}, Свободно: {len(free)}")

        return {"username": username, "results": results}

    def run(self, username):
        return self.check(username)
