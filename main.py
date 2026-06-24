"""
OSINT Swiss Knife v2.0

Разведка доменов, IP-адресов, email, никнеймов.
12 модулей: DNS, WHOIS, Geo, Subdomains, Headers, 
Breaches, SSL, PortScan, Robots, Social, Meta, Screenshot.
"""

import json
import os
import sys

from core.utils import banner, section, ok, err, info, warn, table, save_json, console
from core.utils import is_ip, is_email, resolve_ip
from modules.dns import DNSModule
from modules.whois_mod import WhoisModule
from modules.geo import GeoModule
from modules.subdomains import SubdomainModule
from modules.headers import HeadersModule
from modules.breaches import BreachModule
from modules.ssl_check import SSLModule
from modules.port_scan import PortScanModule
from modules.robots_sitemap import RobotsModule
from modules.social_check import SocialCheckModule
from modules.meta_parser import MetaParserModule
from modules.screenshot import ScreenshotModule


def menu():
    """Главное меню"""
    console.print("\n[bold cyan]--- Меню OSINT Swiss Knife ---[/bold cyan]")
    console.print("  [white]1.[/white] [green]Полная разведка домена[/green]")
    console.print("  [white]2.[/white] [green]Разведка IP-адреса[/green]")
    console.print("  [white]3.[/white] [yellow]Субдомены[/yellow]")
    console.print("  [white]4.[/white] [magenta]HTTP заголовки[/magenta]")
    console.print("  [white]5.[/white] [red]Утечки email (HIBP)[/red]")
    console.print("  [white]6.[/white] [blue]SSL/TLS сертификат[/blue]")
    console.print("  [white]7.[/white] [green]Скан портов[/green]")
    console.print("  [white]8.[/white] [yellow]Robots.txt / Sitemap[/yellow]")
    console.print("  [white]9.[/white] [magenta]Проверка username[/magenta]")
    console.print("  [white]10.[/white] [blue]Meta / OpenGraph парсер[/blue]")
    console.print("  [white]11.[/white] [white]Сохранить страницу[/white]")
    console.print("  [white]12.[/white] [white]Массовая проверка (из файла)[/white]")
    console.print("  [white]0.[/white] [dim]Выход[/dim]")


def ask(prompt):
    console.print(f"[bold yellow]> {prompt}:[/bold yellow]", end=" ")
    return input().strip()


def ask_yn(prompt):
    console.print(f"[bold yellow]? {prompt}[/bold yellow] [dim](y/n)[/dim]", end=" ")
    return input().strip().lower() in ("y", "yes", "да", "д")


def full_recon_domain(domain):
    """Полная разведка домена"""
    results = {"target": domain, "type": "domain", "modules": {}}

    dns = DNSModule()
    results["modules"]["dns"] = dns.run(domain)

    whois = WhoisModule()
    results["modules"]["whois"] = whois.run(domain)

    ip = resolve_ip(domain)
    if ip:
        results["resolved_ip"] = ip
        geo = GeoModule()
        results["modules"]["geolocation"] = geo.run(ip)

    if ask_yn("Проверить HTTP заголовки?"):
        hdr = HeadersModule()
        results["modules"]["headers"] = hdr.run(domain)

    if ask_yn("Проверить SSL сертификат?"):
        ssl = SSLModule()
        results["modules"]["ssl"] = ssl.run(domain)

    if ask_yn("Сканировать порты?"):
        if ip:
            ps = PortScanModule()
            results["modules"]["portscan"] = ps.run(ip)

    if ask_yn("Искать субдомены?"):
        sub = SubdomainModule()
        results["modules"]["subdomains"] = sub.run(domain)

    if ask_yn("Проверить robots.txt?"):
        rb = RobotsModule()
        results["modules"]["robots"] = rb.run(domain)

    if ask_yn("Спарсить meta-теги?"):
        meta = MetaParserModule()
        results["modules"]["meta"] = meta.run(domain)

    if ask_yn("Сохранить страницу?"):
        scr = ScreenshotModule()
        results["modules"]["screenshot"] = scr.run(domain)

    return results


