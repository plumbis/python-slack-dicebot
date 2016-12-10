#!/usr/bin/env python3

import unittest
from dicebot import parse_roll, DicebotException
import string


class ParseRollsTest(unittest.TestCase):

    def setUp(self):

        # A list of valid strings
        self.string_list = ["4", "8", "10", "12", "20", "100"]

        # A list of valid rolls without modifiers. Like 1d6
        self.valid_no_modifier = []

        # A list of valid rolls with modifiers. Like 2d8 +2
        self.valid_modifier = []

        # A list of invalid rolls with modifiers. Like 1d8 +b
        self.invalid_with_modifier = []

        # A list of invalid roll inputs.
        self.invalid_no_modifier = ["ad6", "aad6", "d6", "1da", "abc", "", [], {},
                                    "1daa", "d", "1", "12", "123", "123d",
                                    "0d0", "1d0", "0d12", 0, 1, 2, 33.45, 1000, 100]

        # A list of valid modifier values
        self.valid_modifier_list = ["2", "-2", "-1", "2-3", "3", "3-2", "11", "100", "0"]

        # this list is all strings, as the input passed in is a single string.
        # detecting non-strings would be in `invalid_no_modifier` list.
        self.invalid_modifier_list = ["+-", "-+", "+a", "-a", "0+", "+.", "-.",
                                      "+*", "-*", "a", "a0", "a+", "0a", "-a+", "+a-"]
        self.invalid_modifier_list.append(string.punctuation)

        for x in range(4):
            # List of valid rolls without modifiers
            for die_value in self.string_list:
                for num_dice in self.string_list:
                    output = [num_dice, "d", die_value]
                    output.insert(x - 1, " ")
                    self.valid_no_modifier.append("".join(output))

            # List of valid rolls with modifiers
            for die_value in self.string_list:
                for num_dice in self.string_list:
                    for modifier in self.string_list:
                        output = [num_dice, "d", die_value, "+", modifier]
                        output = [num_dice, "d", die_value, "-", modifier]
                        output.insert(x - 1, " ")
                        self.valid_modifier.append("".join(output))

        # List of valid rolls with invalid modifiers
        for valid_value in self.valid_no_modifier:
            for invalid_value in self.invalid_modifier_list:
                self.invalid_with_modifier.append(valid_value + "+" + invalid_value)
                self.invalid_with_modifier.append(valid_value + "-" + invalid_value)

    def test_valid_input(self):

        result_list = list(map(parse_roll, self.valid_no_modifier))
        result_list.append(list(map(parse_roll, self.valid_modifier)))

        for result in result_list:
            self.assertIsNot(result, False)

    def test_invalid_input(self):
        for value in self.invalid_no_modifier:
            with self.assertRaises(DicebotException, msg=value):
                parse_roll(value)

        for value in self.invalid_with_modifier:
            with self.assertRaises(DicebotException, msg=value):
                parse_roll(value)


if __name__ == '__main__':
    unittest.main()
