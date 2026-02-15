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
import re

logger = logging.getLogger(__name__)


def apply_case(value, case):
    if case == 'title':
        value = value.title()
    elif case == 'upper':
        value = value.upper()
    elif case == 'lower':
        value = value.lower()
    return value

def text_replace(text, old_text, new_text):
    if text is not None:
        text = text.replace(old_text, new_text)
    return text

def get_title_from_chapter(input_str):
    """Extracts the title from a string, if present. Only implemented for strings in the format <chapter number>
     or <chapter number>[<space>]<suffix><space><title> (where the space after chapter number is optional)."""
    split_str = re.split('[^A-z0-9 ] ', input_str.strip())
    out_str = ''
    if len(split_str) > 2:
        remove_str = split_str[0]
        # need to also remove the original split character
        out_str = re.sub(f'{remove_str}[^A-z0-9 ] ', '', input_str)
    elif len(split_str) == 2:
        out_str = split_str[1]
    return str.strip(out_str)