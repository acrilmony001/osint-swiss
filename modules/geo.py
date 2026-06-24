"""Геолокация IP-адреса"""

import requests
from core.utils import section, ok, err, info, table
from core import config


class GeoModule:
    """Определение местоположения по IP"""

    def run(self, ip):
        section(f"Геолокация: {ip}")

        try:
            r = requests.get(
                f"http://ip-api.com/json/{ip}",
                params={"fields": "status,country,countryCode,region,city,zip,lat,lon,timezone,isp,org,as,query"},
                timeout=config.TIMEOUT,
                proxies=config.PROXIES
            )
            data = r.json()

            if data.get("status") != "success":
                err(f"ip-api: {data.get('message', 'ошибка')}")
                return {}

            result = {
                "IP": data.get("query"),
                "Страна": f"{data.get('country')} ({data.get('countryCode')})",
                "Регион": data.get("regionName"),
                "Город": data.get("city"),
                "ZIP": data.get("zip"),
                "Координаты": f"{data.get('lat')}, {data.get('lon')}",
                "Часовой пояс": data.get("timezone"),
                "ISP": data.get("isp"),
                "Организация": data.get("org"),
                "AS": data.get("as"),
            }

            table(result, f"Геолокация: {ip}")

            lat, lon = data.get("lat"), data.get("lon")
            if lat and lon:
                info(f"Карта: https://maps.google.com/?q={lat},{lon}")

            return result

        except Exception as e:
            err(f"Геолокация не удалась: {e}")
            return {}
