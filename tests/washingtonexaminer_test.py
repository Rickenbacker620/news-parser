import pytest
from news_parser import parse_article

from datetime import datetime

# Load the sample HTML for Washington Examiner
@pytest.fixture
def washingtonexaminer_html():
    with open("tests/samples/washingtonexaminer.html", "r", encoding="utf-8") as file:
        return file.read()
    
@pytest.fixture
def article_url():
    return "https://www.washingtonexaminer.com/news/3294031/congress-trump-bipartisan-inauguration-lunch-first-event-new-golden-age/"

@pytest.fixture
def parsed_article(washingtonexaminer_html, article_url):
    return parse_article(
        url=article_url,
        html=washingtonexaminer_html,
    )

def test_parse_title(parsed_article):
    title = parsed_article.title
    assert (
        title
        == "Congress fetes Trump with bipartisan inauguration lunch in first event of new ‘golden age’"
    )

def test_parse_author(parsed_article):
    author = parsed_article.authors
    assert author == {
        "Cami Mondeaux"
    }

def test_parse_date(parsed_article):
    date = parsed_article.time
    assert date == datetime.fromisoformat("2025-01-20T23:38:23+00:00")

def test_parse_paragraphs(parsed_article):
    paragraphs = parsed_article.paragraphs

    assert len(paragraphs) == 23

    assert "Shortly after President Donald Trump took the oath of office on Monday, the newly sworn-in commander in chief got to work to usher in what he and his allies call a" in paragraphs[0]

def test_parse_tags(parsed_article):
    tags = parsed_article.tags
    assert tags == {
        "Congress",
        "Donald Trump",
        "Trump Inauguration",
        "Trump Transition",
        "Washington D.C.",
        "White House",
    }