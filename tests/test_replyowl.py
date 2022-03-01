import pytest

from replyowl import ReplyOwl

from .reply_cases import ReplyCases


@pytest.mark.parametrize(**ReplyCases.compose_reply().__dict__)
@pytest.mark.parametrize("make_html", (True, False), ids=["html", "no_html"])
@pytest.mark.parametrize("make_text", (True, False), ids=["text", "no_text"])
def test_compose_reply(
    content: str,
    quote_html: str,
    quote_text: str,
    expected_html: str,
    expected_text: str,
    quote_attribution: str,
    make_text: bool,
    make_html: bool,
) -> None:
    owl = ReplyOwl()
    text, html = owl.compose_reply(
        content=content,
        quote_attribution=quote_attribution,
        quote_text=quote_text,
        quote_html=quote_html,
        make_text=make_text,
        make_html=make_html,
    )
    assert html == (expected_html if make_html else None)
    assert text == (expected_text if make_text else None)
