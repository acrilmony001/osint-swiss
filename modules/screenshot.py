"""Сохранение HTML-дампа страницы"""

import requests
import os
from core.utils import section, ok, err, info
from core import config


class ScreenshotModule:
    """Сохранение страницы для офлайн-анализа"""

    def run(self, url, outdir="reports"):
        if not url.startswith("http"):
            url = "https://" + url

        section(f"Сохранение: {url}")

        try:
            r = requests.get(
                url,
                timeout=config.TIMEOUT,
                headers=config.HEADERS,
                proxies=config.PROXIES
            )

            os.makedirs(outdir, exist_ok=True)
            fname = url.replace("https://", "").replace("http://", "").replace("/", "_")[:50]
            path = os.path.join(outdir, f"{fname}.html")

            with open(path, "w", encoding="utf-8") as f:
                f.write(r.text)

            ok(f"Сохранено: {path} ({len(r.text)} байт)")
            return {"url": url, "saved_to": path, "size": len(r.text)}

        except Exception as e:
            err(f"Не удалось сохранить: {e}")
            return {}
