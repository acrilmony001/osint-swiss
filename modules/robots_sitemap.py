"""Анализ robots.txt и sitemap.xml"""

import requests
from core.utils import section, ok, err, info, warn
from core import config


class RobotsModule:
    """Парсинг robots.txt и поиск sitemap"""

    def run(self, domain):
        if not domain.startswith("http"):
            url = "https://" + domain
        else:
            url = domain

        section(f"Robots/Sitemap: {domain}")

        results = {"robots": {}, "sitemaps": []}

        # robots.txt
        try:
            r = requests.get(f"{url}/robots.txt", timeout=config.TIMEOUT, headers=config.HEADERS, proxies=config.PROXIES)
            if r.status_code == 200:
                lines = r.text.splitlines()
                disallowed = [l for l in lines if l.startswith("Disallow:")]
                sitemaps = [l.split(": ")[1] for l in lines if l.startswith("Sitemap:")]

                ok(f"robots.txt найден")
                info(f"Запрещённых путей: {len(disallowed)}")

                if disallowed:
                    for d in disallowed[:10]:
                        info(f"  {d}")
                    if len(disallowed) > 10:
                        info(f"  ... и ещё {len(disallowed) - 10}")

                if sitemaps:
                    ok(f"Найдено sitemap: {len(sitemaps)}")
                    for s in sitemaps:
                        info(f"  {s}")
                    results["sitemaps"] = sitemaps

                results["robots"] = {
                    "found": True,
                    "disallowed_count": len(disallowed),
                    "sitemap_count": len(sitemaps),
                }
            else:
                warn(f"robots.txt вернул {r.status_code}")
                results["robots"] = {"found": False, "status": r.status_code}

        except Exception as e:
            err(f"robots.txt не доступен: {e}")
            results["robots"] = {"found": False, "error": str(e)}

        # Попробуем найти sitemap.xml напрямую
        if not results["sitemaps"]:
            try:
                r = requests.get(f"{url}/sitemap.xml", timeout=config.TIMEOUT, headers=config.HEADERS, proxies=config.PROXIES)
                if r.status_code == 200:
                    ok("sitemap.xml найден напрямую")
                    results["sitemaps"].append(f"{url}/sitemap.xml")
            except:
                pass

        return results
