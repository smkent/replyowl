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
        linesep: str = "\n",
    ) -> None:
        self.blockquote_style = blockquote_style or self.BLOCKQUOTE_STYLE
        self.bs_parser = bs_parser or self.BS_PARSER
        self.html2text = h2t or self._init_html2text()
        self.html_template = html_template or self.HTML_TEMPLATE
        self.linesep = linesep

    def compose_reply(
        self,
        content: str,
        quote_attribution: Optional[str],
        quote_text: Optional[str],
        quote_html: Optional[str],
        make_text: bool = True,
        make_html: bool = True,
    ) -> Tuple[Optional[str], Optional[str]]:
        if quote_text and not quote_html:
            quote_html = quote_text.replace(self.linesep, "<br />")
        if quote_html and not quote_text:
            quote_text = self._convert_html_to_text(quote_html)
        html: Optional[str] = None
        text: Optional[str] = None
        if make_html:
            html = self._make_html_reply(
                content, quote_html, quote_attribution
            )
        if make_text:
            text = self._make_text_reply(
                content, quote_text, quote_attribution
            )
        return text, html

    def _init_html2text(self) -> html2text.HTML2Text:
        h2t = html2text.HTML2Text()
        h2t.ul_item_mark = "-"
        h2t.body_width = 0
        return h2t

    def _convert_html_to_text(self, html: str) -> str:
        soup = BeautifulSoup(html, self.bs_parser)
        # Replace links
        for ahref in soup.find_all("a", href=True):
            linkstr = f"{ahref.string} ({ahref['href']})"
            ahref.replace_with(linkstr)
        text = self.html2text.handle(str(soup))
        text = text.replace(r"\-", "-")
        return text

    def _init_html(self, quote_html: Optional[str]) -> Any:
        if quote_html:
            soup = BeautifulSoup(quote_html, self.bs_parser)
            if soup.body:
                return soup
        return BeautifulSoup(
            self.html_template.replace("{html}", quote_html or ""),
            self.bs_parser,
        )

    def _make_html_reply(
        self,
        content: str,
        quote_html: Optional[str],
        quote_attribution: Optional[str],
    ) -> str:
        soup = self._init_html(quote_html)
        tmpl = BeautifulSoup(content, self.bs_parser)
        bq = soup.new_tag(
            "blockquote", type="cite", style=self.blockquote_style
        )
        soup.body.wrap(bq).wrap(soup.new_tag("body"))
        soup.body.body.unwrap()
        new_div = soup.new_tag("div")
        new_div.string = quote_attribution or ""
        new_div.append(soup.new_tag("br"))
        bq.insert_before(new_div)
        new_div.insert_before(tmpl)
        return str(soup)

    def _make_text_reply(
        self,
        content: str,
        quote_text: Optional[str],
        quote_attribution: Optional[str],
    ) -> str:
        text = (
            self._convert_html_to_text(content)
            + self.linesep
            + "----"
            + self.linesep * 2
            + (quote_attribution or "")
            + self.linesep * 2
            + self.linesep.join(
                [f"> {t}" for t in (quote_text or str()).split(self.linesep)]
            )
        )
        return text.replace(self.linesep * 3, self.linesep * 2)
