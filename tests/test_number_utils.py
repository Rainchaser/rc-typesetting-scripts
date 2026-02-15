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

from utils import number_utils

roman_values = [
    ('IV', 4),
    ('VI', 6),
    ('XIV', 14),
    ('XV', 15),
    ('XIX', 19),
    ('XL', 40),
    ('XLIX', 49),
    ('XCIX', 99),
    ('CD', 400),
    ('DC', 600),
    ('MCMLXXXV', 1985)
]

english_values = [
    ('four', 4),
    ('fifteen', 15),
    ('nineteen', 19),
    ('forty', 40),
    ('eighty-nine', 89),
    ('one hundred and sixty-three', 163),
    ('six thousand and two', 6002),
    ('seven thousand, nine hundred and twenty-three', 7923),
    ('ten thousand', 10000)
]


class TestRoman(unittest.TestCase):

    def test_convert_to_roman(self):
        for text, num in roman_values:
            actual_output = number_utils.convert_to_roman(num)
            self.assertEqual(text, actual_output)

    def test_convert_from_roman(self):
        for text, num in roman_values:
            # reverse
            actual_output = number_utils.convert_from_roman(text)
            self.assertEqual(num, actual_output)


class TestEnglish(unittest.TestCase):
    def test_convert_to_english(self):
        for text, num in english_values:
            actual_output = number_utils.convert_to_english(num)
            self.assertEqual(text, actual_output)


if __name__ == '__main__':
    unittest.main()
