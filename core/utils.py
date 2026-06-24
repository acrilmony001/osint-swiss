"""Утилиты и красивый вывод"""

import re
import os
import socket
import ipaddress
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


def is_ip(addr):
    """Проверка, является ли строка IP-адресом"""
    try:
        ipaddress.ip_address(addr)
        return True
    except ValueError:
        return False


def is_email(addr):
    """Проверка, является ли строка email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, addr))


def resolve_ip(domain):
    """Получить IP по домену"""
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None


def banner():
    """Приветственный баннер"""
    text = """
    ┌─────────────────────────────────────┐
    │      OSINT Swiss Knife              │
    │   Разведка доменов, IP, почт,       │
    │   утечки, субдомены, порты, SSL     │
    └─────────────────────────────────────┘
    """
    console.print(Panel(text, style="bold blue"))


def section(name):
    """Заголовок секции"""
    console.print(f"[bold yellow]━━━ {name} ━━━[/bold yellow]")


def ok(msg):
    console.print(f"[green]✓[/green] {msg}")


def err(msg):
    console.print(f"[red]✗[/red] {msg}")


def info(msg):
    console.print(f"[cyan]ℹ[/cyan] {msg}")


def warn(msg):
    console.print(f"[yellow]⚠[/yellow] {msg}")


def table(data, title=""):
    """Вывод словаря в виде таблицы"""
    if not data:
        info("Нет данных")
        return
    t = Table(title=title, show_header=True, header_style="bold magenta")
    t.add_column("Параметр", style="cyan")
    t.add_column("Значение", style="white")
    for k, v in data.items():
        if v is None:
            v = "[dim]—[/dim]"
        elif isinstance(v, list):
            v = " ".join(str(i) for i in v) if v else "[dim]—[/dim]"
        t.add_row(str(k), str(v))
    console.print(t)


def save_json(data, filename):
    """Сохранить результаты в JSON"""
    import json
    os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=str)
    ok(f"Сохранено: {filename}")
