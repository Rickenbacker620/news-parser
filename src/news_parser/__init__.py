from parsel import Selector

from news_parser.ap_news import APParser
from news_parser.cnn import CNNParser
from news_parser.fox import FoxParser
from news_parser.reuters import ReutersParser
from news_parser.thehill import TheHillParser

def parse_article(*, url: str, html: str | Selector):
    mapping = {
        "apnews": APParser,
        "cnn": CNNParser,
        "foxnews": FoxParser,
        "reuters": ReutersParser,
        "thehill": TheHillParser,
    }

    for key, parser in mapping.items():
        if key in url:
            return parser(html=html, url=url).parse()