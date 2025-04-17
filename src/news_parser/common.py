from abc import ABC, abstractmethod
from datetime import datetime
from typing import Annotated
from parsel import Selector
import re

from pydantic import (
    BaseModel,
    BeforeValidator,
    HttpUrl,
    StringConstraints,
    computed_field,
    field_validator,
)

def cleanup_content(v: str | list[str]) -> str:
    """Strip whitespace and replace \xa0 with space.
    if v is a list, join each paragraph with newlines.
    """
    # # Handle list input
    # if isinstance(v, list):
    #     # Strip each paragraph and join with newlines
    #     cleaned = "\n".join(para.strip() for para in v)
    # else:
    #     cleaned = v.strip()

    # Replace \xa0 with space
    v = v.replace("\xa0", " ")

    return v


ArticleTitle = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)
]
ArticleTag = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=40)
]
ArticleAuthor = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=40)
]
ArticleParagraph = Annotated[
    str, BeforeValidator(cleanup_content), StringConstraints(min_length=1)
]


class Article(BaseModel):
    """Article data model."""

    # url: a valid URL
    url: HttpUrl

    # title: length between 1 and 100, automatically strip whitespace
    title: ArticleTitle

    # authors: a set of strings
    authors: set[ArticleAuthor] | None = None  # type: ignore

    # tags: a set of strings
    tags: set[ArticleTag] | None = None

    # time: a datetime object the article was published
    time: datetime

    paragraphs: list[ArticleParagraph]

    @computed_field
    def content(self) -> str:
        """Join paragraphs with newlines."""
        return "\n".join(self.paragraphs)


    @field_validator("content")
    @classmethod
    def clean_and_validate_content(cls, v: str) -> str:
        if re.search(r"<[^>]+>", v):
            raise ValueError("String contains HTML tags")

        return v


class ParsingError(Exception):
    """Exception raised when article parsing fails."""

    def __init__(self, field: str, origin_exception: Exception):
        self.field = field
        super().__init__(f"Failed to parse {field}: {origin_exception}")


class NewsParser(ABC):
    """Abstract base class for article parsing with error handling and auto stripping."""

    def __init__(self, *, html: str | Selector, url: str):
        if isinstance(html, str):
            self.html = html
            self.selector = Selector(html)
        elif isinstance(html, Selector):
            self.html = html.get()
            self.selector = html
        else:
            raise ValueError("Invalid input type. Expected str or Selector.")
        self.url = url

    def parse(self) -> Article:

        try:
            title = self.get_title()
        except Exception as e:
            raise ParsingError("title", e)

        try:
            paragraphs = self.get_paragraphs()
        except Exception as e:
            raise ParsingError("paragraphs", e)

        try:
            authors = self.get_authors()
        except Exception as e:
            raise ParsingError("authors", e)

        try:
            tags = self.get_tags()
        except Exception as e:
            raise ParsingError("tags", e)

        try:
            time = self.get_time()
        except Exception as e:
            raise ParsingError("time", e)

        try:
            url = self.get_url()
        except Exception as e:
            raise ParsingError("url", e)

        return Article(
            url=url,
            title=title,
            paragraphs=paragraphs,
            authors=authors,
            tags=tags,
            time=time,
        )

    @abstractmethod
    def get_title(self) -> str:
        """Get the title of the article."""

    @abstractmethod
    def get_paragraphs(self) -> list[str]:
        """Get the paragraphs of the article as a list of strings."""

    @abstractmethod
    def get_authors(self) -> set[str] | None:
        """Get the authors of the article."""

    @abstractmethod
    def get_time(self) -> datetime:
        """Get the time of the article. Timezone will be automatically converted to the local timezone if not specified."""

    @abstractmethod
    def get_tags(self) -> set[str] | None:
        """Get the tags of the article."""

    def get_url(self) -> str:
        """Get the URL of the article."""
        return self.url