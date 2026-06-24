"""WHOIS информация"""

import whois
from datetime import datetime, timezone
from core.utils import section, ok, err, info, table, warn


class WhoisModule:
    """WHOIS lookup домена"""

    def run(self, domain):
        section(f"WHOIS: {domain}")

        try:
            w = whois.whois(domain)

            data = {
                "Домен": w.domain_name,
                "Регистратор": w.registrar,
                "Создан": self._fmt(w.creation_date),
                "Истекает": self._fmt(w.expiration_date),
                "Обновлен": self._fmt(w.updated_date),
                "Статус": w.status,
                "DNSSEC": w.dnssec,
                "NS": w.name_servers,
                "Организация": w.org or w.name,
                "Страна": w.country,
                "Email": w.emails,
            }

            table(data, f"WHOIS: {domain}")

            # Проверка срока
            exp = w.expiration_date
            if isinstance(exp, list):
                exp = exp[0]
            if isinstance(exp, datetime):
                if exp.tzinfo is None:
                    exp = exp.replace(tzinfo=timezone.utc)
                days = (exp - datetime.now(timezone.utc)).days
                if days < 30:
                    warn(f"Домен истекает через {days} дней!")
                elif days < 90:
                    info(f"До истечения: {days} дней")
                else:
                    ok(f"Активен, {days} дней осталось")

            return data

        except Exception as e:
            err(f"WHOIS не удался: {e}")
            return {}

    def _fmt(self, d):
        if d is None:
            return None
        if isinstance(d, list):
            d = d[0]
        if isinstance(d, datetime):
            return d.strftime("%Y-%m-%d")
        return str(d)
