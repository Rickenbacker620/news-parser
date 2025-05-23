import pytest
from news_parser import parse_article

from datetime import datetime

# Load the sample HTML for The Hill
@pytest.fixture
def politico_html():
    with open("tests/samples/thehill.html", "r", encoding="utf-8") as file:
        return file.read()

@pytest.fixture
def article_url():
    return "https://thehill.com/policy/equilibrium-sustainability/5037593-mineral-water-forever-chemicals/"

@pytest.fixture
def parsed_article(politico_html, article_url):
    return parse_article(
        url=article_url,
        html=politico_html,
    )

def test_parse_title(parsed_article):
    title = parsed_article.title
    assert (
        title
        == "Scientists find 'forever chemical' byproduct in mineral water across Europe"
    )

def test_parse_author(parsed_article):
    author = parsed_article.authors
    assert author == {
        "Sharon Udasin",
    } 

def test_parse_date(parsed_article):
    date = parsed_article.time
    assert date == datetime.fromisoformat("2024-12-12T15:06:00-05:00")

def test_parse_paragraphs(parsed_article):
    paragraphs = parsed_article.paragraphs

    assert len(paragraphs) == 20

    assert "An extremely persistent and highly mobile" in paragraphs[0]

def test_parse_tags(parsed_article):
    tags = parsed_article.tags
    assert tags == {
    }