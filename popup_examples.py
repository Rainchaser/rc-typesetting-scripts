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
from tkinter.constants import LEFT

from utils.popup_utils import WrappedInput, WrappedMessage

my_value = WrappedInput("MessageBox Title - Input",
                        "Please input a value here, this will be used to demonstrate that we can wrap a label"
                        " so that the text doesn't get cut off when the box is generated.").get_result()

WrappedMessage("MessageBox Title - Response", "Your response was '" + my_value + "'!")

my_value = WrappedInput("MessageBox Title - Input",
                        "Please input a value here, this will be used to demonstrate that we can set how long"
                        " the string can be before it is wrapped, in case you want to the box size. The first box was"
                        " set to the default of 300, this one is set to 200 .", 200).get_result()

WrappedMessage("MessageBox Title - Response", "Your response was '" + my_value + "'!", 200)