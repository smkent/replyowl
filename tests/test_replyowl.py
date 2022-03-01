import pytest

from replyowl import ReplyOwl

from .reply_cases import ReplyCases


@pytest.mark.parametrize(**ReplyCases.compose_reply().__dict__)
def test_compose_reply(
    reply_template: str,
    received_html: str,
    received_text: str,
    expected_html: str,
    expected_text: str,
    reply_attribution: str,
) -> None:
    ro = ReplyOwl()
    text, html = ro.compose_reply(
        reply_template, reply_attribution, received_text, received_html
    )
    assert text == expected_text
    assert html == expected_html
