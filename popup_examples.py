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
from utils import popup_utils
from utils.popup_utils import TextInput, WrappedMessage
import tkinter as tk
from tkinter import ttk

# Example input and message boxes with wrapped text.
my_value = TextInput("Fixed Width Input",
                        "This message has a fixed width for wrapping which is the default of 300. If you pull "
                        "the box wider the width of the text is unaffected. This message will not scroll if it is "
                        "longer than the message box height. Please input a value here.").get_result()

WrappedMessage("Response", "Your response was '" + my_value + "'!")

my_value = TextInput("Dynamic Width Input",
                        "This message starts with a custom width of 200, but can be dynamically resized. If you"
                        " pull the box wider or narrower, the text will automatically adjust (unless it is narrower "
                        "than the messagebox minimum). Please input a value here.", True, 200).get_result()

WrappedMessage("Response", "Your response was '" + my_value + "'!", 200)


# Example of how to create a message box with multiple WrappedLabel messages in a vertically scrolled window
text_arg='the quick brown fox jumped over the lazy dog, oh sphinx of black quartz judge my vow. '

window = tk.Tk()
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)
window.title('scrolling example')
outer_frame = popup_utils.VScrollFrame(window)
outer_frame.grid(column=0, row=0, sticky='NWSE')

inner_frame = outer_frame.get_info_frame()
popup_utils.WrappedLabel(inner_frame, is_dynamic=True,
                         text=text_arg + text_arg + text_arg + text_arg + text_arg).grid(column=0, row=0, sticky='WE')
ttk.Separator(inner_frame, orient='horizontal').grid(column=0, row=1, sticky='WE', pady=10)
popup_utils.WrappedLabel(inner_frame, is_dynamic=True,
                         text=text_arg + text_arg + text_arg + text_arg + text_arg).grid(column=0, row=2, sticky='WE')
ttk.Separator(inner_frame, orient='horizontal').grid(column=0, row=3, sticky='WE', pady=10)
popup_utils.WrappedLabel(inner_frame, is_dynamic=True,
                         text=text_arg + text_arg + text_arg + text_arg + text_arg).grid(column=0, row=4, sticky='WE')
ttk.Separator(inner_frame, orient='horizontal').grid(column=0, row=5, sticky='WE', pady=10)
ttk.Button(inner_frame, text='OK').grid(column=0, row=6, sticky='W')
window.mainloop()

# For an example of using the ScriptArgument and ScriptPopup classes, see the "script_launcher" python script.