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
import file_utils

from lxml import html

logger = logging.getLogger(__name__)

def get_parsed_root(html_file):
    parsed_html = html.parse(html_file)
    logger.debug(file_utils.format_message("parse html", "file parsed successfully"))
    return parsed_html.getroot()

def get_html_string(html_tree, method="html"):
    html_string = html.tostring(html_tree, method=method, encoding="utf-8")
    logger.debug(file_utils.format_message("convert html to string", "file serialised"))
    return html_string
