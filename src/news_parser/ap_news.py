from parsel import Selector
from typing import Optional, Set
from datetime import datetime
import json
from .common import NewsParser

class APParser(NewsParser):
    def __init__(self, *, html: str | Selector = None, url: str = None):
        if html is not None and url is not None:
            super().__init__(url=url, html=html)
            self.selector = Selector(text=html) if isinstance(html, str) else html
            self.ld_json = self._load_ld_json()
        else:
            self.ld_json = {}

    def _load_ld_json(self) -> dict:
        json_text = self.selector.css('script#link-ld-json::text').get()
        if not json_text:
            return {}
        try:
            data = json.loads(json_text)
            if isinstance(data, list):
                for entry in data:
                    if entry.get("@type") == "NewsArticle":
                        return entry
            elif isinstance(data, dict) and data.get("@type") == "NewsArticle":
                return data
        except json.JSONDecodeError:
            pass
        return {}

    def get_title(self) -> str:
        if self.ld_json:
            title = self.ld_json.get("headline")
            if title:
                return title.strip()
        raw_title = self.selector.css("title::text").get()
        return raw_title.strip().removesuffix(" | AP News") if raw_title else ""

    # REVIEW
    def get_paragraphs(self) -> list[str]:
        description = self.ld_json.get("description")
        if description:
            return [description.strip()]

    def get_authors(self) -> Optional[Set[str]]:
        authors = set()
        for author in self.ld_json.get("author", []):
            name = author.get("name")
            if name:
                authors.add(name.title())
        return authors if authors else None

    def get_time(self) -> datetime:
        if "dateModified" in self.ld_json:
            try:
                return datetime.strptime(self.ld_json["dateModified"], "%Y-%m-%dT%H:%M:%SZ")
            except Exception:
                pass

    def get_tags(self) -> Optional[Set[str]]:
        tags = set()

        # From meta tags
        meta_tags = self.selector.css('meta[property="article:tag"]::attr(content)').getall()
        tags.update(tag.strip() for tag in meta_tags if tag.strip())

        return tags if tags else None