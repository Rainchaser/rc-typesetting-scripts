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
from pathlib import Path

logger = logging.getLogger(__name__)

"""Set logging config for all loggers"""
def set_log_config(filename):
    logging.basicConfig(filename=filename, encoding='utf-8', level=logging.DEBUG)

"""Set up the output file names"""
def setup_output(output_path,filename):
    fic_name = Path(filename).stem
    time = Path(output_path).stem
    work_file = Path(output_path, fic_name + '_' + time + '.html')
    tags_file = Path(output_path, fic_name + '_tags_' + time + '.html')
    notes_file = Path(output_path, fic_name + '_notes_' + time + '.html')

    return work_file, tags_file, notes_file

"""Format a message"""
def format_message(action, message):
    message = ('Action %s: %s' % action % message)
    return message


"""Add an entry to the report file"""
def add_entry(file_path, value):
    logger.debug("Attempting to write to file")
    with open(file_path, 'a') as write_file:
        write_file.write(value)
        write_file.write('\n')

"""Add an entry to the specified file"""
def write_to_html(file_path, value):
    logger.debug("Attempting to write to file")
    with open(file_path, 'wb') as write_file:
        write_file.write(value)
