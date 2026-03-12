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
from tkinter import ttk, filedialog


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

    # add variable to store selected value
    dropdown_value = tk.StringVar(frame)
    # set the initial value of the combobox - omit if the dropdown should start with no value set
    dropdown_value.set(options_list[0])
    # create the dropdown widget
    ttk.Combobox(frame, textvariable=dropdown_value, values=options_list, state='readonly').grid(column=0, row=1, sticky='WE')

    # add a separator and an OK button
    ttk.Separator(frame, orient='horizontal').grid(column=0, row=2, sticky='WE', pady=5)
    ttk.Button(frame, text='OK', command=root.destroy).grid(column=0, row=3, sticky='WE')

    # display the window
    root.mainloop()
    # once the window is closed, return the selected value
    return dropdown_value.get()


# Example simple listbox popup - using grid method.
def listbox_example(title_val, label_val, options_list):
    # create the nested function to set the value when an item is selected
    def set_value(event):
        if len(listbox.curselection()) == 1:
            pos = int(listbox.curselection()[0])
            listbox_value.set(options_list[pos])

    # create the base window
    root = tk.Tk()
    root.title = title_val

    # add a frame to let the popup match the base OS styling
    frame = ttk.Frame(root)
    frame.grid(column=0, row=0, padx=5, pady=5, sticky='NEWS')

    # add the label - it isn't referenced by later code so no need to assign to a variable
    ttk.Label(frame, text=label_val).grid(column=0, row=0, sticky='WE')

    # add variables to store the options list and the selected value.
    listbox_options = tk.StringVar(frame, options_list)
    listbox_value = tk.StringVar(frame)

    # add the listbox - need to assign to a variable to allow binding the selection event
    listbox = tk.Listbox(frame, listvariable=listbox_options)
    listbox.grid(column=0, row=1, sticky='WE')

    # bind the selection event to the nested function
    listbox.bind('<<ListboxSelect>>', set_value)

    # add a separator and an OK button
    ttk.Separator(frame, orient='horizontal').grid(column=0, row=2, sticky='WE', pady=5)
    ttk.Button(frame, text='OK', command=root.destroy).grid(column=0, row=3, sticky='WE')

    # display the window
    root.mainloop()

    # once the window is closed, return the selected value
    return listbox_value.get()


# Example simple radio popup - using grid method.
def radio_example(title_val, label_val, options_list):
    # create the base window
    root = tk.Tk()
    root.title = title_val

    # add a frame to let the popup match the base OS styling
    frame = ttk.Frame(root)
    frame.grid(column=0, row=0, padx=5, pady=5, sticky='NEWS')

    # add the label - it isn't referenced by later code so no need to assign to a variable
    ttk.Label(frame, text=label_val).grid(column=0, row=0, sticky='WE')

    # set up a variable for the output
    radio_value = tk.StringVar()

    # add a radio button for each option in the options list - use a variable for the row number as don't know the
    # number of options.
    row_count = 1
    for opt in options_list:
        ttk.Radiobutton(frame, text=opt, variable=radio_value,
                        value=opt).grid(column=0, row=row_count, sticky='WE')
        row_count += 1

    # add a separator and an OK button
    ttk.Separator(frame, orient='horizontal').grid(column=0, row=row_count, sticky='WE', pady=5)
    ttk.Button(frame, text='OK', command=root.destroy).grid(column=0, row=row_count+1, sticky='WE')

    # display the window
    root.mainloop()
    # once the window is closed, return the selected value
    return radio_value.get()


