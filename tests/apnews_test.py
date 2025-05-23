import pytest
from news_parser import parse_article

from datetime import datetime

# Load the sample HTML for AP News
@pytest.fixture
def apnews_html():
    with open("tests/samples/apnews.html", "r", encoding="utf-8") as file:
        return file.read()
    
@pytest.fixture
def article_url():
    return "https://apnews.com/article/2025-01-24-politics-kemp-harm-to-law-enforcement-accountable"

@pytest.fixture
def parsed_article(apnews_html, article_url):
    return parse_article(
        url=article_url,
        html=apnews_html,
    )

def test_parse_title(parsed_article):
    title = parsed_article.title
    assert (
        title
        == "Trump leans in on targeting Russian oil revenue as he tries to fulfill pledge to end Ukraine war"
    )

def test_parse_author(parsed_article):
    author = parsed_article.authors
    assert author == {
        "Aamer Madhani",
        "Jennifer Mcdermott",
    }

def test_parse_date(parsed_article):
    time = parsed_article.time
    assert time == datetime.fromisoformat("2025-01-24T23:33:40")

def test_parse_paragraphs(parsed_article):
    paragraphs = parsed_article.paragraphs

    assert len(paragraphs) == 32

    assert "WASHINGTON (AP) — President Donald Trump is emphasizing that targeting Russia’s oil revenue is the best way to get Moscow to end its nearly three-year war against Ukraine." in paragraphs[0]

def test_parse_tags(parsed_article):
    tags = parsed_article.tags
    assert tags == {
        "Donald Trump",
        "War and unrest",
        "Keith Kellogg",
        "General news",
        "Russia",
        "Vladimir Putin",
        "Joe Biden",
        "Ukraine",
        "Karoline Leavitt",
        "OPEC"
    }
    assert len(tags) == 10