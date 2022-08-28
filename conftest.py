from typing import Iterable

import pytest

from replyowl import ReplyOwl


@pytest.fixture
def owl() -> Iterable[ReplyOwl]:
    yield ReplyOwl()
