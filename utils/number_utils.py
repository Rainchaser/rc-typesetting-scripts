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

import logging

from utils import file_utils

logger = logging.getLogger(__name__)

ROMAN_DICT = {
    7 : ('1000','M'),
    6 : ('500','D'),
    5 : ('100', 'C'),
    4 : ('50', 'L'),
    3 : ('10', 'X'),
    2 : ('5', 'V'),
    1 : ('1', 'I')
}

ENGLISH_DICT = {
    1 : 'one',
    2 : 'two',
    3 : 'three',
    4 : 'four',
    5 : 'five',
    6 : 'six',
    7 : 'seven',
    8 : 'eight',
    9 : 'nine',
    10 : 'ten',
    11 : 'eleven',
    12 : 'twelve',
    13 : 'thirteen',
    14 : 'fourteen',
    15 : 'fifteen',
    16 : 'sixteen',
    17 : 'seventeen',
    18 : 'eighteen',
    19 : 'nineteen',
    20 : 'twenty',
    30 : 'thirty',
    40 : 'forty',
    50 : 'fifty',
    60 : 'sixty',
    70 : 'seventy',
    80 : 'eighty',
    90 : 'ninety',
    100 : 'hundred',
    1000 : 'thousand',
}

'''
https://www.nationalarchives.gov.uk/help-with-your-research/reading-old-documents/roman-numerals/
https://www.britannica.com/topic/Roman-numeral
https://en.wikipedia.org/wiki/Roman_numerals

Conventions:
Add large value to following small number
Subtract small value from following large value
Equal sized numbers are added together
A bar called a vinculum placed over a number multiplies its value by 1,000 (not relevant for chapters!)

    IV = 4 (5 - 1)
    VI = 6 (5 + 1)
    XIV = 15 (10 + (5 - 1))
    XCIX = 99 ((100 - 10) + (10 - 1))
    MCMLXXXV = 1985 (1000 + (1000-100) + 50 + 3x10 + 5)
    '''

def convert_to_roman( input_val:int):
    if input_val > 4999:
        logger.error(file_utils.format_message("convert to roman numerals",
                                               "value too large for conversion - vinculum needed"))
        return "ERROR_NUM_TOO_LARGE"

    ones, tens, hundreds, thousands, input_val = get_unit_count(input_val)

    if input_val != 0:
        logger.info(file_utils.format_message("convert to roman numerals",
                                              "value is not an integer, remainder discarded"))

    roman_output = []

    # process the thousands - this doesn't use the same logic as the other values
    add_roman_values(thousands, 7, roman_output)
    # process the hundreds
    process_roman_units(hundreds, 5, roman_output)
    # process the tens
    process_roman_units(tens, 3, roman_output)
    # process the ones
    process_roman_units(ones, 1, roman_output)

    return ''.join(roman_output)


def get_unit_count(input_val:int):
    thousands = divmod(input_val, 1000)
    input_val = thousands[1]
    thousands = thousands[0]

    hundreds = divmod(input_val, 100)
    input_val = hundreds[1]
    hundreds = hundreds[0]

    tens = divmod(input_val, 10)
    input_val = tens[1]
    tens = tens[0]

    ones = divmod(input_val, 1)
    input_val = ones[1]
    ones = ones[0]

    return ones, tens, hundreds, thousands, input_val


def process_roman_units(quantity, position, values:list):
    val = ROMAN_DICT[position][1]
    fiveval = ROMAN_DICT[position + 1][1]
    tenval = ROMAN_DICT[position + 2][1]

    if quantity == 9:
        values.append(val)
        values.append(tenval)
    elif quantity == 4:
        values.append(val)
        values.append(fiveval)
    else:
        if quantity >= 5:
            quantity = quantity - 5
            values.append(fiveval)
        add_roman_values(quantity, position, values)


def add_roman_values(quantity, position, values:list):
    if quantity != 0:
        val = ROMAN_DICT[position][1]
        for _ in range(quantity):
            values.append(val)


def convert_from_roman(input_str:str):
    length = len(input_str)

    total = 0
    skip = False
    position = 0

    while position < length:
        if skip:
            # need to skip as value processed in previous loop, jump to next character
            skip = False
            position += 1
            continue

        value = roman_to_arabic(input_str[position])
        if value == -1:
            logger.error(file_utils.format_message("convert_from_roman", "character is not a valid roman numeral"))
            return -1
        else:
            next_val = 0 if position == length -1 else roman_to_arabic(input_str[position + 1])
            if next_val > value:
                skip = True
                total = total + next_val - value
            else:
                total = total + value
        position += 1
    return total


def roman_to_arabic(input_str:str):
    for x in ROMAN_DICT:
        if ROMAN_DICT[x][1] == input_str:
            return int(ROMAN_DICT[x][0])
    return -1


def convert_to_english(input_val:int):
    if input_val > 10000:
        logger.error(file_utils.format_message("convert to english text",
                                               "method only implemented to 10000 max"))
        return "ERROR_NUM_TOO_LARGE"
    ones, tens, hundreds, thousands, input_val = get_unit_count(input_val)
    output_thousands = ""
    output_hundreds = ""
    output_ones = ""

    if input_val != 0:
        logger.info(file_utils.format_message("convert to english words",
                                              "value is not an integer, remainder discarded"))

    if thousands in ENGLISH_DICT:
        # caps out at 10 so no need to handle the larger values
        output_thousands = ENGLISH_DICT[thousands] + " thousand"

    if hundreds in ENGLISH_DICT:
        output_hundreds = ENGLISH_DICT[hundreds] + " hundred"

    # tens are complicated - need to handle the teens, plus 21, 22, 23 etc
    tens = tens * 10
    sum_val = tens + ones
    if sum_val in ENGLISH_DICT:
        output_ones = ENGLISH_DICT[sum_val]
    elif tens != 0 and ones != 0:
        output_ones = ENGLISH_DICT[tens] + '-' + ENGLISH_DICT[ones]

    final_output = ""
    if output_thousands != "":
        final_output = output_thousands
        if output_hundreds != "":
            final_output = final_output + ", "
        elif output_ones != "":
            final_output = final_output + " and "
    if output_hundreds != "":
        final_output = final_output + output_hundreds
        if output_ones != "":
            final_output = final_output + " and "
    if output_ones != "":
        final_output = final_output + output_ones

    return final_output
