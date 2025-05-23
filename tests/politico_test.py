import pytest
from news_parser import parse_article

from datetime import datetime

# Load the sample HTML for Politico
@pytest.fixture
def politico_html():
    with open("tests/samples/politico.html", "r", encoding="utf-8") as file:
        return file.read()
    
@pytest.fixture
def article_url():
    return "https://www.politico.com/news/2025/01/24/trump-leans-in-on-targeting-russian-oil-revenue-as-he-tries-to-fulfill-pledge-to-end-ukraine-war-00112345"

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
        == "'Everyone wants him out': How Musk helped boot Ramaswamy from DOGE"
    )

def test_parse_author(parsed_article):
    author = parsed_article.authors
    assert author == {
        "Adam Wren",
        "Holly Otterbein",
    }

def test_parse_date(parsed_article):
    date = parsed_article.time
    assert date == datetime.fromisoformat("2025-01-20T19:07-0500")

def test_parse_paragraphs(parsed_article):
    paragraphs = parsed_article.paragraphs

    assert len(paragraphs) == 21

    assert "Elon Musk has already achieved his first cut at the so-called Department of Government Efficiency: his co-leader Vivek Ramaswamy." in paragraphs[0]

def test_parse_tags(parsed_article):
    tags = parsed_article.tags
    assert tags == {
        "Ohio",
        "Donald Trump",
        "Donald Trump 2024",
        "Elon Musk",
        "Mike Johnson",
        "Vivek Ramaswamy",
        "DOGE"
    }