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

# Example simple dropdown popup - using grid method.
# Sticky option is which side(s) of the grid cell an item should stick to (using compass directions)
def dropdown_example(title_val, label_val, options_list):
    # create the base window
    root = tk.Tk()
    root.title = title_val

    # add a frame to let the popup match the base OS styling
    frame = ttk.Frame(root)
    frame.grid(column=0, row=0, padx=5, pady=5, sticky='NEWS')

    # add the label - it isn't referenced by later code so no need to assign to a variable
    ttk.Label(frame, text=label_val).grid(column=0, row=0, sticky='WE')

    # add dropdown widget - setting it as readonly so have to assign to a variable.
    dropdown_value = tk.StringVar(frame)
    # set the initial value of the combobox - omit if the dropdown should start with no value set
    dropdown_value.set(options_list[0])
    box = ttk.Combobox(frame, textvariable=dropdown_value, values=options_list)
    box.grid(column=0, row=1, sticky='WE')
    box['state'] = 'readonly'

    # add a separator and an OK button
    ttk.Separator(frame, orient='horizontal').grid(column=0, row=2, sticky='WE', pady=5)
    ttk.Button(frame, text='OK', command=root.destroy).grid(column=0, row=3, sticky='WE')

    # display the window
    root.mainloop()
    # once the window is closed, return the selected value
    return dropdown_value.get()

# Example dropdown popup
day_list = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
text = dropdown_example('Test Dropdown Window', 'Select a day:', day_list)

WrappedMessage("Response", "Answer: " + text)


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
ttk.Button(inner_frame, text='OK', command=window.destroy).grid(column=0, row=6, sticky='W')
window.mainloop()

# For examples of using the RadioInput, ScriptArgument and ScriptPopup classes, see the "script_launcher" python script.