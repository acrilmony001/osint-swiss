# OSINT Swiss Knife v2.0

Интерактивный инструмент для сбора публичной информации.
12 модулей для разведки доменов, IP, email, никнеймов.

## Возможности

| # | Модуль | Описание |
|---|--------|----------|
| 1 | **DNS** | A, AAAA, MX, NS, TXT, SOA, CNAME, PTR |
| 2 | **WHOIS** | Регистратор, даты, владелец, статус |
| 3 | **Geo** | Страна, город, провайдер, координаты |
| 4 | **Subdomains** | Поиск через SSL-сертификаты (crt.sh) |
| 5 | **Headers** | HTTP заголовки, технологии |
| 6 | **Breaches** | Утечки email (Have I Been Pwned) |
| 7 | **SSL** | Анализ TLS-сертификата |
| 8 | **PortScan** | Топ-20 портов |
| 9 | **Robots** | robots.txt, sitemap.xml |
| 10 | **Social** | Проверка username на 8 платформах |
| 11 | **Meta** | Meta-теги, OpenGraph, Twitter Cards |
| 12 | **Screenshot** | HTML-дамп страницы |

## Установка

```bash
git clone https://github.com/ВАШ_НИК/osint-swiss.git
cd osint-swiss
pip install -r requirements.txt
```

## Запуск

```bash
python main.py
```

## API ключи (опционально)

```bash
cp .env.example .env
```

- **HIBP_KEY** — https://haveibeenpwned.com/API/Key

## Дисклеймер

Только для легального использования.

## Лицензия

MIT
