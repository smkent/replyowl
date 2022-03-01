import os
from typing import Optional, Tuple

import html2text
from bs4 import BeautifulSoup  # type: ignore

BLOCKQUOTE_STYLE = " ".join(
    [
        "margin-left: 0.8ex;",
        "padding-left: 2ex;",
        "border-left: 2px solid #aaa;",
        "border-radius: 8px;",
    ]
)


def get_reply_template() -> str:
    return "<p>I'm a reply generated using replyowl!</p>"


def make_text_reply(
    html: Optional[str], text: Optional[str], reply_attribution: str
) -> str:
    if not html:
        return ""
    at = BeautifulSoup(get_reply_template(), "html.parser")
    for ahref in at.find_all("a", href=True):
        linkstr = f"{ahref.string} ({ahref['href']})"
        ahref.replace_with(linkstr)

    h2t = html2text.HTML2Text()
    h2t.ul_item_mark = "-"
    h2t.body_width = 0
    rendert = h2t.handle(str(at))
    rendert = rendert.replace(r"\-", "-")
    rendert += (
        os.linesep
        + "----"
        + os.linesep * 2
        + reply_attribution
        + os.linesep * 2
        + os.linesep.join(
            [f"> {t}" for t in (text or str()).split(os.linesep)]
        )
    )
    rendert = rendert.replace(os.linesep * 3, os.linesep * 2)
    return rendert


def compose_reply(
    html: Optional[str], text: Optional[str], reply_attribution: str
) -> Tuple[str, str]:
    if not html:
        html = text
    soup = BeautifulSoup(html, "html.parser")
    if not soup.body:
        soup = BeautifulSoup(
            f"<!DOCTYPE html>\n"
            f"<html><head><title></title></head><body>{html}</body>",
            "html.parser",
        )
    tmpl = BeautifulSoup(get_reply_template(), "html.parser")
    bq = soup.new_tag(
        "blockquote",
        type="cite",
        style=BLOCKQUOTE_STYLE,
    )
    soup.body.wrap(bq).wrap(soup.new_tag("body"))
    soup.body.body.unwrap()
    new_div = soup.new_tag("div")
    new_div.string = reply_attribution
    new_div.append(soup.new_tag("br"))
    bq.insert_before(new_div)
    new_div.insert_before(tmpl)
    rendert = make_text_reply(html, text, reply_attribution)
    print(soup)
    print(rendert)
    return rendert, str(soup)
