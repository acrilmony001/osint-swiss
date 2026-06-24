"""Парсинг meta-тегов и OpenGraph"""

import requests
from bs4 import BeautifulSoup
from core.utils import section, ok, err, info, table
from core import config


class MetaParserModule:
    """Извлечение мета-информации со страницы"""

    def run(self, url):
        if not url.startswith("http"):
            url = "https://" + url

        section(f"Meta-теги: {url}")

        try:
            r = requests.get(url, timeout=config.TIMEOUT, headers=config.HEADERS, proxies=config.PROXIES)
            soup = BeautifulSoup(r.text, "html.parser")

            result = {}

            # Title
            title = soup.find("title")
            if title:
                result["Title"] = title.get_text(strip=True)
                ok(f"Title: {result['Title'][:60]}")

            # Meta description
            desc = soup.find("meta", attrs={"name": "description"})
            if desc:
                result["Description"] = desc.get("content", "")[:100]

            # OpenGraph
            og_tags = {}
            for tag in soup.find_all("meta", attrs={"property": True}):
                prop = tag.get("property", "")
                if prop.startswith("og:"):
                    og_tags[prop] = tag.get("content", "")

            if og_tags:
                result["OpenGraph"] = og_tags
                ok(f"OpenGraph тегов: {len(og_tags)}")

            # Twitter Cards
            twitter_tags = {}
            for tag in soup.find_all("meta", attrs={"name": True}):
                name = tag.get("name", "")
                if name.startswith("twitter:"):
                    twitter_tags[name] = tag.get("content", "")

            if twitter_tags:
                result["Twitter Cards"] = twitter_tags

            # Favicon
            favicon = soup.find("link", attrs={"rel": "icon"}) or soup.find("link", attrs={"rel": "shortcut icon"})
            if favicon:
                result["Favicon"] = favicon.get("href", "")

            # Generator (CMS)
            generator = soup.find("meta", attrs={"name": "generator"})
            if generator:
                result["Generator/CMS"] = generator.get("content", "")
                info(f"CMS: {result['Generator/CMS']}")

            # Все meta-теги
            all_meta = {}
            for tag in soup.find_all("meta"):
                name = tag.get("name") or tag.get("property")
                content = tag.get("content")
                if name and content:
                    all_meta[name] = content

            result["_all_meta"] = all_meta

            # Ссылки
            links = [a.get("href") for a in soup.find_all("a", href=True)]
            external = [l for l in links if l and l.startswith("http") and url not in l]
            result["Внешних ссылок"] = len(external)

            table(result, f"Meta-информация: {url}")

            return result

        except Exception as e:
            err(f"Парсинг не удался: {e}")
            return {}
