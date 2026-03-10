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

import tkinter as tk
from dataclasses import dataclass
from tkinter import ttk, filedialog
from tkinter import font


def new_tk_var(var_type=str, value="", parent=None):
    """
    Creates a new tkinter Variable, depending on input type
    :param var_type: variable type - str or int means a StringVar or IntVar is created. Defaults to str
    :param value: the initial value of the variable
    :param parent: the item the variable is associated with
    :return: the populated variable
    """
    if var_type == int:
        new_var = tk.IntVar(parent)
        value = int(value)
    elif var_type == str:
        new_var = tk.StringVar(parent)
    else:
        new_var = tk.Variable(parent)
    new_var.set(value)
    return new_var


def get_args_list(opt_list=None, parent=None):
    """
    Takes the passed dict of options and converts it into a list of ScriptArgument values
    :param opt_list: dict of options - taken from the list in the script used to manage commandline arguments
    :param parent: the tk window that the argument variable will belong to
    :return:
    """
    if opt_list is None:
        opt_list = {}
    script_args = []
    for opt in opt_list:
        script_args.append(ScriptArgument(name=opt_list[opt][0].lstrip("-"),
                                         input_var=new_tk_var(opt_list[opt][1], opt_list[opt][2], parent),
                                         opt_list=opt_list[opt][3],
                                         description=opt_list[opt][4],
                                         input_opt=opt_list[opt][5]))
    # add mandatory options
    script_args.insert(0, ScriptArgument(name='filename',
                                                     description='Filepath for the file to be processed. Required.',
                                                     input_var=new_tk_var(str, ''),
                                                     opt_list=[],
                                                     input_opt='file',
                                                     mandatory=True))
    script_args.insert(0, ScriptArgument(name='output_dir',
                                                     description='Folder to save output files',
                                                     input_var=new_tk_var(str, ''),
                                                     opt_list=[],
                                                     input_opt='filedir',
                                                     mandatory=True))
    return script_args


def add_wrapped_args(parent,
                     args_list,
                     row_count,
                     title_font,
                     is_dynamic=False):
    """
    Takes a list of ScriptArguments and adds them to the parent item according to the format defined
    :param parent: The parent item to add the argument to
    :param args_list: List of arguments to add
    :param row_count: row number to start with
    :param title_font: the font to use for argument names
    :param is_dynamic: whether WrappedLabel items should have is_dynamic set true
    :return: the row counter value once all arguments have been added
    """

    for arg in args_list:
        # add separator
        ttk.Separator(parent, orient='horizontal').grid(column=0, row=row_count, sticky='WE', columnspan=3, pady=10)
        row_count += 1
        # add argument name
        WrappedLabel(parent, is_dynamic=is_dynamic, text=arg.name, font=title_font,
                     justify='left').grid(column=0, row=row_count, sticky='WE', columnspan=2)
        row_count += 1
        # add argument description
        WrappedLabel(parent, is_dynamic=is_dynamic, text=arg.description,
                     justify='left').grid(column=0, row=row_count, sticky='WE', columnspan=3)
        row_count += 1
        # add argument inputs
        if arg.input_opt == 'file':
            ttk.Entry(parent, textvariable=arg.input_var).grid(column=0, row=row_count, sticky='WE', columnspan=2)
            ttk.Button(parent, text='Select File',
                       command=lambda a=arg: a.input_var.set(
                           filedialog.askopenfilename(initialdir=".",
                                                      title="Select file to process",
                                                      filetypes=([("HTML", "*.html")])))).grid(column=2,
                                                                                               row=row_count,
                                                                                               sticky='WE')
        elif arg.input_opt == 'filedir':
            ttk.Entry(parent, textvariable=arg.input_var).grid(column=0, row=row_count, sticky='WE', columnspan=2)
            ttk.Button(parent, text='Select Directory',
                       command=lambda a=arg: a.input_var.set(
                           filedialog.askdirectory(initialdir=".",
                                                      title="Select output directory"))).grid(column=2,
                                                                                               row=row_count,
                                                                                               sticky='WE')
        elif arg.input_opt == 'radio':
            for opt in arg.opt_list:
                ttk.Radiobutton(parent, text=opt, variable=arg.input_var,
                                value=opt).grid(column=0, row=row_count, sticky='WE', columnspan=3)
                row_count += 1
            row_count -= 1 # accommodate for already having added one after last argument

        elif arg.input_opt == 'dropdown':
            box = ttk.Combobox(parent, textvariable=arg.input_var, values=arg.opt_list)
            box.grid(column=0, row=row_count, sticky='WE', columnspan=3)
            box['state'] = 'readonly'

        elif arg.input_opt == 'spin':
            if not arg.opt_list:
                spin = ttk.Spinbox(parent, textvariable=arg.input_var, from_=-10000, to=10000, increment=1)
            else:
                spin = ttk.Spinbox(parent, textvariable=arg.input_var, values=arg.opt_list)
            spin.grid(column=0, row=row_count, sticky='WE', columnspan=3)

        # otherwise 'free'
        else:
            ttk.Entry(parent, textvariable=arg.input_var).grid(column=0, row=row_count, sticky='WE', columnspan=3)

        # increase row count
        row_count += 1

    return row_count


