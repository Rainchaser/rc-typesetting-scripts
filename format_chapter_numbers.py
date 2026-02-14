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

from utils import file_utils, html_utils
from utils.string_utils import apply_case

logger = logging.getLogger(__name__)

# short code: (long code, type, default, description)
OPTIONS_DICT = {
    '-n' : ('--numbers', 'str', 'text', 'Number style - "roman" (e.g. "IV"), "arabic" (e.g. "32"), '
                                        '"text" (e.g. "fourteen". Optional, defaults to text'),
    '-p' : ('--prefix', 'str', '',
            'String to add before numbers, e.g. "Chapter", "Chap", "Ch". Optional, defaults to none.'),
    '-s' : ('--suffix', 'str', '', 'String to add after numbers, e.g. ":". Optional, defaults to none unless text '
                                   'format is combined then it defaults to ":". Cannot set empty if combined selected'),
    '-o' : ('--offset', 'int', '0', 'Set positive to skip numbering the initial chapters - e.g. set to 1 to skip '
                                    'prologue. Set negative to start numbering from a higher value, e.g. set to -4 to '
                                    'number first chapter as 5. Optional, defaults to 0.'),
    '-c' : ('--case', 'str', 'title', 'Case to use - upper, lower or title (first letters capitalised). Roman numerals '
                                      'will be uppercase if titlecase is selected. Optional, defaults to title'),
    '-a' : ('--after', 'str', '', 'Ornament to use after the chapter/title. Optional, defaults to none.'),
    '-b' : ('--between', 'str', '', 'Ornament to use between the chapter and title. Ignored if text format not split.'
                                    'Optional, defaults to none.'),
    '-t' : ('--text', 'str', 'split', 'text format - one of "chapter" (just the numbering), "title" (just the title), '
                                  '"combined" (chapter then title on same line), "split" (title on separate line '
                                  'beneath chapter). Optional, defaults to split.')
}


def main(options, work_file):
    logger.debug(file_utils.format_message("start main", ("file to process is " + options['filename'])))
    html_root = html_utils.get_parsed_root(options['filename'])

    # set prefix and suffix
    if options['prefix'] is not None and options['prefix'] != '':
        prefix = apply_case(options['prefix'], options['case'])
        prefix = str.strip(prefix) + " "
        use_prefix = True
    else:
        use_prefix = False

    if options['suffix'] is not None and options['suffix'] != '':
        suffix = apply_case(options['suffix'], options['case'])
        suffix = str.strip(suffix) + " "
        use_suffix = True
    elif options['text'] == 'combined':
            use_suffix = True
            suffix = ": "
    else:
            use_suffix = False
            suffix = ""

    # configure starting chapter info
    first_chap_num = 1
    chapters_skip = 0

    if options['offset'] > 0:
        chapters_skip = options['offset']
    elif options['offset'] < 0:
        # convert offset to positive and add to starting number
        first_chap_num = first_chap_num + abs(options['offset'])


    # find the chapter (1st h2 in div id=chapters)
    chapter_tags = html_utils.get_chapter_tags(html_root)

    if len(chapter_tags) > 0:
        element = html_utils.new_html_element(Tag.H2.value)
        element.text = headings[0].text
        text_div.addprevious(element)
    notes_root.append(group)

    # if next tag is also h2, already have a split chapter / title
    # if it is h1, it is an in-between ornament
    # if it is h6, it is an after ornament

    # create initial h2:
    # if using prefix, add prefix
    # if using numbering, add number (set num style) and convert case
    # if using suffix, add suffix

    # get title:
    # check if next tag is 2nd h2 - if yes, use value
    # if no, extract from 1st h2 - remove "text-whitespace-text/num-whitespace" from start of string
    # if combined, add title to 1st h2 value
    # if split, add title to a 2nd h2 value:

    # if split and in-between, set up h1 value

    # if using after, set up h6 value

    # replace 1st h2 with h2 text
    # check next line -
    # if h1 and not using h1, drop tag/tree
    # if not h1 and using h1, insert h1
    # if it is h1 and using h1, replace text
    # if h2 and not using h2, drop tag/tree
    # if not h2 and using h2, insert h2
    # if it is h2 and using h2, replace text
    # if h6 and not using h6, drop tag/tree
    # if not h6 and using h6, insert h6
    # if it is h6 and using h6, replace text



    # main body: convert tree to string and write to output file
    file_utils.write_to_bfile(work_file, html_utils.get_html_string(html_root))


    if __name__ == '__main__':
        arg_parser = file_utils.get_arg_parser(OPTIONS_DICT)
        arg_parser.add_argument('output_dir', help='Folder to save output files.')
        arg_parser.add_argument('filename', help='Filepath for the file to be processed. Required.')
        options = vars(arg_parser.parse_args())

        folder = file_utils.setup_config(options['output_dir'])

        # only need the first filename
        work_filename = file_utils.get_file_name(folder, options['filename'])

        # process the file - pass arguments to main so it can be called from anthology script
        main(options, work_filename)