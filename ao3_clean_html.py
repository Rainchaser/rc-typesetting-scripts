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
import sys

from utils import file_utils, html_utils, Tag, Punctuation, XpathPart, Attr, get_arg_parser
from utils.html_utils import make_xpath, new_html_element

logger = logging.getLogger(__name__)

# short code: (long code, type, default, options, description, popup input (if using script launcher)
OPTIONS_DICT = {
    '-d' : ('--dash_style', str, '', ['','UK', 'US'], 'Dash style is one of "UK" or "US". If left blank then '
                                                         'dash style will not be updated.', 'dropdown')
}

def move_tags(html_root, tags_root):
    # get the initial message of "originally posted on..."
    element = new_html_element(Tag.DIV.value, None)
    element.append(html_root.xpath(make_xpath([XpathPart.ALL_FROM_ROOT.value,
                                               Tag.PARAGRAPH.value + XpathPart.item_with_val(XpathPart.CLASS.name,
                                                                                       Attr.MESSAGE.value)
                                               ]))[0])
    # Get the list of tags
    tags = html_root.xpath(make_xpath([XpathPart.ALL_FROM_ROOT.value,
                                       Tag.DL.value + XpathPart.item_with_val(XpathPart.CLASS.name, Attr.TAGS.value)]))
    body_element = tags_root.find(Tag.BODY.get_find_str())
    body_element.append(element)
    body_element.append(tags[0])


def move_notes(html_root, notes_root):
    body_element = notes_root.find(Tag.BODY.get_find_str())
    # move title/author in root
    pre_div = html_root.xpath(make_xpath([XpathPart.ALL_FROM_ROOT.value,
                                          Tag.DIV.value + XpathPart.item_with_val(XpathPart.ID.name, Attr.PREFACE.value)]))[0]
    pre_div.find(Tag.H2.get_find_str()).drop_tree()
    pre_div.append(pre_div.xpath(make_xpath([XpathPart.ALL_FROM_ROOT.value,
                                             Tag.DIV.value + XpathPart.item_with_val(XpathPart.CLASS.name, Attr.META.value),
                                             Tag.H1.value
                                             ]))[0])
    pre_div.append(pre_div.xpath(make_xpath([XpathPart.ALL_FROM_ROOT.value,
                                             Tag.DIV.value + XpathPart.item_with_val(XpathPart.CLASS.name, Attr.META.value),
                                             Tag.DIV.value + XpathPart.item_with_val(XpathPart.CLASS.name, Attr.BYLINE.value)
                                             ]))[0])

    # move summary and work notes
    body_element.append(pre_div.xpath(make_xpath([XpathPart.ALL_FROM_ROOT.value,
                                                  Tag.DIV.value + XpathPart.item_with_val(XpathPart.CLASS.name, Attr.META.value)
                                                  ]))[0])

    # move chapter start / end notes
    group1 = make_xpath([XpathPart.ALL_FROM_ROOT.value,
                         Tag.DIV.value + XpathPart.item_with_val(XpathPart.ID.name, Attr.CHAPTERS.value),
                         Tag.DIV.value + XpathPart.item_with_val(XpathPart.CLASS.name, Attr.META_GRP.value)])
    group2 = make_xpath([XpathPart.ALL_FROM_ROOT.value,
                         Tag.DIV.value + XpathPart.item_with_val(XpathPart.ID.name, Attr.CHAPTERS.value),
                         Tag.DIV.value + XpathPart.item_with_val(XpathPart.CLASS.name, Attr.META.value)])
    meta_groups = html_root.xpath(group1 + XpathPart.GROUP_SEPARATOR.value + group2)
    for group in meta_groups:
        if group.get(Attr.CLASS.value) == Attr.META_GRP.value:
            text_div = group.getnext()
            headings = group.xpath(make_xpath([XpathPart.ALL_FROM_ROOT.value,
                                               Tag.H2.value + XpathPart.item_with_val(XpathPart.CLASS.name, Attr.HEADING.value)]))
            if len(headings) > 0:
                element = new_html_element(Tag.H2.value, headings[0].text)
                text_div.addprevious(element)
            body_element.append(group)
        else:
            body_element.append(group)

    # move afterword
    afterword = html_root.xpath(make_xpath([XpathPart.ALL_FROM_ROOT.value,
                                            Tag.DIV.value + XpathPart.item_with_val(XpathPart.ID.name, Attr.AFTERWORD.value)]))
    for note in afterword:
        body_element.append(note)


def main(html_file, work_file, tags_file, notes_file, dash_style_opt):
    """
    Converts an AO3 HTML file to a cleaned up format for Scribus, and moves tags and notes to additional files for
    optional inclusion.
    Arguments are passed in explicitly, so that main can be called from other scripts
    """
    logger.debug(file_utils.format_message("start main", ("file to process is " + html_file)))
    html_root = html_utils.get_parsed_root(html_file)

    # remove meta title and style
    html_utils.deltree_all_of_tag(html_root, make_xpath([XpathPart.SINGLE_REL_PATH.value, Tag.HEAD.value, Tag.TITLE.value]))
    html_utils.deltree_all_of_tag(html_root, make_xpath([XpathPart.SINGLE_REL_PATH.value, Tag.HEAD.value, Tag.STYLE.value]))

    # remove html links
    html_utils.drop_all_of_tag(html_root, Tag.ANCHOR.get_find_str())

    # change bold and italics to consistent tag
    html_utils.update_tag_type(html_root, Tag.BOLD.get_find_str(), Tag.STRONG.value)
    html_utils.update_tag_type(html_root, Tag.ITALIC.get_find_str(), Tag.EMPHASIS.value)

    # convert ellipse and dash style to proper format
    html_utils.convert_punctuation(html_root, Punctuation.ELLIPSIS)
    html_utils.convert_punctuation(html_root, Punctuation.get_dash_style(dash_style_opt))

    # tags - move them to a separate file
    tags_root = html_utils.new_html_base("tags")
    move_tags(html_root, tags_root)

    # notes - move them to a separate file
    notes_root = html_utils.new_html_base("notes")
    move_notes(html_root, notes_root)

    # remove remaining TOC title heading if present (single-chapter fics only)
    html_utils.deltree_all_of_tag(html_root, make_xpath([XpathPart.ALL_REL_TO_NODE.value,
                                                         Tag.ANY.value + XpathPart.item_with_val(XpathPart.CLASS.name,
                                                                                           'toc-heading')
                                                         ]))

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

    arg_parser = get_arg_parser(OPTIONS_DICT)
    arg_parser.add_argument('filename', help='Filepath for the file to be processed. Required.')
    arg_parser.add_argument('output_dir', help='Folder to save output files.')

    # print the full help if no arguments passed
    if len(sys.argv) == 1:
        print('\033[31m Note:\033[0m use "-h" to get full usage information.')
    opts = vars(arg_parser.parse_args())

    # set up the output folder and log file
    folder = file_utils.setup_config(opts['output_dir'])

    # set up filenames for the modified work, the tags, and any author / chapter notes
    work_filename, tags_filename, notes_filename = file_utils.setup_ao3_output(folder, opts['filename'])

    # process the file - pass arguments to main so it can be called from anthology script
    main(opts['filename'], work_filename, tags_filename, notes_filename, opts['dash_style'])