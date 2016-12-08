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

    # {"num_dice": <int>, "die": <int>, "modifier": <int>}

    def test_invalid_inputs(self):
        # Note: list of length 3 with all int or float are valid
        # as they can be cast to int.
        input_list = [{},
                      {"num_dice": "1"},
                      {"num_dice": "1", "die": "1"},
                      {"num_dice": "[1]", "die": "2", "modifier": "3"},
                      {"num_dice": "1", "die": "[2]", "modifier": "3"},
                      {"num_dice": "1", "die": "2", "modifier": "[3]"},
                      {"num_dice": [1], "die": 2, "modifier": 3},
                      {"num_dice": 1, "die": [2], "modifier": 3},
                      {"num_dice": 1, "die": 2, "modifier": [3]},
                      {"num_dice": 1},
                      {"num_dice": 1, "die": 1},
                      {"num_dice": 1.1},
                      {"num_dice": 1, "die": 1.1},
                      {"num_dice": 1.1, "die": 1},
                      {"num_dice": 1.1, "die": 1.1},

                      {"die": 1},
                      {"die": 1, "modifier": 1},
                      {"die": 1.1},
                      {"die": 1, "modifier": 1.1},
                      {"die": 1.1, "modifier": 1},
                      {"die": 1.1, "modifier": 1.1},
                      ]

        result_list = list(map(generate_roll, input_list))

        for result in result_list:
            self.assertFalse(result)

    def test_valid_inputs(self):

        self.assertEqual(generate_roll({"num_dice": 1, "die": 1, "modifier": 0})["total"], 1)
        self.assertEqual(generate_roll({"num_dice": 1, "die": 1, "modifier": -1})["total"], 0)
        self.assertEqual(generate_roll({"num_dice": 1, "die": 1, "modifier": 1})["total"], 2)

        self.assertEqual(generate_roll({"num_dice": 2, "die": 1, "modifier": 0})["total"], 2)
        self.assertEqual(generate_roll({"num_dice": 2, "die": 1, "modifier": -1})["total"], 1)
        self.assertEqual(generate_roll({"num_dice": 2, "die": 1, "modifier": 1})["total"], 3)

        self.assertTrue(2 <= generate_roll({"num_dice": 2, "die": 6, "modifier": 0})["total"] <= 16)
        self.assertTrue(2 <= generate_roll({"num_dice": 2, "die": 6, "modifier": 0})["total"] <= 16)
        self.assertTrue(2 <= generate_roll({"num_dice": 2, "die": 6, "modifier": 0})["total"] <= 16)

        self.assertTrue(3 <= generate_roll({"num_dice": 2, "die": 6, "modifier": 1})["total"] <= 17)
        self.assertTrue(3 <= generate_roll({"num_dice": 2, "die": 6, "modifier": 1})["total"] <= 17)
        self.assertTrue(3 <= generate_roll({"num_dice": 2, "die": 6, "modifier": 1})["total"] <= 17)

        self.assertTrue(1 <= generate_roll({"num_dice": 2, "die": 6, "modifier": -1})["total"] <= 15)
        self.assertTrue(1 <= generate_roll({"num_dice": 2, "die": 6, "modifier": -1})["total"] <= 15)
        self.assertTrue(1 <= generate_roll({"num_dice": 2, "die": 6, "modifier": -1})["total"] <= 15)

        self.assertTrue(3 <= generate_roll({"num_dice": 3, "die": 10, "modifier": 0})["total"] <= 30)
        self.assertTrue(3 <= generate_roll({"num_dice": 3, "die": 10, "modifier": 0})["total"] <= 30)
        self.assertTrue(3 <= generate_roll({"num_dice": 3, "die": 10, "modifier": 0})["total"] <= 30)

        self.assertTrue(4 <= generate_roll({"num_dice": 3, "die": 10, "modifier": 1})["total"] <= 31)
        self.assertTrue(4 <= generate_roll({"num_dice": 3, "die": 10, "modifier": 1})["total"] <= 31)
        self.assertTrue(4 <= generate_roll({"num_dice": 3, "die": 10, "modifier": 1})["total"] <= 31)

        self.assertTrue(2 <= generate_roll({"num_dice": 3, "die": 10, "modifier": -1})["total"] <= 29)
        self.assertTrue(2 <= generate_roll({"num_dice": 3, "die": 10, "modifier": -1})["total"] <= 29)
        self.assertTrue(2 <= generate_roll({"num_dice": 3, "die": 10, "modifier": -1})["total"] <= 29)

        self.assertTrue(3 <= generate_roll({"num_dice": 3, "die": 100, "modifier": 0})["total"] <= 300)
        self.assertTrue(3 <= generate_roll({"num_dice": 3, "die": 100, "modifier": 0})["total"] <= 300)
        self.assertTrue(3 <= generate_roll({"num_dice": 3, "die": 100, "modifier": 0})["total"] <= 300)

        self.assertTrue(4 <= generate_roll({"num_dice": 3, "die": 100, "modifier": 1})["total"] <= 301)
        self.assertTrue(4 <= generate_roll({"num_dice": 3, "die": 100, "modifier": 1})["total"] <= 301)
        self.assertTrue(4 <= generate_roll({"num_dice": 3, "die": 100, "modifier": 1})["total"] <= 301)

        self.assertTrue(2 <= generate_roll({"num_dice": 3, "die": 100, "modifier": -1})["total"] <= 299)
        self.assertTrue(2 <= generate_roll({"num_dice": 3, "die": 100, "modifier": -1})["total"] <= 299)
        self.assertTrue(2 <= generate_roll({"num_dice": 3, "die": 100, "modifier": -1})["total"] <= 299)

        self.assertTrue(4 <= generate_roll({"num_dice": 3, "die": 10, "modifier": +11})["total"] <= 44)
        self.assertTrue(4 <= generate_roll({"num_dice": 3, "die": 10, "modifier": +11})["total"] <= 44)
        self.assertTrue(4 <= generate_roll({"num_dice": 3, "die": 10, "modifier": +11})["total"] <= 44)

        self.assertTrue(0 <= generate_roll({"num_dice": 3, "die": 10, "modifier": -3})["total"] <= 27)
        self.assertTrue(0 <= generate_roll({"num_dice": 3, "die": 10, "modifier": -3})["total"] <= 27)
        self.assertTrue(0 <= generate_roll({"num_dice": 3, "die": 10, "modifier": -3})["total"] <= 27)

        self.assertTrue(-17 <= generate_roll({"num_dice": 3, "die": 10, "modifier": -20})["total"] <= 10)
        self.assertTrue(-17 <= generate_roll({"num_dice": 3, "die": 10, "modifier": -20})["total"] <= 10)
        self.assertTrue(-17 <= generate_roll({"num_dice": 3, "die": 10, "modifier": -20})["total"] <= 10)

if __name__ == '__main__':
    unittest.main()
