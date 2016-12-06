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

    Returns True or False if the roll is valid
    '''

    roll_string = input_roll_string.replace(" ", "")

    # 1d6 is minimum roll string length
    # 100d100+100 is the maximum roll string
    if len(roll_string) < 3 or len(roll_string) > 9:
        return False

    d_position = roll_string.find("d")

    if d_position < 0:
        return False

    num_dice = roll_string[:d_position]

    for character in num_dice:
        if not character.isdigit():
            return False

    plus_pos = roll_string.find("+")
    minus_pos = roll_string.find("-")

    if plus_pos > 0:
        die_value = roll_string[d_position + 1:plus_pos]
        roll_modifier = roll_string[plus_pos + 1:]
    elif minus_pos > 0:
        die_value = roll_string[d_position + 1:minus_pos]
        roll_modifier = roll_string[minus_pos:]
    else:
        die_value = roll_string[d_position:]

    for character in die_value:
        if not character.isdigit():
            return False

    if len(roll_modifier) > 0:
        for character in roll_modifier:
            if not character.isdigit():
                return False

    return True


def generate_roll(roll_string):
    '''
    Takes in a valid roll string and returns the sum of the roll with modifiers
    '''

    '''
    A big chunk of this code is duplicated from valid_roll().
    They could probably be put into a shared function, but
    I would have to be better at parsing logic
    '''

    d_position = roll_string.find("d")

    num_dice = roll_string[:d_position]

    for character in num_dice:
        if not character.isdigit():
            return False

    plus_pos = roll_string.find("+")
    minus_pos = roll_string.find("-")

    if plus_pos > 0:
        die_value = roll_string[d_position + 1:plus_pos]
        roll_modifier = roll_string[plus_pos + 1:]
    elif minus_pos > 0:
        die_value = roll_string[d_position + 1:minus_pos]
        roll_modifier = roll_string[minus_pos:]
    else:
        die_value = roll_string[d_position:]
        roll_modifier = 0

    rolls = []
    for x in range(0, num_dice):
        rolls.append(random.randint(1, die_value))

    return sum(rolls) + roll_modifier


@app.route('/test', methods=["GET", "POST"])
def roll():
    if "text" not in request.form:
        return "Error. Expecting 'text' key from slack, received: " + request.form

    slack_message = request.form.get('text')

    if not valid_roll(slack_message):
        return "error"

    return generate_roll(slack_message)

    return "blah"


if __name__ == "__main__":
    app.run()
