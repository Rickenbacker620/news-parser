import pytest
from news_parser import parse_article

from datetime import datetime

@pytest.fixture
def reuters_html():
    with open("tests/samples/reuters.html", "r", encoding="utf-8") as file:
        return file.read()

@pytest.fixture
def article_url():
    return "https://www.reuters.com/world/africa/sudans-rsf-fighters-say-they-plan-work-with-new-government-raising-partition-2024-12-20/?id=K6F6QMFP3ZJ6ZH7SLNEK2BHFY4"

@pytest.fixture
def parsed_article(reuters_html, article_url):
    return parse_article(
        url=article_url,
        html=reuters_html,
    )

def test_parse_title(parsed_article):
    title = parsed_article.title
    assert (
        title
        == "Sudan's RSF fighters say they plan to work with new government, raising partition fears"
    )

def test_parse_author(parsed_article):
    author = parsed_article.authors
    assert author == {
        "Khalid Abdelaziz",
        "Nafisa Eltahir",
    }

def test_parse_date(parsed_article):
    date = parsed_article.time
    assert date == datetime.fromisoformat("2024-12-20T16:09:36.828")

def test_parse_paragraphs(parsed_article):
    paragraphs = parsed_article.paragraphs

    assert len(paragraphs) == 24

    assert " DUBAI/CAIRO, Dec 20 (Reuters) - Sudan's Rapid Support Forces (RSF) fighters have said they will" in paragraphs[0]

def test_parse_tags(parsed_article):
    tags = parsed_article.tags
    assert tags == {
        "RSBI:HUMAN-RIGHTS", "TOPIC:WORLD-SUDAN", "ADVO", "CIV", "CMPNY", "CWP", "DIP", "GEN",
        "HMAC", "HRGT", "INDG", "INDG08", "INDS", "INDS08", "INTAG", "LOCOS", "MACH", "MACH08",
        "NEWS1", "NGO", "POL", "PRIVT", "UN1", "WAR", "EASIA", "AMERS", "SWASIA", "AFR", "US",
        "MEAST", "SD", "NAFR", "TGLF", "NAMER", "EMEA", "ASXPAC", "EMRG", "AE", "CN", "ASIA", "EG",
        "DEST:CSA", "DEST:LBY", "DEST:REULB", "DEST:GFN", "DEST:G", "DEST:RAST", "DEST:PGE", 
        "DEST:RNP", "DEST:AFA", "DEST:PSC", "DEST:DNP", "DEST:AFN", "DEST:UCDPTEST", "DEST:RWSA", 
        "DEST:GNS", "DEST:RWS", "DEST:RBN", "DEST:OUSWDM", "DEST:OZATPM", "PACKAGE:WORLD-NEWS"
    }
