# replyowl

Email reply body generator for HTML and text in Python

[![License](https://img.shields.io/github/license/smkent/replyowl)](https://github.com/smkent/replyowl/blob/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/replyowl)](https://pypi.org/project/replyowl/)
[![Python](https://img.shields.io/pypi/pyversions/replyowl)](https://pypi.org/project/replyowl/)
[![CI](https://github.com/smkent/replyowl/actions/workflows/ci.yaml/badge.svg)](https://github.com/smkent/replyowl/actions/workflows/ci.yaml)
[![Coverage](https://codecov.io/gh/smkent/replyowl/branch/main/graph/badge.svg)](https://codecov.io/gh/smkent/replyowl)
[![Renovate](https://img.shields.io/badge/renovate-enabled-brightgreen?logo=renovatebot)](https://renovatebot.com)
[![GitHub stars](https://img.shields.io/github/stars/smkent/replyowl?style=social)](https://github.com/smkent/replyowl)

[![replyowl][logo]](#)

replyowl creates email bodies with quoted messages. Provide the original message
and your reply message, and replyowl will combine them into a new message. The
returned content can be used as the text and/or HTML body content of a new
email. HTML-to-text conversion is performed with [html2text][html2text].

## Installation

```sh
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

## Project template

This project is generated and maintained with [copier-python][copier-python].

[copier-python]: https://smkent.github.io/copier-python
[html2text]: https://github.com/Alir3z4/html2text
[logo]: https://raw.github.com/smkent/replyowl/main/img/replyowl.png
