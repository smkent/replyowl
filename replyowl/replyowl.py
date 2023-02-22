from typing import Any, Optional, Tuple

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
BS_PARSER = "html.parser"
HTML_TEMPLATE = (
    "<!DOCTYPE html><html><head><title></title></head><body>{html}</body>"
)


class ReplyOwl:
    def __init__(
        self,
        blockquote_style: str = BLOCKQUOTE_STYLE,
        bs_parser: str = BS_PARSER,
        html_template: str = HTML_TEMPLATE,
        h2t: Optional[html2text.HTML2Text] = None,
        linesep: str = "\n",
    ) -> None:
        self.blockquote_style = blockquote_style
        self.bs_parser = bs_parser
        self.html2text = h2t or self._init_html2text()
        self.html_template = html_template
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
        if not make_text and not make_html:
            return (None, None)
        if quote_text and not quote_html:
            quote_html = quote_text.replace(self.linesep, "<br />")
        if quote_html and not quote_text:
            quote_text = self.html_to_text(quote_html)
        return (
            (
                self._make_text_reply(content, quote_text, quote_attribution)
                if make_text
                else None
            ),
            (
                self._make_html_reply(content, quote_html, quote_attribution)
                if make_html
                else None
            ),
        )

    def html_to_text(self, html: str) -> str:
        soup = BeautifulSoup(html, self.bs_parser)
        # Replace links
        for a_tag in soup.find_all("a", href=True):
            link_text = a_tag.text
            link_target = a_tag["href"]
            link_str = f"{link_text} ({link_target})"
            if link_text.strip() == link_target:
                link_str = link_text
            a_tag.replace_with(link_str)
        text = self.html2text.handle(str(soup))
        text = text.replace(r"\-", "-")
        return text

    def _init_html2text(self) -> html2text.HTML2Text:
        h2t = html2text.HTML2Text()
        h2t.ul_item_mark = "-"
        h2t.body_width = 0
        return h2t

    def _init_html(self, quote_html: str) -> Any:
        soup = BeautifulSoup(quote_html, self.bs_parser)
        if soup.body:
            return soup
        return BeautifulSoup(
            self.html_template.replace("{html}", quote_html),
            self.bs_parser,
        )

    def _make_html_reply(
        self,
        content: str,
        quote_html: Optional[str],
        quote_attribution: Optional[str],
    ) -> str:
        if not quote_html:
            return str(
                BeautifulSoup(
                    self.html_template.replace("{html}", content),
                    self.bs_parser,
                )
            )
        soup = self._init_html(quote_html)
        tmpl = BeautifulSoup(content, self.bs_parser)
        bq = soup.new_tag(
            "blockquote", type="cite", style=self.blockquote_style
        )
        soup.body.wrap(bq).wrap(soup.new_tag("body", **soup.body.attrs))
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
        text = self.html_to_text(content)
        if quote_text:
            text += (
                self.linesep
                + "----"
                + self.linesep * 2
                + (quote_attribution or "")
                + self.linesep * 2
                + self.linesep.join(
                    [f"> {t}" for t in (quote_text or "").split(self.linesep)]
                )
            )
        return text.replace(self.linesep * 3, self.linesep * 2)
