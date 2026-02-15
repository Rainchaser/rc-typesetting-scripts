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

from datetime import datetime
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)


def setup_config(parent):
    """
    Create timestamped output directory and set logging config for all loggers.
    :param parent: The directory where the timestamped directory should be created
    :return: the timestamped directory
    """
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    folder = os.path.join(parent, timestamp)
    if not os.path.exists(folder):
        os.makedirs(folder)

    logging.basicConfig(filename=os.path.join(folder, timestamp + ".log"), encoding='utf-8', level=logging.DEBUG)

    return folder


def setup_ao3_output(output_path, filename):
    """
    Set up the filename for the split / modified output from a file.

    :param output_path: the path to the directory where the files should be saved
    :param filename: name of the original file (may include path)
    :returns: names for work_file (main content); tags_file (any tags removed from the work);
      notes_file (any author / chapter notes removed from the work)
    """
    work_name = Path(filename).stem
    suffix = Path(filename).suffix
    time = Path(output_path).stem
    work_file = Path(output_path, work_name + '_' + time + suffix)
    tags_file = Path(output_path, work_name + '_tags_' + time + suffix)
    notes_file = Path(output_path, work_name + '_notes_' + time + suffix)

    return work_file, tags_file, notes_file


def get_file_name(output_path, filename):
    name = Path(filename).stem
    suffix = Path(filename).suffix
    time = Path(output_path).stem

    return Path(output_path, name + '_' + time + suffix)


def format_message(action, message):
    """
    Format a message for logging / reporting
    :param action: action being performed when message generated
    :param message: text of message
    :returns: formatted message"""
    message = 'Action {}: {}'.format(action, message)

    return message


def append_to_rfile(file_path, value):
    """
    Append an entry to file in regular (non-binary) mode.
    :param file_path: path to target file
    :param value: string to write to file
    """
    logger.debug("Attempting to write to file")
    with open(file_path, 'a') as write_file:
        write_file.write(value)
        write_file.write('\n')


def write_to_bfile(file_path, value):
    """
    write an entry to file in binary mode.
    :param file_path: path to target file
    :param value: string to write to file
    """
    logger.debug("Attempting to write to file")
    with open(file_path, 'wb') as write_file:
        write_file.write(value)