def show_error(title, message):
    """
    Display an error popup either above current window or as a standalone popup.
    :param title: Message box title
    :param message: Error message
    """
    error_popup = tk.Tk()
    error_popup.title(title)
    error_popup.columnconfigure(0, weight=1, minsize=300)
    mainframe = ttk.Frame(error_popup, padding="12 12 12 12")
    mainframe.columnconfigure(0, weight=1)
    mainframe.grid(column=0, row=0, sticky='NEWS')
    WrappedLabel(mainframe, True, text=message, justify='left').grid(column=0, row=0, sticky='WE')
    ttk.Button(mainframe, text='OK', command=error_popup.destroy).grid(column=0, row=1)

    error_popup.mainloop()


def centre_window(window):
    screen_x = (window.winfo_screenwidth() - window.winfo_reqwidth()) // 2
    screen_y = (window.winfo_screenheight() - window.winfo_reqheight()) // 2
    window.geometry(f"+{screen_x}+{screen_y}")


class WrappedLabel(ttk.Label):
    """Label that wraps text at a specified length, and can dynamically update the wrap length if resized"""
    def __init__(self, master=None, is_dynamic=False, wrap_lth=300, **kwargs):
        super().__init__(master, wraplength=wrap_lth, **kwargs)
        if is_dynamic:
            self.bind('<Configure>', lambda e: self.update_width())

    def update_width(self):
        new_length = self.winfo_width()
        self.config(wraplength=new_length)


