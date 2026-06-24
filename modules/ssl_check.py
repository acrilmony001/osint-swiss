"""Анализ SSL/TLS сертификата"""

import ssl
import socket
from datetime import datetime
from core.utils import section, ok, err, info, table, warn


class SSLModule:
    """Проверка SSL-сертификата сайта"""

    def run(self, domain, port=443):
        section(f"SSL/TLS: {domain}:{port}")

        try:
            context = ssl.create_default_context()
            with socket.create_connection((domain, port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    cipher = ssock.cipher()
                    version = ssock.version()

            if not cert:
                err("Сертификат не получен")
                return {}

            # Парсим данные
            subject = dict(x[0] for x in cert.get("subject", []))
            issuer = dict(x[0] for x in cert.get("issuer", []))

            not_before = cert.get("notBefore")
            not_after = cert.get("notAfter")

            # Парсим даты
            def parse_date(d):
                if d:
                    return datetime.strptime(d, "%b %d %H:%M:%S %Y %Z").strftime("%Y-%m-%d")
                return None

            result = {
                "Домен": subject.get("commonName", "—"),
                "Организация": subject.get("organizationName", "—"),
                "Выдан": issuer.get("commonName", "—"),
                "Действует с": parse_date(not_before),
                "Действует до": parse_date(not_after),
                "Версия TLS": version,
                "Шифр": cipher[0] if cipher else "—",
                "SAN": cert.get("subjectAltName", []),
            }

            table(result, f"SSL сертификат: {domain}")

            # Проверка срока
            if not_after:
                exp = datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
                days = (exp - datetime.now()).days
                if days < 30:
                    warn(f"Сертификат истекает через {days} дней!")
                elif days < 90:
                    info(f"До истечения сертификата: {days} дней")
                else:
                    ok(f"Сертификат активен, {days} дней осталось")

            return result

        except Exception as e:
            err(f"SSL проверка не удалась: {e}")
            return {}
