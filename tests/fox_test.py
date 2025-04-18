import pytest
from news_parser import parse_article

from datetime import datetime


# Load the sample HTML for Fox
@pytest.fixture
def fox_html():
    with open("tests/samples/fox.html", "r", encoding="utf-8") as file:
        return file.read()


@pytest.fixture
def article_url():
    return "https://www.foxnews.com/us/fsu-shooter-identified-used-sheriff-deputy-moms-weapon-killing-police"


@pytest.fixture
def parsed_article(fox_html, article_url):
    return parse_article(
        url=article_url,
        html=fox_html,
    )


def test_parse_title(parsed_article):
    title = parsed_article.title
    assert (
        title
        == "FSU shooter identified, used sheriff deputy mom's weapon in killing: police"
    )


def test_parse_author(parsed_article):
    author = parsed_article.authors
    assert author == {
        "Rachel Wolf",
        "Preston Mizell",
        "David Spunt",
        "Andrea Margolis",
        "Ashley Papa",
    }


def test_parse_date(parsed_article):
    time = parsed_article.time
    print(time)
    assert time == datetime.fromisoformat("2025-04-17T18:57:24-04:00")


def test_parse_paragraphs(parsed_article):
    paragraphs = parsed_article.paragraphs

    assert len(paragraphs) == 33

    assert paragraphs[0].startswith(
        "Two people were killed, and six others were injured"
    )