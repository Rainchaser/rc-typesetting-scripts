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
import sys

from utils import file_utils, html_utils, Tag, number_utils, get_arg_parser
from utils.string_utils import apply_case, get_title_from_chapter
from copy import deepcopy

logger = logging.getLogger(__name__)

# short code: (long code, type, default, description)
OPTIONS_DICT = {
    '-n' : ('--numbers', str, 'text', 'Number style - "roman" (e.g. "IV"), "arabic" (e.g. "32"), '
                                        '"text" (e.g. "fourteen". Optional, defaults to text'),
    '-p' : ('--prefix', str, '', 'String added before numbers, e.g. "Chap", "Ch". Some characters may need to be placed'
                                 ' in double quotes in order to be accepted e.g. "|" Optional, defaults to none.'),
    '-s' : ('--suffix', str, '', 'String to add after numbers - some characters may need to be placed in double quotes '
                                 'in order to be accepted e.g. "|". Optional, defaults to none unless text'
                                 ' format is combined then it defaults to ":". Cannot set empty if combined selected'),
    '-o' : ('--offset', int, '0', 'Set positive to skip numbering the initial chapters - e.g. set to 1 to skip '
                                    'prologue. Set negative to start numbering from a higher value, e.g. set to -4 to '
                                    'number first chapter as 5. Optional, defaults to 0.'),
    '-c' : ('--case', str, 'title', 'Case to use - upper, lower or title (first letters capitalised). Roman numerals '
                                      'will be uppercase unless lowercase is selected. If an empty value is passed,'
                                      '(e.g. -c "") then the case is left unaltered. Optional, defaults to title'),
    '-a' : ('--after', str, '', 'Ornament to use after the chapter/title, not affected by case. '
                                  'Optional, defaults to none.'),
    '-b' : ('--between', str, '', 'Ornament to use between the chapter and title. Ignored if text format not split, '
                                    'not affected by case. Optional, defaults to none.'),
    '-t' : ('--text', str, 'combined', 'text format - one of "chapter" (just the numbering), "title" (just the title), '
                                  '"combined" (chapter then title on same line), "split" (title on separate line '
                                  'beneath chapter). Optional, defaults to combined.')
}

def set_fixes(value, case):
    # set prefix / suffix
    if value is not None and value != '':
        fix = apply_case(str.rstrip(value) + ' ', case)
    else:
        fix = ''
    return fix

def set_ornament(value, tag_name):
    use = False
    tag = None
    if value is not None and value != '':
        use = True
        tag = html_utils.new_html_element(tag_name, value)
    return use, tag

def set_chap_numbers(text_opt, offset):
    chap_num = 1
    chapters_skip = 0

    # configure starting chapter info - if text option isn't title only
    if text_opt != 'title':
        if offset > 0:
            chapters_skip = offset
        elif offset < 0:
            # convert offset to positive and add to starting number
            chap_num = chap_num + abs(offset)

    return chap_num, chapters_skip

def get_chapter_val(option_set, value):
    chap_text = ''
    # if using title only, don't need to calculate the chapter value
    if option_set['text'] == 'title':
        return chap_text
    if option_set['numbers'] == 'roman':
        chap_text = number_utils.convert_to_roman(value)
        # roman text should only be upper or lower case - if lower isn't selected, use upper
        if option_set['case'] == 'lower':
            chap_text = apply_case(chap_text, 'lower')
        else:
            chap_text = apply_case(chap_text, 'upper')
    elif option_set['numbers'] == 'arabic':
        chap_text = str(value)
    # default option is text, e.g. 'one'
    else:
        chap_text = apply_case(number_utils.convert_to_english(value), option_set['case'])

    return chap_text

def get_chapter_text(text, chapter_text, pre_val_suf):
    if text == 'title':
        # include prefix and suffix on either side of title in case people want to use them for decorating the title
        text_val = pre_val_suf[0] + get_title_from_chapter(chapter_text) + pre_val_suf[2]
    elif text == 'combined':
        text_val = ''.join(pre_val_suf) + get_title_from_chapter(chapter_text)
    # for 'chapter' and 'split', include suffix in case people want to use them for decoration
    else:
        text_val = ''.join(pre_val_suf)
    return str.strip(text_val)

def process_split_option(text_opt, chapter, use_between, between_tag):
    last_tag = chapter
    if text_opt == 'split':
        title_text = get_title_from_chapter(chapter.text)
        if title_text is not None and title_text != '':
            title_tag = html_utils.new_html_element(Tag.H2, title_text)
            last_tag = title_tag
            if use_between:
                new_tag = deepcopy(between_tag)
                chapter.addnext(new_tag)
                new_tag.addnext(title_tag)
            else:
                chapter.addnext(title_tag)

    return last_tag


def main(options, work_file):
    """Main entry point for the script. This script will take an HTML file that has been downloaded from AO3 and
    then been edited by the ao3_clean_html.py script, and modify the chapter titles according to the options given.
    Only works on multi-chapter fics."""
    logger.debug(file_utils.format_message('start main', ('file to process is ' + options['filename'])))
    html_root = html_utils.get_parsed_root(options['filename'])

    # set prefix and suffix
    prefix = set_fixes(options['prefix'], options['case'])

    suffix = set_fixes(options['suffix'], options['case'])
    # if combined and no suffix set, use default
    if options['text'] == 'combined' and suffix == '':
        suffix = ': '

    # set up ornaments - will need to append copies of the tags in the tree
    use_after, after_tag = set_ornament(options['after'], Tag.H6)
    use_between, between_tag = set_ornament(options['between'], Tag.H1)

    # configure starting chapter info - if text option isn't title only
    chap_num, chapters_skip = set_chap_numbers(options['text'], options['offset'])

    # find the chapters (h2 in div id=chapters)
    chapter_tags = html_utils.get_chapter_titles(html_root)

    for chapter in chapter_tags:
        # skip chapters until it's time to start numbering
        if chapters_skip > 0:
            chapters_skip -= 1
            continue

        # get chapter value
        chap_val_text = get_chapter_val(options, chap_num)
        # advance number ready for next round
        chap_num += 1

        # check for split option and configure text and between ornament
        last_tag = process_split_option(options['text'], chapter, use_between, between_tag)

        # update the chapter text with the new options
        chapter.text = get_chapter_text(options['text'], chapter.text, [prefix, chap_val_text, suffix])

        if use_after:
            last_tag.addnext(deepcopy(after_tag))

    # convert tree to string and write to output file
    file_utils.write_to_bfile(work_file, html_utils.get_html_string(html_root))


if __name__ == '__main__':
    arg_parser = get_arg_parser(OPTIONS_DICT)
    arg_parser.add_argument('filename', help='Filepath for the file to be processed. Required.')
    arg_parser.add_argument('output_dir', help='Folder to save output files.')

    # print the full help if no arguments passed
    if len(sys.argv) == 1:
        print('\033[31m Note:\033[0m use "-h" to get full usage information.')
    opts = vars(arg_parser.parse_args())

    folder = file_utils.setup_config(opts['output_dir'])

    # only need the first filename
    work_filename = file_utils.get_file_name(folder, opts['filename'])

    # process the file - pass arguments to main so it can be called from anthology script
    main(opts, work_filename)