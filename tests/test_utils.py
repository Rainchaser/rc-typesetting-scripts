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
from utils import Punctuation, Tag, XpathPart, Attr


class TestUtils(unittest.TestCase):
    def test_punctuation_enum(self):
        self.assertEqual(3, len(Punctuation.ELLIPSIS.value))

        value = Punctuation.ELLIPSIS.get_canonical_value()
        self.assertEqual('…', value)  # add assertion here
        aliases = Punctuation.ELLIPSIS.get_aliases()
        self.assertEqual(2, len(aliases))
        self.assertEqual('. . .', aliases[0])
        self.assertEqual('...', aliases[1])

        # check new call to ELLIPSIS
        self.assertEqual(3, len(Punctuation.ELLIPSIS.value))

    def test_tag_enum(self):
        value = Tag.PARAGRAPH.value
        self.assertEqual('p', value)  # add assertion here
        value = Tag.PARAGRAPH.get_find_str()
        self.assertEqual('.//p', value)

    def test_xpart_item_val(self):
        value = XpathPart.item_with_val(XpathPart.CLASS.name, Attr.META.value)
        self.assertEqual(value, '[@class="meta"]')

        value = XpathPart.item_with_val(XpathPart.ID.name, Attr.META_GRP.value)
        self.assertEqual(value, '[@id="meta group"]')

        value = XpathPart.item_with_val('bad_val', Attr.META.value)
        self.assertEqual(value, '[@*="meta"]')


if __name__ == '__main__':
    unittest.main()
