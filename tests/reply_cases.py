from dataclasses import dataclass
from typing import Any, Iterable, List


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
    reply_template: str
    received_html: str
    received_text: str
    expected_html: str
    expected_text: str
    reply_attribution: str


class ReplyCases:
    NO_BODY_TAG = ReplyCaseParams(
        id="html_without_body_tag",
        reply_template=(
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
        received_html=(
            "<div><b>Pictures taken instantaneously!</b><br /></div>"
            "I'm a photographic <i>genius</i>, "
            "if I do say so myself!<br /></div>"
            "<div>Okay, get ready for an instant memory!<br /></div>"
            "<div>Look at the camera... Ready... "
            'Say, "fuzzy pickles."<br /></div>'
        ),
        received_text=(
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
        reply_attribution=("At some point, the camera man appeared and said:"),
    )

    BODY_TAG_ONLY = ReplyCaseParams(
        id="html_with_body_tag_only",
        reply_template=(
            "Waffles here with the following message:<br /><br />"
            "Bacon ipsum dolor amet cupim occaecat ullamco "
            "beef pork loin ham hock pastrami irure "
            "in excepteur shankle adipisicing corned beef"
        ),
        received_html=(
            "Come work for us. "
            "The compensation is in the <b>real world</b>."
        ),
        received_text=(""),
        expected_html=(
            "<!DOCTYPE html>\n\n"
            "<html><head><title></title></head><body>"
            "Waffles here with the following message:<br/><br/>"
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
            "Waffles here with the following message:  \n  \n"
            "Bacon ipsum dolor amet cupim occaecat ullamco "
            "beef pork loin ham hock pastrami irure "
            "in excepteur shankle adipisicing corned beef\n\n"
            "----\n\n"
            "Four score and a few fortnights ago, someone opined:\n\n"
            "> Come work for us. The compensation is in the **real world**.\n"
            "> "
        ),
        reply_attribution=(
            "Four score and a few fortnights ago, someone opined:"
        ),
    )

    BLANK_MESSAGE = ReplyCaseParams(
        id="empty_message",
        reply_template="",
        received_html="",
        received_text="",
        expected_html=(
            "<!DOCTYPE html>\n\n<html><head><title></title></head>"
            "<body><div><br/></div><blockquote "
            'style="margin-left: 0.8ex; padding-left: 2ex; '
            'border-left: 2px solid #aaa; border-radius: 8px;" '
            'type="cite"></blockquote></body></html>'
        ),
        expected_text="\n\n----\n\n\n> ",
        reply_attribution="",
    )

    @classmethod
    def compose_reply(
        cls,
    ) -> ParametrizeParams:
        argnames = [
            "reply_template",
            "received_html",
            "received_text",
            "expected_html",
            "expected_text",
            "reply_attribution",
        ]
        ids: List[str] = []
        argvalues: List[Any] = []
        for reply_case in [
            cls.NO_BODY_TAG,
            cls.BODY_TAG_ONLY,
            cls.BLANK_MESSAGE,
        ]:
            ids.append(reply_case.id)
            argvalues.append(
                [
                    reply_case.reply_template,
                    reply_case.received_html,
                    reply_case.received_text,
                    reply_case.expected_html,
                    reply_case.expected_text,
                    reply_case.reply_attribution,
                ]
            )
        return ParametrizeParams(
            argnames=argnames, argvalues=argvalues, ids=ids
        )
