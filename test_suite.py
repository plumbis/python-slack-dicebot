#!/usr/bin/env python3

import unittest
from app import valid_roll, generate_roll
import string


class ValidateRolls(unittest.TestCase):

    string_list = ["1", "2", "3", "10", "11", "20", "21", "30", "31",
                   "40", "49", "90", "99", "100"]

    def test_valid_roll_no_modifer(self):
        '''
        Tests all combinations of 1d1 through 100d100.
        Because whitespace is removed early, 1d6, 1d 6, 1 d6 and 1 d 6 are valid
        '''

        roll_list = []
        for die_value in ValidateRolls.string_list:
            for num_dice in ValidateRolls.string_list:
                roll_list.append(num_dice + "d" + die_value)    # 1d6
                roll_list.append(num_dice + "d " + die_value)   # 1d 6
                roll_list.append(num_dice + " d" + die_value)   # 1 d6
                roll_list.append(num_dice + " d " + die_value)  # 1 d 6

        result_list = list(map(valid_roll, roll_list))

        for result in result_list:
            self.assertIsNot(result, False)

    def test_valid_roll_with_modifer(self):
        '''
        Tests all combinations of 1d1 through 100d100.
        Because whitespace is removed early, 1d6, 1d 6, 1 d6 and 1 d 6 are valid
        '''

        roll_list = []
        for die_value in ValidateRolls.string_list:
            for num_dice in ValidateRolls.string_list:
                for modifier in ValidateRolls.string_list:
                    roll_list.append(num_dice + "d" + die_value + "+" + modifier)    # 1d6+2
                    roll_list.append(num_dice + "d " + die_value + "+" + modifier)   # 1d 6+2
                    roll_list.append(num_dice + " d" + die_value + "+" + modifier)   # 1 d6+2
                    roll_list.append(num_dice + " d " + die_value + "+" + modifier)  # 1 d 6+2

                    roll_list.append(num_dice + "d" + die_value + " +" + modifier)    # 1d6 +2
                    roll_list.append(num_dice + "d " + die_value + " +" + modifier)   # 1d 6 +2
                    roll_list.append(num_dice + " d" + die_value + " +" + modifier)   # 1 d6 +2
                    roll_list.append(num_dice + " d " + die_value + " +" + modifier)  # 1 d 6 +2

                    roll_list.append(num_dice + "d" + die_value + "+ " + modifier)    # 1d6+ 2
                    roll_list.append(num_dice + "d " + die_value + "+ " + modifier)   # 1d 6+ 2
                    roll_list.append(num_dice + " d" + die_value + "+ " + modifier)   # 1 d6+ 2
                    roll_list.append(num_dice + " d " + die_value + "+ " + modifier)  # 1 d 6+ 2

                    roll_list.append(num_dice + "d" + die_value + "-" + modifier)    # 1d6-2
                    roll_list.append(num_dice + "d " + die_value + "-" + modifier)   # 1d 6-2
                    roll_list.append(num_dice + " d" + die_value + "-" + modifier)   # 1 d6-2
                    roll_list.append(num_dice + " d " + die_value + "-" + modifier)  # 1 d 6-2

                    roll_list.append(num_dice + "d" + die_value + " -" + modifier)    # 1d6 -2
                    roll_list.append(num_dice + "d " + die_value + " -" + modifier)   # 1d 6 -2
                    roll_list.append(num_dice + " d" + die_value + " -" + modifier)   # 1 d6 -2
                    roll_list.append(num_dice + " d " + die_value + " -" + modifier)  # 1 d 6 -2

                    roll_list.append(num_dice + "d" + die_value + "- " + modifier)    # 1d6- 2
                    roll_list.append(num_dice + "d " + die_value + "- " + modifier)   # 1d 6- 2
                    roll_list.append(num_dice + " d" + die_value + "- " + modifier)   # 1 d6- 2
                    roll_list.append(num_dice + " d " + die_value + "- " + modifier)  # 1 d 6- 2

        result_list = list(map(valid_roll, roll_list))

        for result in result_list:
            self.assertIsNot(result, False)

    def test_invalid_roll_no_modifier(self):

        roll_list = ["ad6", "aad6", "d6", "1da", "abc",
                     "1daa", "d", "1", "12", "123", "123d",
                     "0d0", "1d0", "0d12", 0, 1, 2, 33.45, 1000, 100]

        result_list = list(map(valid_roll, roll_list))

        for result in result_list:
            self.assertFalse(result)

    def test_invalid_modifiers(self):
        roll_list = []
        modifier_list = ["+-", "-+", "+a", "-a", "0+", "+.", "-.",
                         "+*", "-*", "a", "a0", "a+", "0a", "-a+", "+a-"]

        for die_value in ValidateRolls.string_list:
            for num_dice in ValidateRolls.string_list:
                for modifier in string.punctuation:  # Try all punctuation chars.
                    roll_list.append(num_dice + "d" + die_value + "+" + modifier)    # 1d6+2
                    roll_list.append(num_dice + "d " + die_value + "+" + modifier)   # 1d 6+2
                    roll_list.append(num_dice + " d" + die_value + "+" + modifier)   # 1 d6+2
                    roll_list.append(num_dice + " d " + die_value + "+" + modifier)  # 1 d 6+2

                for modifer in modifier_list:
                    roll_list.append(num_dice + "d" + die_value + "+" + modifier)    # 1d6+2
                    roll_list.append(num_dice + "d " + die_value + "+" + modifier)   # 1d 6+2
                    roll_list.append(num_dice + " d" + die_value + "+" + modifier)   # 1 d6+2
                    roll_list.append(num_dice + " d " + die_value + "+" + modifier)  # 1 d 6+2

        result_list = list(map(valid_roll, roll_list))

        for result in result_list:
            self.assertFalse(result)


