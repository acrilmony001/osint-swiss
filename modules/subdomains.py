"""Перечисление субдоменов"""

import requests
from core.utils import section, ok, err, info


class SubdomainModule:
    """Поиск субдоменов через открытые источники"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        self.session.timeout = 15

    def crt_sh(self, domain):
        """Поиск через crt.sh (SSL сертификаты)"""
        info("Запрос к crt.sh...")
        try:
            r = self.session.get(f"https://crt.sh/?q=%.{domain}&output=json")
            if r.status_code != 200:
                err(f"crt.sh вернул {r.status_code}")
                return set()

            data = r.json()
            found = set()
            for entry in data:
                names = entry.get("name_value", "").split("\n")
                for name in names:
                    name = name.strip()
                    if name and name.endswith(domain) and name != domain:
                        found.add(name)

            return found

        except Exception as e:
            err(f"crt.sh ошибка: {e}")
            return set()

    def run(self, domain):
        section(f"Субдомены: {domain}")

        all_subs = set()

        crt = self.crt_sh(domain)
        all_subs.update(crt)
        if crt:
            ok(f"crt.sh: {len(crt)} найдено")

        if all_subs:
            ok(f"Всего уникальных: {len(all_subs)}")
            for s in sorted(all_subs)[:25]:
                info(f"  • {s}")
            if len(all_subs) > 25:
                info(f"  ... и ещё {len(all_subs) - 25}")
        else:
            err("Субдомены не найдены")

        return {
            "domain": domain,
            "total": len(all_subs),
            "subdomains": sorted(all_subs),
        }
