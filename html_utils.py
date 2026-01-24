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

from lxml.html import HtmlElement
from lxml.html.builder import HTML, HEAD, BODY, TITLE, H1, STRONG, EM

import file_utils

from lxml import html, etree

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


def remove_links(html_element: html.HtmlElement):
    html_tags = html_element.findall('.//a')
    for item in html_tags:
        item.drop_tag()


def remove_meta(html_element: html.HtmlElement):
    del_tag_tree(html_element, './head/title')
    del_tag_tree(html_element, './head/style')


def del_tag_tree(html_element: html.HtmlElement, string_tag):
    tag = html_element.find(string_tag)
    if tag is not None:
        tag.drop_tree()


def clean_style_tags(html_element: html.HtmlElement):
    update_tag_type(html_element, './/b', 'strong')
    update_tag_type(html_element, './/i', 'em')


def update_tag_type(html_element: html.HtmlElement, search_str, tag_type):
    tags = html_element.findall(search_str)
    for tag in tags:
        tag.tag = tag_type


def convert_ellipse(html_element: html.HtmlElement):
    for element in html_element.iter():
        text = element.text
        text = text_replace(text, '...', '…')
        text = text_replace(text, '. . .', '…')
        element.text = text


def convert_dash(html_element: html.HtmlElement, style_type):
    if style_type == 'UK':
        new_text = ' – '
        old_text = [' — ','—', ' - ']
    elif style_type == 'US':
        new_text = '—'
        old_text = [' – ','–', ' - ']
    else:
        new_text = ''
        old_text = []


    for element in html_element.iter():
        text = element.text
        for style in old_text:
            text = text_replace(text, style, new_text)
        element.text = text


def text_replace(text, old_text, new_text):
    if text is not None:
        text = text.replace('old_text', new_text)
    return text


def move_tags(html_root: HtmlElement, tags_root:HtmlElement):
    # add the initial message of "originally posted on.."
    element = HtmlElement()
    element.set('tag','div')
    element.append(html_root.xpath('//p[@class="message"]')[0])
    tags_root.append(element)

    # Add the list of tags
    tags = html_root.xpath('//dl[@class="tags"]')
    tags_root.append(tags[0])


def move_notes(html_root, notes_root):
    # move title/author in root
    pre_div = html_root.xpath('//div[@id="preface"]')[0]
    pre_div.find('.//h2').drop_tree()
    pre_div.append(pre_div.xpath('//div[@class="meta"]/h1')[0])
    pre_div.append(pre_div.xpath('//div[@class="meta"]/div[@class="byline"]')[0])

    # move summary and work notes
    notes_root.append(pre_div.xpath('//div[@class="meta"]')[0])

    # move chapter start / end notes
    meta_groups = html_root.xpath('//div[@id="chapters"]/div[@class="meta group"]|//div[@id="chapters"]/div[@class="meta"]')
    for group in meta_groups:
        if group.get('class') == 'meta group':
            text_div = group.getnext()
            headings = group.xpath('//h2[@class="heading"]')
            if len(headings) > 0:
                element = HtmlElement()
                element.tag = 'h2'
                element.text = headings[0].text
                text_div.addprevious(element)
            notes_root.append(group)
        else:
            notes_root.append(group)

    # move afterword
    afterword = html_root.xpath('//div[@id="afterword"]')
    for note in afterword:
        notes_root.append(note)
