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

from utils import file_utils, html_utils, Tag, Punctuation, XpathPart, Attr
from utils.html_utils import make_xpath, new_html_element

logger = logging.getLogger(__name__)


def move_tags(html_root, tags_root):
    # get the initial message of "originally posted on..."
    element = new_html_element(Tag.DIV, None)
    element.append(html_root.xpath(make_xpath([XpathPart.ALL_FROM_ROOT,
                                               Tag.PARAGRAPH + XpathPart.item_with_val(XpathPart.CLASS.name,
                                                                                       Attr.MESSAGE)
                                               ]))[0])
    # Get the list of tags
    tags = html_root.xpath(make_xpath([XpathPart.ALL_FROM_ROOT,
                                       Tag.DL + XpathPart.item_with_val(XpathPart.CLASS.name, Attr.TAGS)]))
    body_element = tags_root.find(Tag.BODY.get_find_str())
    body_element.append(element)
    body_element.append(tags[0])


def move_notes(html_root, notes_root):
    body_element = notes_root.find(Tag.BODY.get_find_str())
    # move title/author in root
    pre_div = html_root.xpath(make_xpath([XpathPart.ALL_FROM_ROOT,
                                          Tag.DIV + XpathPart.item_with_val(XpathPart.ID.name, Attr.PREFACE)]))[0]
    pre_div.find(Tag.H2.get_find_str()).drop_tree()
    pre_div.append(pre_div.xpath(make_xpath([XpathPart.ALL_FROM_ROOT,
                                             Tag.DIV + XpathPart.item_with_val(XpathPart.CLASS.name, Attr.META),
                                             Tag.H1
                                             ]))[0])
    pre_div.append(pre_div.xpath(make_xpath([XpathPart.ALL_FROM_ROOT,
                                             Tag.DIV + XpathPart.item_with_val(XpathPart.CLASS.name, Attr.META),
                                             Tag.DIV + XpathPart.item_with_val(XpathPart.CLASS.name, Attr.BYLINE)
                                             ]))[0])

    # move summary and work notes
    body_element.append(pre_div.xpath(make_xpath([XpathPart.ALL_FROM_ROOT,
                                                  Tag.DIV + XpathPart.item_with_val(XpathPart.CLASS.name, Attr.META)
                                                  ]))[0])

    # move chapter start / end notes
    group1 = make_xpath([XpathPart.ALL_FROM_ROOT,
                         Tag.DIV + XpathPart.item_with_val(XpathPart.ID.name, Attr.CHAPTERS),
                         Tag.DIV + XpathPart.item_with_val(XpathPart.CLASS.name, Attr.META_GRP)])
    group2 = make_xpath([XpathPart.ALL_FROM_ROOT,
                         Tag.DIV + XpathPart.item_with_val(XpathPart.ID.name, Attr.CHAPTERS),
                         Tag.DIV + XpathPart.item_with_val(XpathPart.CLASS.name, Attr.META)])
    meta_groups = html_root.xpath(group1 + XpathPart.GROUP_SEPARATOR + group2)
    for group in meta_groups:
        if group.get(Attr.CLASS) == Attr.META_GRP:
            text_div = group.getnext()
            headings = group.xpath(make_xpath([XpathPart.ALL_FROM_ROOT,
                                               Tag.H2 + XpathPart.item_with_val(XpathPart.CLASS.name, Attr.HEADING)]))
            if len(headings) > 0:
                element = new_html_element(Tag.H2, headings[0].text)
                text_div.addprevious(element)
            body_element.append(group)
        else:
            body_element.append(group)

    # move afterword
    afterword = html_root.xpath(make_xpath([XpathPart.ALL_FROM_ROOT,
                                            Tag.DIV + XpathPart.item_with_val(XpathPart.ID.name, Attr.AFTERWORD)]))
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
    html_utils.deltree_all_of_tag(html_root, make_xpath([XpathPart.SINGLE_REL_PATH, Tag.HEAD, Tag.TITLE]))
    html_utils.deltree_all_of_tag(html_root, make_xpath([XpathPart.SINGLE_REL_PATH, Tag.HEAD, Tag.STYLE]))

    # remove html links
    html_utils.drop_all_of_tag(html_root, Tag.ANCHOR.get_find_str())

    # change bold and italics to consistent tag
    html_utils.update_tag_type(html_root, Tag.BOLD.get_find_str(), Tag.STRONG)
    html_utils.update_tag_type(html_root, Tag.ITALIC.get_find_str(), Tag.EMPHASIS)

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
    html_utils.deltree_all_of_tag(html_root, make_xpath([XpathPart.ALL_REL_TO_NODE,
                                                         Tag.ANY + XpathPart.item_with_val(XpathPart.CLASS.name,
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

    # get any passed arguments
    if len(sys.argv) > 2:
        html_filename = sys.argv[1]
        output_dir = sys.argv[2]
        if len(sys.argv) > 3:
            dash_style = sys.argv[3]
        else:
            dash_style = None
    else:
        print("usage: python ao3_clean_html.py <html_filename> <output_directory> [<dash_style>] where dash_style is "
              "one of 'UK' or 'US'. If not specified then dashes will not be updated.")
        sys.exit(1)

    # set up the output folder and log file
    folder = file_utils.setup_config(output_dir)

    # set up filenames for the modified work, the tags, and any author / chapter notes
    work_filename, tags_filename, notes_filename = file_utils.setup_ao3_output(folder, html_filename)

    # process the file - pass arguments to main so it can be called from anthology script
    main(html_filename, work_filename, tags_filename, notes_filename, dash_style)
