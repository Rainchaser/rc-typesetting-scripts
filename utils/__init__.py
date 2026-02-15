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
"""
The utility modules for the typesetting scripts
"""

__all__ = ['file_utils', 'html_utils', 'number_utils', 'Tag', 'Punctuation', 'XpathPart', 'Attr', 'get_arg_parser']

import argparse
from enum import Enum, StrEnum

from utils.string_utils import text_replace


def get_arg_parser(opts_list: dict):
    parser = argparse.ArgumentParser()

    for opt in opts_list:
        parser.add_argument(opt, opts_list[opt][0], type=opts_list[opt][1],
                            default=opts_list[opt][2], help=opts_list[opt][3])

    return parser


'''
An enum class containing values for specific attribute-related values (mainly used by AO3).
'''
class Attr(StrEnum):
    # types of attribute
    ID = 'id'
    CLASS = 'class'
    # attribute values
    CHAPTERS = 'chapters'
    META = 'meta'
    META_GRP = 'meta group'
    BYLINE = 'byline'
    PREFACE = 'preface'
    AFTERWORD = 'afterword'
    TAGS = 'tags'
    MESSAGE = 'message'
    HEADING = 'heading'
    TOC_HEADING = 'toc-heading'


'''
An enum class containing values for specific html tags, plus a method to retrieve the string to use with find or
findall to retrieve any occurrence of that tag.
'''
class Tag(StrEnum):
    DROP = 'drop' # set by script to id items to delete
    ANY = '*'
    HTML = 'html'
    BODY = 'body'
    HEAD = 'head'
    TITLE = 'title'
    STYLE = 'style'
    ANCHOR = 'a'
    DIV = 'div'
    SPAN = 'span'
    PARAGRAPH = 'p'
    BOLD = 'b'
    ITALIC = 'i'
    EMPHASIS = 'em'
    STRONG = 'strong'
    DL = 'dl'
    H1 = 'h1'
    H2 = 'h2'
    H3 = 'h3'
    H4 = 'h4'
    H5 = 'h5'
    H6 = 'h6'
    AO3_WORK_TITLE = 'h1' # alias for actual header value. Edit here if using a different header level
    AO3_CHAP_TITLE = 'h2' # alias for actual header value. Edit here if using a different header level

    def get_find_str(self):
        return './/' + self.value # string to use with 'find' or 'findall'


'''
An enum class containing values for specific html tags, plus a method to retrieve the string to use with find or
findall to retrieve any occurrence of that tag.
'''
class XpathPart(StrEnum):
    ALL_REL_TO_NODE = './' # only one / as join will add an extra one
    ALL_FROM_ROOT = '/' # only one / as join will add an extra one
    SINGLE_PATH_FROM_ROOT = '' # no / as join will add an extra one
    SINGLE_REL_PATH = '.' # no / as join will add an extra one
    PATH_SEPARATOR = '/'
    GROUP_SEPARATOR = '|'
    ID = '[@id]'
    CLASS = '[@class]'
    ANY = '[@*]'

    @classmethod
    def item_with_val(cls, item_val, attr_val):
        if item_val not in ['ID', 'CLASS', 'ANY']:
            item_val = 'ANY'
        return text_replace(cls[item_val].value, ']', '="' + attr_val + '"]')


'''
An enum class containing pre-set preferred values for specific punctuation types, 
plus aliases that may have been used instead.
'''
class Punctuation(Enum):
    # first value is the correct version. Subsequent values are potential variants that need updating
    ELLIPSIS = ['…', '. . .', '...']
    UK_DASH = [' – ', ' — ', '—', ' - ']
    US_DASH = ['—', ' – ', '–', ' - ']
    NONE = ['']

    def get_canonical_value(self):
        return self.value[0] # intended value

    def get_aliases(self):
        # use a copy so the actual enum value isn't affected
        temp = self.value.copy()
        del temp[0] # drop the intended value and return the aliases
        return temp

    @classmethod
    def get_dash_style(cls, style_string):
        if style_string == 'UK':
            return cls.UK_DASH
        elif style_string == 'US':
            return cls.US_DASH
        else:
            return Punctuation.NONE