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

from utils import html_utils, Tag, XpathPart

class TestHtmlUtils(unittest.TestCase):
    def test_make_xpath(self):
        path_list = [XpathPart.ALL_REL_TO_NODE.value, Tag.BOLD.value]
        value = html_utils.make_xpath(path_list)
        self.assertEqual('.//b', value)

        path_list = [XpathPart.SINGLE_REL_PATH.value, Tag.HEAD.value, Tag.TITLE.value]
        value = html_utils.make_xpath(path_list)
        self.assertEqual('./head/title', value)

        path_list = [XpathPart.SINGLE_PATH_FROM_ROOT.value, Tag.HEAD.value, Tag.TITLE.value]
        value = html_utils.make_xpath(path_list)
        self.assertEqual('/head/title', value)

        path_list = [XpathPart.ALL_FROM_ROOT.value,
                     Tag.DIV.value + XpathPart.cls_with_val('meta'),
                     Tag.DIV.value + XpathPart.cls_with_val('byline')]
        value = html_utils.make_xpath(path_list)
        self.assertEqual('//div[@class="meta"]/div[@class="byline"]', value)

        path_list = [XpathPart.ALL_FROM_ROOT.value,
                     Tag.PARAGRAPH.value + XpathPart.cls_with_val('message')]
        value = html_utils.make_xpath(path_list)
        self.assertEqual('//p[@class="message"]', value)

        path_list = [XpathPart.ALL_FROM_ROOT.value,
                     Tag.DIV.value + XpathPart.id_with_val('chapters'),
                     Tag.DIV.value + XpathPart.cls_with_val('meta group')]
        group1 = html_utils.make_xpath(path_list)
        path_list = [XpathPart.ALL_FROM_ROOT.value,
                     Tag.DIV.value + XpathPart.id_with_val('chapters'),
                     Tag.DIV.value + XpathPart.cls_with_val('meta')]
        group2 = html_utils.make_xpath(path_list)
        value = group1 + XpathPart.GROUP_SEPARATOR.value + group2
        self.assertEqual('//div[@id="chapters"]/div[@class="meta group"]|//div[@id="chapters"]/div[@class="meta"]',
                         value)



if __name__ == '__main__':
    unittest.main()
