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
from tkinter import ttk

class WrappedInput(tk.Tk):
    def __init__(self, title_text, label_text, wrap_length=300):
        super().__init__()
        self.title(title_text)
        self.value = tk.StringVar()
        mainframe = ttk.Frame(padding="12 12 12 12")
        mainframe.grid(column=0, row=0, sticky='NWSE')
        label_value = tk.StringVar(value=label_text)
        text_entry = ttk.Entry(mainframe, textvariable=self.value)

        ttk.Label(mainframe, textvariable=label_value, wraplength=wrap_length, justify='left').grid(column=0, row=0, sticky='W')
        text_entry.grid(column=0, row=1, sticky='WE')
        ttk.Button(mainframe, text='OK', command=lambda: self.destroy()).grid(column=0, row=2, sticky='E')

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        text_entry.focus_force()
        self.mainloop()

    def get_result(self):
        return self.value.get()


class WrappedMessage(tk.Tk):
    def __init__(self, title_text, label_text, wrap_length=300):
        super().__init__()
        self.title(title_text)
        self.value = tk.StringVar()
        mainframe = ttk.Frame(padding="12 12 12 12")
        mainframe.grid(column=0, row=1, sticky='NWSE')
        label_value = tk.StringVar(value=label_text)
        (ttk.Label(mainframe, textvariable=label_value, wraplength=wrap_length, justify='left')
         .grid(column=0, row=0, sticky='W', columnspan=3))
        ttk.Button(mainframe, text='OK', command=lambda: self.destroy()).grid(column=1, row=1)

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        self.focus_force()
        self.mainloop()