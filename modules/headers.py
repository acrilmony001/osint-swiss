"""Анализ HTTP заголовков"""

import requests
from core.utils import section, ok, err, info, table
from core import config


class HeadersModule:
    """Анализ ответа веб-сервера"""

    def run(self, url):
        if not url.startswith("http"):
            url = "https://" + url

        section(f"HTTP заголовки: {url}")

        try:
            r = requests.get(
                url,
                timeout=config.TIMEOUT,
                headers=config.HEADERS,
                proxies=config.PROXIES,
                allow_redirects=True
            )

            info(f"Статус: {r.status_code}")
            info(f"URL: {r.url}")

            interesting = {}
            for k, v in r.headers.items():
                kl = k.lower()
                if kl in ["server", "x-powered-by", "via", "x-frame-options",
                          "content-security-policy", "strict-transport-security",
                          "x-content-type-options", "x-xss-protection"]:
                    interesting[k] = v

            if interesting:
                table(interesting, "Заголовки безопасности")

            srv = r.headers.get("Server", "")
            if srv:
                info(f"Сервер: {srv}")
            xpb = r.headers.get("X-Powered-By", "")
            if xpb:
                info(f"Powered by: {xpb}")

            return {
                "url": r.url,
                "status": r.status_code,
                "headers": dict(r.headers),
                "interesting": interesting,
            }

        except Exception as e:
            err(f"Запрос не удался: {e}")
            return {}
