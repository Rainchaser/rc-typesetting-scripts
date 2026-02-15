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
import ao3_chapnum_format
from utils import Tag

test_fix_values = [
    ('Chapter','upper', 'CHAPTER '),
    ('chapter   ', 'title', 'Chapter '),
    ('ChApTeR', '', 'ChApTeR '),
    (None, 'upper', ''),
    ('', '', '')
]

test_ornament_values = [
    ('~#~', Tag.H1, True),
    ('**', Tag.H6, True),
    ('', Tag.H1, False),
    (None, Tag.H1, False)
]

test_cnum_values = [
    ('title', 1, [1, 0]),
    ('text', 0, [1, 0]),
    ('text', 2, [1, 2]),
    ('', -4, [5, 0])
]

test_cval_values = [
    ({'text': 'title', 'numbers': 'roman', 'case': 'upper'}, 1, ''),
    ({'text': 'other', 'numbers': 'roman', 'case': 'upper'}, 19, 'XIX'),
    ({'text': 'other', 'numbers': 'roman', 'case': 'lower'}, 4, 'iv'),
    ({'text': 'other', 'numbers': 'roman', 'case': 'title'}, 27, 'XXVII'),
    ({'text': 'other', 'numbers': 'arabic', 'case': 'upper'}, 23, '23'),
    ({'text': 'other', 'numbers': 'other', 'case': 'upper'}, 1, 'ONE'),
    ({'text': 'other', 'numbers': 'other', 'case': 'lower'}, 50, 'fifty'),
    ({'text': 'other', 'numbers': 'other', 'case': 'title'}, 121, 'One Hundred And Twenty-One')
]

test_ctext_values = [
    ('title', 'Chapter 1: I made a mistake', ['', '1', ' '], 'I made a mistake'),
    ('title', 'Chapter 1: I made a mistake', ['# ', '1', ' # '], '# I made a mistake #'),
    ('combined', "Chapter 4: I've got a cat & a dog", ['Chapter ', 'IV', ': '], "Chapter IV: I've got a cat & a dog"),
    ('other', 'Chapter 5: Getting on like a house on fire', [' * ', 'five', ' * '], '* five *'),
    ('other', 'Chapter 6: Peace at last', ['', 'five', ''], 'five')
]

class TestChapNumFormat(unittest.TestCase):
    def test_set_fixes(self):
        for test_text, case, exp_out in test_fix_values:
            actual_output = ao3_chapnum_format.set_fixes(test_text, case)
            self.assertEqual(exp_out, actual_output)

    def test_set_ornament(self):
        for test_text, tag_val, exp_use in test_ornament_values:
            actual_use, html_tag = ao3_chapnum_format.set_ornament(test_text, tag_val)
            self.assertEqual(exp_use, actual_use)
            if exp_use:
                self.assertEqual(html_tag.tag, tag_val)
                self.assertEqual(html_tag.text, test_text)
            else:
                self.assertIsNone(html_tag)

    def test_set_chap_numbers(self):
        for num_format, offset, exp_result in test_cnum_values:
            actual_output = ao3_chapnum_format.set_chap_numbers(num_format, offset)
            self.assertEqual(exp_result[0], actual_output[0])
            self.assertEqual(exp_result[1], actual_output[1])

    def test_get_chapter_val(self):
        for options, value, exp_result in test_cval_values:
            actual_output = ao3_chapnum_format.get_chapter_val(options, value)
            self.assertEqual(exp_result, actual_output)

    def test_get_chapter_text(self):
        for text_type, test_text, test_vals, exp_out in test_ctext_values:
            actual_output = ao3_chapnum_format.get_chapter_text(text_type, test_text, test_vals)
            self.assertEqual(exp_out, actual_output)


if __name__ == '__main__':
    unittest.main()
