#!/usr/bin/env python3
from flask import Flask
from flask import request
import random

app = Flask(__name__)


def valid_roll(input_roll_string):
    '''
    Takes in a roll_string from the slack command.
    Expected format is <num_dice>d<die_value>.
    Examples: 1d4, 2d6, 3d8, 99d100

    A valid roll can also include "+<num>" or "-<num>"
    Spaces are allowed on either side of the +/-

    Examples: 4d4 + 2, 2d6+1, 8d12 +11

    Valid numbers are between 1d1 and 99d100

    If the roll is invalid returns False.
    If the roll is valid, an list of [number_of_dice, die, modifier] is returned
    '''
    if not isinstance(input_roll_string, str):
        print("Input not a string. Given " + str(input_roll_string))
        return False

    roll_string = input_roll_string.replace(" ", "")

    # 1d6 is minimum roll string length
    # 100d100+100 is the maximum roll string
    if len(roll_string) < 3 or len(roll_string) > 11:
        print("Roll string too short. Given " + input_roll_string)
        return False

    d_position = roll_string.find("d")

    if d_position < 0:
        print("'d' found in incorrect position. Given " + input_roll_string)
        return False

    num_dice = roll_string[:d_position]

    for character in num_dice:
        if not character.isdigit():
            print("Non digit found in the number of dice provided. Given " + input_roll_string)
            return False

    plus_pos = roll_string.find("+")
    minus_pos = roll_string.find("-")

    if plus_pos > 0:
        die_value = roll_string[d_position + 1:plus_pos]
        if len(die_value) == 0:
            print("No dice value provided. Given " + input_roll_string)
            return False
        roll_modifier = roll_string[plus_pos + 1:]
    elif minus_pos > 0:
        die_value = roll_string[d_position + 1:minus_pos]
        if len(die_value) == 0:
            print("No dice value provided. Given " + input_roll_string)
            return False
        roll_modifier = roll_string[minus_pos:]
    else:
        die_value = roll_string[d_position + 1:]
        if len(die_value) == 0:
            print("No dice value provided. Given " + input_roll_string)
            return False
        roll_modifier = "0"

    for character in die_value:
        if not character.isdigit():
            print("Non digit found in the dice value. Given " + input_roll_string)
            print(die_value)
            return False

    if int(die_value) <= 0:
        print("Die value can not be 0 or less. Given " + input_roll_string)
        return False

    if int(num_dice) <= 0:
        print("Number of dice can not be 0 or less. Given " + input_roll_string)
        return False

    if len(roll_modifier) > 0:
        first_character = True
        for character in roll_modifier:

            # To make the math easier, we preserve the "-" in a "-2" modifier.
            # This breaks the isdigit() check.
            # To solve, let's allow a "-" in the first position only.
            if character == "-" and first_character:
                if len(roll_modifier) <= 1:
                    print ("Invalid roll modifer. Given " + str(input_roll_string))
                    return False

                first_character = False
                continue
            if not character.isdigit():
                print("Non digit found in the modifier. Given " + input_roll_string)
                return False
            first_character = False

    return [num_dice, die_value, roll_modifier]


def generate_roll(roll_list):
    '''
    Takes in a valid roll string and returns the sum of the roll with modifiers
    '''

    '''
    A big chunk of this code is duplicated from valid_roll().
    They could probably be put into a shared function, but
    I would have to be better at parsing logic
    '''

    if not isinstance(roll_list, list):
        print("Roll list is not a list. Passed " + str(roll_list))

    if not len(roll_list) == 3:
        print("Invalid roll list, passed " + str(roll_list))
        return False

    for num in roll_list:
        # Because I'm not above giving StackOverflow some credit
        # https://stackoverflow.com/questions/27050570/how-would-i-account-for-negative-values-in-python
        try:
            int(num)
        except ValueError:
            print("Roll list contains non-numbers. Passed " + str(roll_list))
            return False

    num_dice = int(roll_list[0])
    die_value = int(roll_list[1])
    modifier = int(roll_list[2])

    if num_dice <= 0:
        print("Invalid number of dice. Passed " + str(roll_list))
        return False
    if die_value <= 0:
        print("Invalid die value. Passed " + str(roll_list))
        return False
    rolls = []

    for x in range(0, num_dice):
        roll_result = random.randint(1, die_value)
        print(("roll: " + str(roll_result)))
        rolls.append(roll_result)

    return sum(rolls) + modifier


@app.route('/test', methods=["GET", "POST"])
def roll():
    if "text" not in request.form:
        return "Error. Expecting 'text' key from slack, received: " + request.form

    slack_message = request.form.get('text')

    roll_list = valid_roll(slack_message)
    if not roll_list:
        print("error")

    roll = generate_roll(roll_list)

    print("complete")

    return roll

if __name__ == "__main__":
    app.run()
