from parsel import Selector

from news_parser.cnn import CNNParser
from news_parser.fox import FoxParser

def parse_article(*, url: str, html: str | Selector):
    mapping = {
        "cnn": CNNParser,
        "foxnews": FoxParser,
    }

    for key, parser in mapping.items():
        if key in url:
            return parser(html=html, url=url).parse()