# replyowl: Email reply body generator for HTML and text in Python

[![replyowl][logo]](#)

replyowl creates email bodies with quoted messages. Provide the original message
and your reply message, and replyowl will combine them into a new message. The
returned content can be used as the text and/or HTML body content of a new
email.

replyowl is in initial development.

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


## Development

Prerequisites: [Poetry][poetry]

* Setup: `poetry install`
* Run all tests: `poetry run poe test`
* Fix linting errors: `poetry run poe lint`

---

Created from [smkent/cookie-python][cookie-python] using
[cookiecutter][cookiecutter]

[cookie-python]: https://github.com/smkent/cookie-python
[cookiecutter]: https://github.com/cookiecutter/cookiecutter
[logo]: https://raw.github.com/smkent/replyowl/master/img/replyowl.png
[poetry]: https://python-poetry.org/docs/#installation
[replyowl-pypi]: https://pypi.org/project/replyowl/