# Example simple spinbox popup - using grid method.
def spinbox_example(title_val, label_val, options_list):
    # create the base window
    root = tk.Tk()
    root.title = title_val

    # add a frame to let the popup match the base OS styling
    frame = ttk.Frame(root)
    frame.grid(column=0, row=0, padx=5, pady=5, sticky='NEWS')

    # add an example number spinbox
    new_value = tk.IntVar()
    ttk.Label(frame, text='This is a demo box to show getting a number between 10 and '
                          '-10. The value is not returned by the function').grid(column=0, row=0, sticky='WE')
    ttk.Spinbox(frame, textvariable=new_value, from_=-10, to=10,
                wrap=True, state='readonly').grid(column=0, row=1, sticky='WE')
    ttk.Separator(frame, orient='horizontal').grid(column=0, row=2, sticky='WE', pady=5)

    # add the label - it isn't referenced by later code so no need to assign to a variable
    ttk.Label(frame, text=label_val).grid(column=0, row=3, sticky='WE')

    # create the variable to store the selected value.
    spinbox_value = tk.StringVar(frame)
    # set the initial value of the spinbox - omit if the spinbox should start with no value set
    spinbox_value.set(options_list[0])
    # create the spinbox widget - set wrap=True to move from the lowest to highest value. Defaults to False
    ttk.Spinbox(frame, textvariable=spinbox_value, values=options_list,
                wrap=True, state='readonly').grid(column=0, row=4, sticky='WE')

    # add a separator and an OK button
    ttk.Separator(frame, orient='horizontal').grid(column=0, row=5, sticky='WE', pady=5)
    ttk.Button(frame, text='OK', command=root.destroy).grid(column=0, row=6, sticky='WE')

    # display the window
    root.mainloop()
    # once the window is closed, return the selected value
    return spinbox_value.get()

# Example simple listbox popup - using grid method.
def file_dialog_example(title_val, label_val):
    # create the base window
    root = tk.Tk()
    root.title = title_val

    # add a frame to let the popup match the base OS styling
    frame = ttk.Frame(root)
    frame.grid(column=0, row=0, padx=5, pady=5, sticky='NEWS')

    # add the label - it isn't referenced by later code so no need to assign to a variable
    ttk.Label(frame, text=label_val).grid(column=0, row=0, sticky='WE')

    # add variable to store the chosen file and directory paths
    file_value = tk.StringVar(frame)
    dir_value = tk.StringVar(frame)

    # add an Entry to store the value for the file
    ttk.Entry(frame, textvariable=file_value).grid(column=0, row=1, sticky='WE')
    # add a button to bind the file selection dialog to - this example will filter to HTML and txt files only
    ttk.Button(frame, text='Select File',
               command=lambda: file_value.set(filedialog.askopenfilename(initialdir=".",
                                              title="Select file to process",
                                              filetypes=([("HTML", "*.html"), ("TEXT", "*.txt")])))
               ).grid(column=1, row=1, sticky='WE')
    # add an Entry to store the value for the directory
    ttk.Entry(frame, textvariable=dir_value).grid(column=0, row=2, sticky='WE')
    ttk.Button(frame, text='Select Directory',
               command=lambda: dir_value.set(
                   filedialog.askdirectory(initialdir=".", title="Select output directory"))
               ).grid(column=1, row=2, sticky='WE')


    # add a separator and an OK button
    ttk.Separator(frame, orient='horizontal').grid(column=0, row=3, sticky='WE', pady=5)
    ttk.Button(frame, text='OK', command=root.destroy).grid(column=0, row=4, sticky='WE')

    # display the window
    root.mainloop()
    # once the window is closed, return the selected value
    return file_value.get(), dir_value.get()


# Usage examples:
label_text = 'Select a day:'
answer_prefix = "Answer: "
# Example dropdown popup
day_list = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
text = dropdown_example('Test Dropdown Window', label_text, day_list)
WrappedMessage("Response", answer_prefix + text)

# Example listbox popup
day_list = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
text = listbox_example('Test Listbox Window', label_text, day_list)
WrappedMessage("Response", answer_prefix + text)

# Example radio popup
day_list = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
text = radio_example('Test Radio Window', label_text, day_list)
WrappedMessage("Response", answer_prefix + text)

# Example spinbox popup
day_list = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
text = spinbox_example('Test Spinbox Window', label_text, day_list)
WrappedMessage("Response", answer_prefix + text)

# Example file and dir selection popup
day_list = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
file_text, dir_text = file_dialog_example('Test File Window', 'Select a file and directory:')
WrappedMessage("Response", answer_prefix + file_text + " " + dir_text, wrap_length=500)


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