class GenerateRolls(unittest.TestCase):

    def test_invalid_inputs(self):
        # Note: list of length 3 with all int or float are valid
        # as they can be cast to int.
        input_list = [[], ["1"], ["1", "1"], ["1", "2", "3", "4"],
                      ["-1", "-1", "-1"], [1], [1, 2], [1, 2, 3, 4],
                      [1.1], [1.1, 2], [1.1, 2, 3, 4],
                      [1, 2.1], [1, 2.1, 3, 4], [1, 2, 3, 4.1]]

        result_list = list(map(generate_roll, input_list))

        for result in result_list:
            self.assertFalse(result)

    def test_valid_inputs(self):
        # input_list = [, [1, 1, -1], [1, 1, 0],
        #               [2, 1, 1], [2, 1, -1], [2, 1, 0]]

        self.assertEqual(generate_roll([1, 1, 0]), 1)
        self.assertEqual(generate_roll([1, 1, -1]), 0)
        self.assertEqual(generate_roll([1, 1, 1]), 2)

        self.assertEqual(generate_roll([2, 1, 0]), 2)
        self.assertEqual(generate_roll([2, 1, -1]), 1)
        self.assertEqual(generate_roll([2, 1, 1]), 3)

        self.assertTrue(2 <= generate_roll([2, 6, 0]) <= 16)
        self.assertTrue(2 <= generate_roll([2, 6, 0]) <= 16)
        self.assertTrue(2 <= generate_roll([2, 6, 0]) <= 16)

        self.assertTrue(3 <= generate_roll([2, 6, 1]) <= 17)
        self.assertTrue(3 <= generate_roll([2, 6, 1]) <= 17)
        self.assertTrue(3 <= generate_roll([2, 6, 1]) <= 17)

        self.assertTrue(1 <= generate_roll([2, 6, -1]) <= 15)
        self.assertTrue(1 <= generate_roll([2, 6, -1]) <= 15)
        self.assertTrue(1 <= generate_roll([2, 6, -1]) <= 15)

        self.assertTrue(3 <= generate_roll([3, 10, 0]) <= 30)
        self.assertTrue(3 <= generate_roll([3, 10, 0]) <= 30)
        self.assertTrue(3 <= generate_roll([3, 10, 0]) <= 30)

        self.assertTrue(4 <= generate_roll([3, 10, 1]) <= 31)
        self.assertTrue(4 <= generate_roll([3, 10, 1]) <= 31)
        self.assertTrue(4 <= generate_roll([3, 10, 1]) <= 31)

        self.assertTrue(2 <= generate_roll([3, 10, -1]) <= 29)
        self.assertTrue(2 <= generate_roll([3, 10, -1]) <= 29)
        self.assertTrue(2 <= generate_roll([3, 10, -1]) <= 29)

        self.assertTrue(3 <= generate_roll([3, 100, 0]) <= 300)
        self.assertTrue(3 <= generate_roll([3, 100, 0]) <= 300)
        self.assertTrue(3 <= generate_roll([3, 100, 0]) <= 300)

        self.assertTrue(4 <= generate_roll([3, 100, 1]) <= 301)
        self.assertTrue(4 <= generate_roll([3, 100, 1]) <= 301)
        self.assertTrue(4 <= generate_roll([3, 100, 1]) <= 301)

        self.assertTrue(2 <= generate_roll([3, 100, -1]) <= 299)
        self.assertTrue(2 <= generate_roll([3, 100, -1]) <= 299)
        self.assertTrue(2 <= generate_roll([3, 100, -1]) <= 299)

        self.assertTrue(4 <= generate_roll([3, 10, +11]) <= 44)
        self.assertTrue(4 <= generate_roll([3, 10, +11]) <= 44)
        self.assertTrue(4 <= generate_roll([3, 10, +11]) <= 44)

        self.assertTrue(0 <= generate_roll([3, 10, -3]) <= 27)
        self.assertTrue(0 <= generate_roll([3, 10, -3]) <= 27)
        self.assertTrue(0 <= generate_roll([3, 10, -3]) <= 27)

        self.assertTrue(-17 <= generate_roll([3, 10, -20]) <= 10)
        self.assertTrue(-17 <= generate_roll([3, 10, -20]) <= 10)
        self.assertTrue(-17 <= generate_roll([3, 10, -20]) <= 10)


if __name__ == '__main__':
    unittest.main()
