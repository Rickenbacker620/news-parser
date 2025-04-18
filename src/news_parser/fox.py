from parsel import Selector
from typing import Optional, Set
from datetime import datetime

from news_parser.utils import get_all_text
from .common import NewsParser

class FoxParser(NewsParser):
    def __init__(self, *, html: str | Selector = None, url: str = None):
        if html is not None and url is not None:
            super().__init__(url=url, html=html)
        else:
            # Default constructor for when the parse method will be called separately
            pass

    def get_title(self) -> str:
        title = self.selector.css(".headline.speakable::text").get()
        return title.strip() if title else ""

    def get_paragraphs(self) -> list[str]:
        paragraphs = []
        # Extract paragraphs from the main article body
        elements = self.selector.css(".article-body>p")
        for element in elements:
            text = get_all_text(element)
            if text and not text.isupper():
                paragraphs.append(text.strip())

        return paragraphs

    def get_authors(self) -> Optional[Set[str]]:
        authors = set()
        elements = self.selector.css("div.author-byline > span > span > a::text")
        for element in elements:
            authors.add(element.get().strip())
        return authors if authors else None

    def get_time(self) -> datetime:
        time_str = self.selector.css("meta[data-hid='dcterms.modified']::attr(content)").get()
        if time_str:
            return datetime.fromisoformat(time_str)
        raise ValueError("No valid date found in HTML.")

    def get_tags(self) -> Optional[Set[str]]:
        tags = set()
        elements = self.selector.css(".eyebrow > a::text")
        for element in elements:
            tag = element.get()
            if tag:
                tag = tag.strip()
                if tag == "Fox News First":
                    raise ValueError("Unrelated tag found: Fox News First")
                tags.add(tag)
        return tags if tags else None
