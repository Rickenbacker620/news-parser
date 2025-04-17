from parsel import Selector

from news_parser.cnn import CNNParser

def parse_article(url: str, html: str | Selector):
    mapping = {
        "cnn": CNNParser,
    }

    for key, parser in mapping.items():
        if key in url:
            return parser(html=html, url=url).parse()