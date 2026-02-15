#  Copyright (c) 2026 Ellen H. (https://github.com/Rainchaser)
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, <see https://www.gnu.org/licenses/>.

import logging

from lxml import html
from lxml.html import HtmlElement
from lxml.html.builder import HTML, HEAD, BODY, TITLE, H1

from utils import file_utils, Punctuation, XpathPart, Tag, Attr
from utils.string_utils import text_replace

logger = logging.getLogger(__name__)


def get_parsed_root(html_file):
    """
    Parse the provided HTML file and return the root element.
    :param html_file: path to the HTML file to parse
    :return: root element
    """
    parsed_html = html.parse(html_file)
    logger.debug(file_utils.format_message("parse html", "file parsed successfully"))
    return parsed_html.getroot()

def get_html_string(html_tree):
    """
    Convert HTML tree to utf-8 formatted string.
    :param html_tree: the parsed HTML tree
    :return: binary string in utf-8 format
    """
    html_string = html.tostring(html_tree, method="html", encoding="utf-8")
    logger.debug(file_utils.format_message("convert html to string", "file serialised"))
    return html_string

def new_html_base(content_type):
    return HTML(
        HEAD( TITLE(content_type)),
        BODY(
            H1(content_type)
        ),
    )

def new_html_element(tag):
    element = HtmlElement()
    element.tag = tag
    return element

def drop_all_of_tag(html_element: html.HtmlElement, tag_string):
    html_tags = html_element.findall(tag_string)
    for item in html_tags:
        item.drop_tag()

def del_tag_tree(html_element: html.HtmlElement, tag_string):
    tag = html_element.find(tag_string)
    if tag is not None:
        tag.drop_tree()

def update_tag_type(html_element: html.HtmlElement, search_str, tag_type):
    tags = html_element.findall(search_str)
    for tag in tags:
        tag.tag = tag_type

def convert_punctuation(html_element: html.HtmlElement, punct: Punctuation):
    new_text = punct.get_canonical_value()
    old_text = punct.get_aliases()

    for element in html_element.iter():
        text = element.text
        for alias in old_text:
            text = text_replace(text, alias, new_text)
        element.text = text

def get_chapter_titles(html_root: HtmlElement):
    return html_root.xpath(make_xpath([XpathPart.ALL_FROM_ROOT,
                                       Tag.DIV + XpathPart.item_with_val(XpathPart.CLASS.name, Attr.CHAPTERS),
                                       Tag.H2]))

def make_xpath(arg_list):
    return XpathPart.PATH_SEPARATOR.join(arg_list)