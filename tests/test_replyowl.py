import pytest

from replyowl import ReplyOwl

from .reply_cases import ReplyCases


@pytest.mark.parametrize(**ReplyCases.compose_reply().__dict__)
@pytest.mark.parametrize("make_html", (True, False), ids=["html", "no_html"])
@pytest.mark.parametrize("make_text", (True, False), ids=["text", "no_text"])
def test_compose_reply(
    reply_template: str,
    received_html: str,
    received_text: str,
    expected_html: str,
    expected_text: str,
    reply_attribution: str,
    make_text: bool,
    make_html: bool,
) -> None:
    owl = ReplyOwl()
    text, html = owl.compose_reply(
        content=reply_template,
        quote_attribution=reply_attribution,
        quote_text=received_text,
        quote_html=received_html,
        make_text=make_text,
        make_html=make_html,
    )
    assert html == (expected_html if make_html else None)
    assert text == (expected_text if make_text else None)
