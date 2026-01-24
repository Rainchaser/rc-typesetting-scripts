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
A script to clean up HTML files downloaded from AO3, primarily for use with Scribus.
"""
import logging
import os
import sys
from datetime import datetime

import file_utils
import html_utils


def main():
    logger.debug(file_utils.format_message("start main", ("file to process is " + html_filename)))
    html_root = html_utils.get_parsed_root(html_filename)

    # remove meta title and style
    html_utils.remove_meta(html_root)

    # remove html links
    html_utils.remove_links(html_root)

    # change bold and italics to consistent tag
    html_utils.clean_style_tags(html_root)

    # convert ellipse to proper character
    html_utils.convert_ellipse(html_root)

    #TODO: implement style switch
    # convert dash to proper character
    html_utils.convert_dash(html_root, 'UK')

    # tags
    tags_root = html_utils.new_html_base("tags")
    html_utils.move_tags(html_root, tags_root)

    # notes
    notes_root = html_utils.new_html_base("notes")
    html_utils.move_notes(html_root, notes_root)

    #TODO: Clean up spaces (duplicate spaces, nbsp?, extra spaces around punctuation)

    #TODO: format headers
    # check for existing headers - h3 - h6 ?

    #TODO: double-spacing

    #TODO: scene breaks, mini breaks, <br/> (have these been used as scene breaks?)
    # convert multiple empty paragraphs to mini break
    # replace ornamented breaks with new ornament
    # convert first paragraph after each scene break to h4 ?

    #TODO check for one or two character italics and log to review doc

    # tag file: convert tree to string and write to output file
    file_utils.write_to_bfile(tags_file, html_utils.get_html_string(tags_root))
    # notes file: convert tree to string and write to output file
    file_utils.write_to_bfile(notes_file, html_utils.get_html_string(notes_root))

    # main body: convert tree to string and write to output file
    file_utils.write_to_bfile(work_file, html_utils.get_html_string(html_root))

if __name__ == '__main__':
    #TODO: getopts for options. Make timestamp configurable for anthologies.

    # get any passed arguments
    if len(sys.argv) > 2:
        html_filename = sys.argv[1]
        output_dir = sys.argv[2]
    else:
        print("usage: python clean_ao3_html.py <html_filename> <output_directory>")
        sys.exit(1)

    # set up the output folder and log file
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    logger = logging.getLogger(__name__)
    file_utils.set_log_config(os.path.join(output_dir, timestamp + ".log"))

    # configure the output file names
    folder = os.path.join(output_dir, timestamp)
    if not os.path.exists(folder):
        os.makedirs(folder)
    # set up the report file for any items that need to be checked
    report_filename = os.path.join(folder, timestamp + "_report.txt")
    # set up filenames for the modified work, the tags, and any author / chapter notes
    work_file, tags_file, notes_file = file_utils.setup_output(folder, html_filename)

    # process the file
    main()