class VScrollFrame(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.canvas = tk.Canvas(self)
        self.canvas.grid(column=0, row=0, sticky='NEWS')
        self.canvas.columnconfigure(0, weight=1)

        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.vsb.grid(column=1, row=0, sticky='NS')
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.iframe = ttk.Frame(self.canvas, padding= '12 12 12 12')
        self.iframe.columnconfigure(0, weight=1)

        self.canvas.create_window((0, 0), window=self.iframe, anchor='nw', tags='inner')
        self.layout_update()
        self.canvas.bind('<Configure>', self.on_configure)

    def layout_update(self):
        # need to call update after arguments added
        self.iframe.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
        self.canvas.yview('moveto', '0.0')
        self.size = self.iframe.grid_size()

    def on_configure(self, event):
        w = event.width
        self.canvas.itemconfigure('inner', width=w )
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def get_info_frame(self):
        return self.iframe


class TextInput(tk.Tk):
    def __init__(self, title_text, label_text, is_dynamic=False, wrap_lth=300):
        """
        Text input box where the accompanying text is wrapped at a specific length and can be dynamically updated
        :param title_text: Title of the popup window
        :param label_text: Text accompanying the input box
        :param is_dynamic: Should wrap length be dynamically updated if the box is resized. Defaults to False
        :param wrap_lth: Length at which text should wrap. Defaults to 300
        """
        super().__init__()
        self.title(title_text)
        self.columnconfigure(0, weight=1, minsize=wrap_lth)
        self.value = tk.StringVar()
        mainframe = ttk.Frame(padding="12 12 12 12")
        mainframe.columnconfigure(0, weight=1)
        mainframe.grid(column=0, row=0, sticky='NEWS')
        label_value = tk.StringVar(value=label_text)
        text_entry = ttk.Entry(mainframe, textvariable=self.value)

        WrappedLabel(mainframe, is_dynamic, textvariable=label_value, wrap_lth=wrap_lth,
                     justify='left').grid(column=0, row=0, sticky='WE')
        text_entry.grid(column=0, row=1, sticky='WE')
        ttk.Button(mainframe, text='OK', command=self.destroy).grid(column=0, row=2, sticky='E')

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        text_entry.focus_force()
        self.mainloop()

    def get_result(self):
        return self.value.get()


class WrappedMessage(tk.Tk):
    def __init__(self, title_text, label_text, is_dynamic=False, wrap_length=300):
        """
        Message box where the  text is wrapped at a specific length and can be dynamically updated
        :param title_text: Title of the popup window
        :param label_text: Content of the popup window
        :param is_dynamic: Should wrap length be dynamically updated if the box is resized. Defaults to False
        :param wrap_length: Length at which text should wrap. Defaults to 300
        """
        super().__init__()
        self.title(title_text)
        self.columnconfigure(0, weight=1, minsize=wrap_length)
        mainframe = ttk.Frame(padding="12 12 12 12")
        mainframe.columnconfigure(0, weight=1)
        mainframe.grid(column=0, row=0, sticky='NEWS')
        WrappedLabel(mainframe, is_dynamic, text=label_text, wrap_lth=wrap_length,
                     justify='left').grid(column=0, row=0, sticky='WE', columnspan=3)
        ttk.Button(mainframe, text='OK', command=self.destroy).grid(column=1, row=1)

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        self.focus_force()
        self.mainloop()


class RadioInput(tk.Tk):
    def __init__(self, title, description, opts_list, is_dynamic=False, wrap_lth=300):
        super().__init__()
        self.title(title)
        self.columnconfigure(0, weight=1, minsize=wrap_lth)
        self.rowconfigure(0, weight=1)
        self.value = tk.StringVar()

        mainframe = ttk.Frame(padding="12 12 12 12")
        mainframe.columnconfigure(0, weight=1)
        mainframe.grid(column=0, row=0, sticky='NEWS')

        font_info = font.nametofont('TkDefaultFont')
        style = ttk.Style()
        style.configure('TRadiobutton', font = (font_info['family'], font_info['size'], 'bold'))
        # Add script information

        # add description
        WrappedLabel(mainframe, is_dynamic=is_dynamic, text=description,
                     justify='left').grid(column=0, row=0, sticky='WE', columnspan=2)

        rcount = 1
        for opt in opts_list:
            # add separator
            ttk.Separator(mainframe, orient='horizontal').grid(column=0, row=rcount, sticky='WE', columnspan=2, pady=10)
            # add option and description
            ttk.Radiobutton(mainframe, text=opt, style='TRadiobutton', variable=self.value,
                            value=opt).grid(column=0, row=rcount + 1, sticky='WE')
            WrappedLabel(mainframe, is_dynamic=is_dynamic, text=opts_list[opt],
                     justify='left').grid(column=1, row=rcount + 1, sticky='WE')
            rcount += 2

        # add OK Cancel buttons
        ttk.Separator(mainframe, orient='horizontal').grid(column=0, row=rcount, sticky='WE', columnspan=2, pady=10)
        rcount += 1
        ttk.Button(mainframe, text='Cancel', command=self.quit).grid(column=0, row=rcount,
                                                                                       sticky='E')
        ttk.Button(mainframe, text='OK', command=self.validate).grid(column=1, row=rcount, sticky='W')

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        self.mainloop()

    def get_result(self):
        if self.value:
            return self.value.get()
        else:
            return None

    def quit(self):
        self.value = None
        self.destroy()

    def validate(self):
        if not self.value or self.value.get() == '':
            show_error('No script selected',
                       'Please select a script or cancel.')
        else:
            self.destroy()


@dataclass
class ScriptArgument:
    """
    :param name: str - the name of the argument. Must match the "long option" without the leading --
    :param description: str - the argument description.
    :param input_var: tk.Variable - the variable used to manage the argument value
    :param opt_list: list - the allowed values for the argument
    :param input_opt: string - widget used to set value. One of 'free', 'file', 'radio', 'dropdown', 'spin'
    :param mandatory: bool - must this argument have a value other than ''
    :param multi_select: bool - can multiple values be selected
    """
    name: str
    description: str
    input_var: tk.Variable
    opt_list: list
    input_opt: str
    mandatory: bool = False
    multi_select: bool = False


class ScriptPopup:
    def __init__(self, title, script_desc, opts_list):
        self.value_list = {}  # argument values to be returned
        self.title = title
        self.description = script_desc

        window = tk.Tk()
        window.columnconfigure(0, weight=1)
        window.rowconfigure(0, weight=1)
        window.title(self.title)
        outer_frame = VScrollFrame(window)
        outer_frame.grid(column=0, row=0, sticky='NEWS')

        # now that inner frame available, create args list
        inner_frame = outer_frame.get_info_frame()
        self.args_list = get_args_list(opts_list, inner_frame)

        b_font = font.nametofont('TkDefaultFont').copy()
        b_font['weight'] = 'bold'
        # Add script information
        WrappedLabel(inner_frame, text=title, font=b_font).grid(column=0, row=0, sticky='WE', columnspan=2)
        WrappedLabel(inner_frame, is_dynamic=True, text=script_desc).grid(column=0, row=1, sticky='WE', columnspan=3)

        # add arguments
        row_int = add_wrapped_args(inner_frame, self.args_list, 2, title_font=b_font, is_dynamic=True)

        # add OK Cancel buttons
        ttk.Separator(inner_frame, orient='horizontal').grid(column=0, row=row_int, sticky='WE', columnspan=3, pady=10)
        row_int += 1
        ttk.Button(inner_frame, text='Cancel', command=lambda: self.quit(window)).grid(column=1, row=row_int, sticky='E')
        ttk.Button(inner_frame, text='OK', command=lambda: self.validate(window)).grid(column=2, row=row_int, sticky='W')

        outer_frame.layout_update()
        window.mainloop()

    def get_values(self):
        if self.value_list == {}:
            for arg in self.args_list:
                self.value_list[arg.name] = arg.input_var.get()
        return self.value_list

    def quit(self, tk_window):
        self.args_list = {}
        tk_window.destroy()

    def validate(self, tk_window):
        self.get_values()
        if self.value_list['filename'] == '' or self.value_list['output_dir'] == '':
            # missing value - blank the value list and try again
            self.value_list = {}
            show_error('Mandatory argument missing',
                       'Please check that filename and output directory have been provided.')
        else:
            tk_window.destroy()