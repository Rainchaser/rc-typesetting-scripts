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

"""A script to clean up HTML files downloaded from AO3, primarily for use with Scribus."""
import logging
import os
import sys
from datetime import datetime
from lxml import html

import file_utils
import html_utils


"""Main function: process the specified file and clean it up"""
def main():
    logger.debug(file_utils.format_message("start main", ("file to process is '%s'", html_filename)))
    html_root = html_utils.get_parsed_root(html_filename)

    # tag file: convert tree to string and write to output file

    # notes file: convert tree to string and write to output file

    # main body: convert tree to string and write to output file
    file_utils.write_to_html(work_file, html_utils.get_html_string(html_root))

if __name__ == '__main__':
    # get any passed arguments
    if len(sys.argv) > 2:
        html_filename = sys.argv[1]
        output_dir = sys.argv[2]
    else:
        print("usage: python clean_ao3_html.py <html_filename> <output_directory>")
        sys.exit(1)

    # set up the logging and report files
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    logger = logging.getLogger(__name__)
    file_utils.set_log_config(os.path.join(".", timestamp + ".log"))
    report_filename = timestamp + "_report.txt"

    # configure the output file names
    folder = os.path.join(output_dir, timestamp)
    if not os.path.exists(folder):
        os.makedirs(folder)
    # set up filenames for the modified work, the tags, and any author / chapter notes
    work_file, tags_file, notes_file = file_utils.setup_output(folder, html_filename)

    # process the file
    main()



# remove all tabs, newlines and duplicate spaces - not needed?

# sometimes our scene break is surrounded by <span></span>. We need to axe those so we can get rid of the sdans, which otherwise mess up our italic spacing correction - also not needed?

# remove nbsp - not needed with html parsing?

# remove blank characters from between end of paragraph and start of next - need to see if this messes up html parsing not doing it


# clean up spaces
    # clean up extra spaces around tags - think the current code is weird about this?
    # clean up spaces between tags and following punctuation
    # clean up extra spaces around paragraphs (i.e </p> <p> - covered by previous comment?


# check for existing headers - h3 - h6 ?


# remove chapter notes

# remove tags (remove links)

# handle top matter? (save to restore later)

# remove  links

# convert dashes (convert all dashes including hyphens?)

# convert ... and . . . to an ellipse

# handle <br> - have these been used as scene breaks?

# clean up double-spacing

# convert multiple empty paragraphs to mini break

# replace ornamented breaks with new ornament
    # handle if they've doublespaced before/after ornament (will have minibreak+newbreak or newbreak+minibreak)

# convert first paragraph after each scene break to h4 ?

# restore line breaks (not needed?)

# check for one or two character italics and log to review doc

# write to new doc and save / end script






