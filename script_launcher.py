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
import ao3_chapnum_format, ao3_clean_html
from utils import file_utils, popup_utils


CLEAN = 'ao3_clean_html'
CHAPNUM = 'ao3_chapnum_format'
SCRIPT_LIST = {
    CLEAN: 'Select this script to process an HTML file downloaded from AO3 ready for import',
    CHAPNUM: 'Select this script to format the chapter numbers / headings in an AO3 HTML file that '
             'has been run through the cleanup script.'
    }


def check_opts_valid(options):
    result = False
    if not options:
        popup_utils.show_error('Cancelled', 'Input cancelled, script not run.')
    elif options['filename'] == '' or options['output_dir'] == '':
        popup_utils.show_error('Cannot run', 'One or more mandatory arguments missing, script not run.')
    else:
        result = True
    return result


def select_script(script_name):
    if script_name == CLEAN:
        launch_clean()
    elif script_name == CHAPNUM:
        launch_chapnum()


def launch_chapnum():
    # get options values from popup
    opts = popup_utils.ScriptPopup(title= 'AO3 ChapNum Format Script',
                                   script_desc="Format the chapter numbers / titles of a cleaned AO3 downloaded file.",
                                   opts_list=ao3_chapnum_format.OPTIONS_DICT).get_values()
    # if options complete, run the script
    if check_opts_valid(opts):
        folder = file_utils.setup_config(opts['output_dir'])
        work_filename = file_utils.get_file_name(folder, opts['filename'])
        ao3_chapnum_format.main(opts, work_filename)
        popup_utils.WrappedMessage('Script Finished', 'Chapter formatting script has finished.')


def launch_clean():
    # get options values from popup
    opts = popup_utils.ScriptPopup(title= 'AO3 Cleanup Script',
                                   script_desc="Clean up a file downloaded from AO3 ready for import.",
                                   opts_list=ao3_clean_html.OPTIONS_DICT).get_values()
    # if options complete, run the script
    if check_opts_valid(opts):
        folder = file_utils.setup_config(opts['output_dir'])
        work_filename, tags_filename, notes_filename = file_utils.setup_ao3_output(folder, opts['filename'])
        ao3_clean_html.main(opts['filename'], work_filename, tags_filename, notes_filename, opts['dash_style'])
        popup_utils.WrappedMessage('Script Finished', 'Cleanup script has finished.')


if __name__ == '__main__':
    get_value = popup_utils.RadioInput(title='Select Script',
                                     description="Choose the script that you want to run.",
                                     opts_list=SCRIPT_LIST)
    script = get_value.get_result()
    select_script(script)