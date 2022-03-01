import os
from typing import Any, Optional, Tuple

import html2text
from bs4 import BeautifulSoup  # type: ignore


class ReplyOwl:
    BLOCKQUOTE_STYLE = " ".join(
        [
            "margin-left: 0.8ex;",
            "padding-left: 2ex;",
            "border-left: 2px solid #aaa;",
            "border-radius: 8px;",
        ]
    )
    BS_PARSER = "html.parser"
    HTML_TEMPLATE = (
        "<!DOCTYPE html>\n"
        "<html><head><title></title></head><body>{html}</body>"
    )

    def __init__(
        self,
        blockquote_style: Optional[str] = None,
        bs_parser: Optional[str] = None,
        html_template: Optional[str] = None,
        h2t: Optional[html2text.HTML2Text] = None,
    ) -> None:
        self.blockquote_style = blockquote_style or self.BLOCKQUOTE_STYLE
        self.bs_parser = bs_parser or self.BS_PARSER
        self.html_template = html_template or self.HTML_TEMPLATE
        self.html2text = h2t or self.init_html2text()

    def init_html2text(self) -> html2text.HTML2Text:
        h2t = html2text.HTML2Text()
        h2t.ul_item_mark = "-"
        h2t.body_width = 0
        return h2t

    def init_html(self, quote_html: Optional[str]) -> Any:
        if quote_html:
            soup = BeautifulSoup(quote_html, self.bs_parser)
            if soup.body:
                return soup
            return BeautifulSoup(
                self.html_template.replace("{html}", quote_html),
                self.bs_parser,
            )
        return BeautifulSoup(
            self.html_template.replace("{html}", ""), self.bs_parser
        )

    def compose_reply(
        self,
        content: str,
        quote_attribution: Optional[str],
        quote_text: Optional[str],
        quote_html: Optional[str],
        make_text: bool = True,
        make_html: bool = True,
    ) -> Tuple[Optional[str], Optional[str]]:
        soup = self.init_html(quote_html)

        tmpl = BeautifulSoup(content, self.bs_parser)
        bq = soup.new_tag(
            "blockquote", type="cite", style=self.blockquote_style
        )
        soup.body.wrap(bq).wrap(soup.new_tag("body"))
        soup.body.body.unwrap()
        new_div = soup.new_tag("div")
        new_div.string = quote_attribution
        new_div.append(soup.new_tag("br"))
        bq.insert_before(new_div)
        new_div.insert_before(tmpl)

        rendert = self.make_text_reply(
            content, quote_html, quote_text, quote_attribution
        )
        print(soup)
        print(rendert)
        return rendert, str(soup)

    def make_text_reply(
        self,
        content: str,
        html: Optional[str],
        text: Optional[str],
        reply_attribution: Optional[str],
    ) -> str:
        if not html:
            return ""
        # Replace links
        at = BeautifulSoup(content, self.bs_parser)
        for ahref in at.find_all("a", href=True):
            linkstr = f"{ahref.string} ({ahref['href']})"
            ahref.replace_with(linkstr)

        rendert = self.html2text.handle(str(at))
        rendert = rendert.replace(r"\-", "-")
        rendert += (
            os.linesep
            + "----"
            + os.linesep * 2
            + (reply_attribution or "")
            + os.linesep * 2
            + os.linesep.join(
                [f"> {t}" for t in (text or str()).split(os.linesep)]
            )
        )
        rendert = rendert.replace(os.linesep * 3, os.linesep * 2)
        return rendert
