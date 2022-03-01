# replyowl: Email reply body generator for HTML and text in Python

[![PyPI](https://img.shields.io/pypi/v/replyowl)][pypi]
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/replyowl)][pypi]
[![Build](https://img.shields.io/github/checks-status/smkent/replyowl/master?label=build)][gh-actions]
[![codecov](https://codecov.io/gh/smkent/replyowl/branch/master/graph/badge.svg)][codecov]
[![GitHub stars](https://img.shields.io/github/stars/smkent/replyowl?style=social)][repo]

[![replyowl][logo]](#)

replyowl creates email bodies with quoted messages. Provide the original message
and your reply message, and replyowl will combine them into a new message. The
returned content can be used as the text and/or HTML body content of a new
email.

## Installation

[replyowl is available on PyPI][replyowl-pypi]:

```
pip install replyowl
```

## Usage

```py
from replyowl import ReplyOwl

owl = ReplyOwl()
text, html = owl.compose_reply(
    content="<i>New</i> reply <b>content</b>",
    quote_attribution="You wrote:",
    quote_text="Original message text",
    quote_html="<b>Original</b> message text",
)

print(text)
# _New_ reply **content**
#
# ----
#
# You wrote:
#
# > Original message text

print(html)  # (output formatted for readability)
# <!DOCTYPE html>
# <html>
#   <head>
#     <title></title>
#   </head>
#   <body>
#     <i>New</i> reply <b>content</b>
#     <div>You wrote:<br />
#     </div>
#     <blockquote style="margin-left: 0.8ex; padding-left: 2ex;
#                        border-left: 2px solid #aaa; border-radius: 8px;" type="cite">
#       <b>Original</b> message text
#     </blockquote>
#   </body>
# </html>
```

Links in HTML are preserved when creating plain text email bodies:
```py
from replyowl import ReplyOwl

owl = ReplyOwl()
text, html = owl.compose_reply(
    content=(
        'Check <a href="https://example.com/">this</a> out<br />'
        'Or this: <a href="https://example.net/">https://example.net/</a>'
    ),
    quote_attribution="You wrote:",
    quote_text="Send me a URL",
    quote_html="Send me a <i>URL</i>",
)

print(text)
# Check this (https://example.com/) out
# Or this: https://example.net/
#
# ----
#
# You wrote:
#
# > Send me a URL
```

If the quoted HTML content contains a `<body>` tag, that is preserved:
```py
from replyowl import ReplyOwl

owl = ReplyOwl()
text, html = owl.compose_reply(
    content="Hello there",
    quote_attribution="You wrote:",
    quote_text="Hi",
    quote_html='<html><body class="sender_body"><b>Hi</b></body></html>',
)

print(html)  # (output formatted for readability)
# <html>
#   <body class="sender_body">
#     Hello there
#     <div>
#     You wrote:<br/>
#     </div>
#     <blockquote style="margin-left: 0.8ex; padding-left: 2ex;
#                        border-left: 2px solid #aaa; border-radius: 8px;" type="cite">
#       <b>Hi</b>
#     </blockquote>
#   </body>
# </html>
```

A custom value can be provided for the `<blockquote>`'s `style` tag:
```py
from replyowl import ReplyOwl

owl = ReplyOwl(blockquote_style="font-weight: bold;")
text, html = owl.compose_reply(
    text, html = owl.compose_reply(
        content="Your quote is in bold",
        quote_attribution="You wrote:",
        quote_text="I'm going to be in bold when you reply",
        quote_html="I'm going to be in bold when you reply",
    )
)

print(html)  # (output formatted for readability)
# <html>
#   <body class="sender_body">
#     Your quote is in bold
#     <div>
#     You wrote:<br/>
#     </div>
#     <blockquote style="font-weight: bold;" type="cite"
#       I'm going to be in bold when you reply
#     </blockquote>
#   </body>
# </html>
```

## Development

Prerequisites: [Poetry][poetry]

* Setup: `poetry install`
* Run all tests: `poetry run poe test`
* Fix linting errors: `poetry run poe lint`

---

Created from [smkent/cookie-python][cookie-python] using
[cookiecutter][cookiecutter]

[codecov]: https://codecov.io/gh/smkent/replyowl
[cookie-python]: https://github.com/smkent/cookie-python
[cookiecutter]: https://github.com/cookiecutter/cookiecutter
[gh-actions]: https://github.com/smkent/replyowl/actions?query=branch%3Amaster
[logo]: https://raw.github.com/smkent/replyowl/master/img/replyowl.png
[poetry]: https://python-poetry.org/docs/#installation
[pypi]: https://pypi.org/project/replyowl/
[replyowl-pypi]: https://pypi.org/project/replyowl/
[repo]: https://github.com/smkent/replyowl
