from parsel import Selector


def get_all_text(element: Selector) -> str:

    return element.xpath('string(.)').get()