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

import unittest
from utils import string_utils

test_title_values = [
    ('Chapter 1: Title text here', 'Title text here'),
    ('Chapter two: title text here', 'title text here'),
    ('Chapter three', ''),
    ('chapter IV', ''),
    ('\nchapter IV - title text here\n', 'title text here'),
    ('chapter fifteen ~ title text here', 'title text here'),
    ('IV', ''),
    ('TWENTY-TWO', ''),
    ('\nCh Thirty Two\n', ''),
    ('#22 - title', 'title'),
    ('#22 | here we go again', 'here we go again'),
    ("#22 | Where I've made mistakes & paid the price", "Where I've made mistakes & paid the price")
]

test_case_values = [
    ('Chapter one: Title text here', 'CHAPTER ONE: TITLE TEXT HERE', 'upper'),
    ('CHAPTER TWO: Title Text Here', 'chapter two: title text here', 'lower'),
    ("chapter three: Title text here", "Chapter Three: Title Text Here", 'title'),
]


class TestStringUtils(unittest.TestCase):
    def test_get_title(self):
        for test_text, exp_out in test_title_values:
            actual_output = string_utils.get_title_from_chapter(test_text)
            self.assertEqual(exp_out, actual_output)

    def test_apply_case(self):
        for test_text, exp_out, case in test_case_values:
            actual_output = string_utils.apply_case(test_text, case)
            self.assertEqual(exp_out, actual_output)

    def test_text_replace(self):
        test_string = 'This is a test'
        expected_output = 'This is not a test'
        actual_output = string_utils.text_replace(test_string, 'is a', 'is not a')
        self.assertEqual(expected_output, actual_output)


if __name__ == '__main__':
    unittest.main()