def recon_ip(ip):
    """Разведка IP"""
    results = {"target": ip, "type": "ip", "modules": {}}

    geo = GeoModule()
    results["modules"]["geolocation"] = geo.run(ip)

    if ask_yn("Сканировать порты?"):
        ps = PortScanModule()
        results["modules"]["portscan"] = ps.run(ip)

    return results


def bulk_check():
    """Массовая проверка из файла"""
    path = ask("Путь к файлу со списком целей")
    if not os.path.exists(path):
        err("Файл не найден")
        return []

    with open(path, "r") as f:
        targets = [l.strip() for l in f if l.strip()]

    info(f"Загружено {len(targets)} целей")
    all_results = []

    for i, t in enumerate(targets, 1):
        console.print(f"\n[bold cyan]--- Цель {i}/{len(targets)}: {t} ---[/bold cyan]")
        try:
            if is_ip(t):
                r = recon_ip(t)
            elif is_email(t):
                br = BreachModule()
                r = br.run(t)
            else:
                r = full_recon_domain(t)
            all_results.append(r)
        except Exception as e:
            err(f"Ошибка: {e}")
            all_results.append({"target": t, "error": str(e)})

    return all_results


def main():
    banner()

    while True:
        menu()
        choice = ask("Выбор")

        if choice == "0":
            console.print("\n[bold green]Пока![/bold green]\n")
            break

        elif choice == "1":
            domain = ask("Домен")
            if not domain:
                err("Пусто")
                continue
            results = full_recon_domain(domain)
            if ask_yn("Сохранить в JSON?"):
                fname = ask("Имя файла") or f"{domain}_recon"
                if not fname.endswith(".json"):
                    fname += ".json"
                save_json(results, os.path.join("reports", fname))

        elif choice == "2":
            ip = ask("IP-адрес")
            if not is_ip(ip):
                err("Неверный IP")
                continue
            results = recon_ip(ip)
            if ask_yn("Сохранить в JSON?"):
                fname = ask("Имя файла") or f"{ip}_recon"
                if not fname.endswith(".json"):
                    fname += ".json"
                save_json(results, os.path.join("reports", fname))

        elif choice == "3":
            domain = ask("Домен")
            sub = SubdomainModule()
            results = sub.run(domain)
            if ask_yn("Сохранить?"):
                fname = ask("Имя файла") or f"{domain}_subs"
                save_json(results, os.path.join("reports", fname + ".json"))

        elif choice == "4":
            url = ask("URL или домен")
            hdr = HeadersModule()
            hdr.run(url)

        elif choice == "5":
            email = ask("Email")
            br = BreachModule()
            br.run(email)

        elif choice == "6":
            domain = ask("Домен")
            port = ask("Порт (по умолчанию 443)")
            port = int(port) if port.isdigit() else 443
            ssl = SSLModule()
            ssl.run(domain, port)

        elif choice == "7":
            ip = ask("IP-адрес")
            if not is_ip(ip):
                err("Неверный IP")
                continue
            ps = PortScanModule()
            ps.run(ip)

        elif choice == "8":
            domain = ask("Домен")
            rb = RobotsModule()
            rb.run(domain)

        elif choice == "9":
            username = ask("Username")
            soc = SocialCheckModule()
            soc.run(username)

        elif choice == "10":
            url = ask("URL или домен")
            meta = MetaParserModule()
            meta.run(url)

        elif choice == "11":
            url = ask("URL или домен")
            scr = ScreenshotModule()
            scr.run(url)

        elif choice == "12":
            results = bulk_check()
            if results and ask_yn("Сохранить все результаты?"):
                fname = ask("Имя файла") or "bulk_results"
                save_json({"bulk": results}, os.path.join("reports", fname + ".json"))

        else:
            err("Нет такого пункта")

        console.print("\n[dim]Enter для продолжения...[/dim]")
        input()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[red]Прервано[/red]")
        sys.exit(0)
