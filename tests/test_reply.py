from typing import Iterable
from unittest import mock

import pytest

from replyowl import reply
from replyowl.reply import compose_reply

from .reply_cases import ReplyCases

TEST_REPLY_TEMPLATE = """
The year is 199X. A meteorite has fallen in
<b><a href="https://earthbound.fandom.com/wiki/Onett">Onett</a></b>.<br />
<br />
Watch out for:<br />
<ul>
<li>Coil Snake</li>
<li>Runaway Dog</li>
<li>Spiteful Crow</li>
</ul>
""".strip()


@pytest.fixture
def reply_mock() -> Iterable[mock.MagicMock]:
    with mock.patch.object(reply, "get_reply_template") as reply_template_mock:
        yield reply_template_mock


@pytest.mark.parametrize(**ReplyCases.compose_reply().__dict__)
def test_compose_reply(
    reply_mock: mock.MagicMock,
    reply_template: str,
    received_html: str,
    received_text: str,
    expected_html: str,
    expected_text: str,
    reply_attribution: str,
) -> None:
    reply_mock.return_value = reply_template
    text, html = compose_reply(received_html, received_text, reply_attribution)
    assert text == expected_text
    assert html == expected_html
