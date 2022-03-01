from dataclasses import dataclass
from typing import Any, Iterable, List, Optional


@dataclass
class ParametrizeParams:
    argnames: Iterable[str]
    argvalues: Iterable[Any]
    ids: Iterable[str]


@dataclass
class ReplyCase:
    id: str
    argvalues: Iterable[str]


@dataclass
class ReplyCaseParams:
    id: str
    content: str
    quote_html: Optional[str]
    quote_text: Optional[str]
    expected_html: str
    expected_text: str
    quote_attribution: Optional[str]


class ReplyCases:
    HTML_QUOTE_WITHOUT_BODY_TAG = ReplyCaseParams(
        id="html_quote_without_body_tag",
        content=(
            "The year is 199X. A meteorite has fallen in\n"
            '<b><a href="https://earthbound.fandom.com/wiki/Onett">'
            "Onett</a></b>.<br />\n"
            "<br />\n"
            "Watch out for:<br />\n"
            "<ul>\n"
            "<li>Coil Snake</li>\n"
            "<li>Runaway Dog</li>\n"
            "<li>Spiteful Crow</li>\n"
            "</ul>"
        ),
        quote_html=(
            "<div><b>Pictures taken instantaneously!</b><br /></div>"
            "I'm a photographic <i>genius</i>, "
            "if I do say so myself!<br /></div>"
            "<div>Okay, get ready for an instant memory!<br /></div>"
            "<div>Look at the camera... Ready... "
            'Say, "fuzzy pickles."<br /></div>'
        ),
        quote_text=(
            "Pictures taken instantaneously!\n\n"
            "I'm a photographic genius, if I do say so myself!\n\n"
            "Okay, get ready for an instant memory!\n\n"
            'Look at the camera... Ready... Say, "fuzzy pickles."'
        ),
        expected_html=(
            "<!DOCTYPE html>\n\n<html><head><title></title></head><body>"
            "The year is 199X. A meteorite has fallen in\n"
            '<b><a href="https://earthbound.fandom.com/wiki/Onett">'
            "Onett</a></b>.<br/>\n<br/>\nWatch out for:<br/>\n<ul>\n"
            "<li>Coil Snake</li>\n<li>Runaway Dog</li>\n"
            "<li>Spiteful Crow</li>\n</ul>"
            "<div>At some point, the camera man appeared and said:<br/>"
            '</div><blockquote style="margin-left: 0.8ex; '
            "padding-left: 2ex; border-left: 2px solid #aaa; "
            'border-radius: 8px;" type="cite">'
            "<div><b>Pictures taken instantaneously!</b><br/></div>"
            "I'm a photographic <i>genius</i>, if I do say so myself!<br/>"
            "<div>Okay, get ready for an instant memory!<br/></div>"
            '<div>Look at the camera... Ready... Say, "fuzzy pickles."'
            "<br/></div></blockquote></body></html>"
        ),
        expected_text=(
            "The year is 199X. A meteorite has fallen in "
            "**Onett (https://earthbound.fandom.com/wiki/Onett)**.  "
            "\n  \nWatch out for:  \n\n"
            "  - Coil Snake\n  - Runaway Dog\n  - Spiteful Crow\n\n\n"
            "----\n\nAt some point, the camera man appeared and said:\n\n"
            "> Pictures taken instantaneously!\n> \n"
            "> I'm a photographic genius, if I do say so myself!\n> \n"
            "> Okay, get ready for an instant memory!\n> \n"
            '> Look at the camera... Ready... Say, "fuzzy pickles."'
        ),
        quote_attribution=("At some point, the camera man appeared and said:"),
    )

    HTML_QUOTE_WITH_BODY_TAG_ONLY = ReplyCaseParams(
        id="html_quote_with_body_tag_only",
        content=(
            "ReplyOwl here with the following message:<br /><br />"
            "Bacon ipsum dolor amet cupim occaecat ullamco "
            "beef pork loin ham hock pastrami irure "
            "in excepteur shankle adipisicing corned beef"
        ),
        quote_html=(
            "Come work for us. "
            "The compensation is in the <b>real world</b>."
        ),
        quote_text=(""),
        expected_html=(
            "<!DOCTYPE html>\n\n"
            "<html><head><title></title></head><body>"
            "ReplyOwl here with the following message:<br/><br/>"
            "Bacon ipsum dolor amet cupim occaecat ullamco "
            "beef pork loin ham hock pastrami irure "
            "in excepteur shankle adipisicing corned beef"
            "<div>Four score and a few fortnights ago, someone opined:"
            '<br/></div><blockquote style="'
            "margin-left: 0.8ex; padding-left: 2ex; border-left: 2px "
            'solid #aaa; border-radius: 8px;" type="cite">'
            "Come work for us. "
            "The compensation is in the <b>real world</b>."
            "</blockquote></body></html>"
        ),
        expected_text=(
            "ReplyOwl here with the following message:  \n  \n"
            "Bacon ipsum dolor amet cupim occaecat ullamco "
            "beef pork loin ham hock pastrami irure "
            "in excepteur shankle adipisicing corned beef\n\n"
            "----\n\n"
            "Four score and a few fortnights ago, someone opined:\n\n"
            "> Come work for us. The compensation is in the **real world**.\n"
            "> "
        ),
        quote_attribution=(
            "Four score and a few fortnights ago, someone opined:"
        ),
    )

    HTML_QUOTE_ONLY = ReplyCaseParams(
        id="html_quote_only",
        content=("Your original message only had <b>HTML</b>."),
        quote_html=(
            '<a href="https://baconipsum.com"><b>Bacon</b> ipsum</a> '
            "dolor amet ex <i>spare ribs</i> duis aute."
        ),
        quote_text=None,
        expected_html=(
            "<!DOCTYPE html>\n\n<html><head><title></title></head><body>"
            "Your original message only had <b>HTML</b>."
            "<div>At midnight, the narwhal baconed:<br/>"
            '</div><blockquote style="margin-left: 0.8ex; padding-left: 2ex; '
            'border-left: 2px solid #aaa; border-radius: 8px;" '
            'type="cite"><a href="https://baconipsum.com">'
            "<b>Bacon</b> ipsum</a> dolor amet ex <i>spare ribs</i> "
            "duis aute.</blockquote></body></html>"
        ),
        expected_text=(
            "Your original message only had **HTML**.\n\n----\n\n"
            "At midnight, the narwhal baconed:\n\n"
            "> Bacon ipsum (https://baconipsum.com) "
            "dolor amet ex _spare ribs_ duis aute.\n> "
        ),
        quote_attribution=("At midnight, the narwhal baconed:"),
    )

    ALL_BLANK_INPUTS = ReplyCaseParams(
        id="all_blank_inputs",
        content="",
        quote_html="",
        quote_text="",
        expected_html=(
            "<!DOCTYPE html>\n\n"
            "<html><head><title></title></head><body></body></html>"
        ),
        expected_text="\n",
        quote_attribution="",
    )

    @classmethod
    def compose_reply(
        cls,
    ) -> ParametrizeParams:
        argnames = [
            "content",
            "quote_html",
            "quote_text",
            "expected_html",
            "expected_text",
            "quote_attribution",
        ]
        ids: List[str] = []
        argvalues: List[Any] = []
        for reply_case in [
            cls.HTML_QUOTE_WITHOUT_BODY_TAG,
            cls.HTML_QUOTE_WITH_BODY_TAG_ONLY,
            cls.HTML_QUOTE_ONLY,
            cls.ALL_BLANK_INPUTS,
        ]:
            ids.append(reply_case.id)
            argvalues.append(
                [
                    reply_case.content,
                    reply_case.quote_html,
                    reply_case.quote_text,
                    reply_case.expected_html,
                    reply_case.expected_text,
                    reply_case.quote_attribution,
                ]
            )
        return ParametrizeParams(
            argnames=argnames, argvalues=argvalues, ids=ids
        )
