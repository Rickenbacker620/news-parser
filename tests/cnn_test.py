import pytest
from news_parser import parse_article

from datetime import datetime


# Load the sample HTML for CNN
@pytest.fixture
def cnn_html():
    with open("tests/samples/cnn.html", "r", encoding="utf-8") as file:
        return file.read()


@pytest.fixture
def article_url():
    return "https://www.cnn.com/2025/01/24/politics/kemp-harm-to-law-enforcement-accountable/index.html"


@pytest.fixture
def parsed_article(cnn_html, article_url):
    return parse_article(
        url=article_url,
        html=cnn_html,
    )


def test_parse_title(parsed_article):
    title = parsed_article.title
    assert (
        title
        == "Kemp says anyone who harms law enforcement ‘should be held fully accountable’ for actions"
    )


def test_parse_author(parsed_article):
    author = parsed_article.authors
    assert author == {"Kaitlan Collins"}


def test_parse_date(parsed_article):
    time = parsed_article.time
    assert time == datetime.fromisoformat("2025-01-24T22:19:42.412Z")


def test_parse_paragraphs(parsed_article):
    paragraphs = parsed_article.paragraphs

    assert len(paragraphs) == 10

    assert paragraphs[0].startswith(
        "Georgia Republican Gov. Brian Kemp criticized President Donald Trump’s"
    )
