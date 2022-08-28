import pytest

from replyowl import ReplyOwl

from .reply_cases import ReplyCases


@pytest.mark.parametrize(**ReplyCases.compose_reply().__dict__)
@pytest.mark.parametrize("make_html", (True, False), ids=["html", "no_html"])
@pytest.mark.parametrize("make_text", (True, False), ids=["text", "no_text"])
def test_compose_reply(
    owl: ReplyOwl,
    content: str,
    quote_html: str,
    quote_text: str,
    expected_html: str,
    expected_text: str,
    quote_attribution: str,
    make_text: bool,
    make_html: bool,
) -> None:
    composed_replies = owl.compose_reply(
        content=content,
        quote_attribution=quote_attribution,
        quote_text=quote_text,
        quote_html=quote_html,
        make_text=make_text,
        make_html=make_html,
    )
    assert composed_replies == (
        (expected_text if make_text else None),
        (expected_html if make_html else None),
    )


@pytest.mark.parametrize(
    ["html", "text"],
    [
        ("", "\n"),
        (
            "<b>test here</b> with some <small>small</small> text",
            "**test here** with some small text\n",
        ),
        (
            '<a href="https://example.com/">Click <b>here</b></a> '
            "to see an example",
            "Click here (https://example.com/) to see an example\n",
        ),
    ],
    ids=["empty", "basic_formatting", "hyperlink"],
)
def test_html_to_text(owl: ReplyOwl, html: str, text: str) -> None:
    assert owl.html_to_text(html) == text
