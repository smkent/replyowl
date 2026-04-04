import pytest

from replyowl import ReplyOwl


@pytest.fixture
def owl() -> ReplyOwl:
    return ReplyOwl()
