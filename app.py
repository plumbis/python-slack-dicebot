#!/usr/bin/env python3
from flask import Flask
from flask import request
from flask import jsonify
import random
import os

app = Flask(__name__)

debug = True
SLACK_WEBHOOK = None
SLACK_TOKEN = None


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

    # Slack returns unicode messages. tests are likely strings.
    # Let's do this the dumb and easy way.
    try:
        str(input_roll_string)
    except ValueError:
        if debug:
            print type(input_roll_string)
            print("Input not a string. Given " + str(input_roll_string))
        return False

    roll_string = input_roll_string.replace(" ", "")

    # 1d6 is minimum roll string length
    # 100d100+100 is the maximum roll string
    if len(roll_string) < 3 or len(roll_string) > 11:
        if debug:
            print("Roll string too short. Given " + input_roll_string)
        return False

    d_position = roll_string.find("d")

    if d_position < 0:
        if debug:
            print("'d' found in incorrect position. Given " + input_roll_string)
        return False

    num_dice = roll_string[:d_position]

    for character in num_dice:
        if not character.isdigit():
            if debug:
                print("Non digit found in the number of dice provided. Given " + input_roll_string)
            return False

    plus_pos = roll_string.find("+")
    minus_pos = roll_string.find("-")

    if plus_pos > 0:
        die_value = roll_string[d_position + 1:plus_pos]
        if len(die_value) == 0:
            if debug:
                print("No dice value provided. Given " + input_roll_string)
            return False
        roll_modifier = roll_string[plus_pos + 1:]
    elif minus_pos > 0:
        die_value = roll_string[d_position + 1:minus_pos]
        if len(die_value) == 0:
            if debug:
                print("No dice value provided. Given " + input_roll_string)
            return False
        roll_modifier = roll_string[minus_pos:]
    else:
        die_value = roll_string[d_position + 1:]
        if len(die_value) == 0:
            if debug:
                print("No dice value provided. Given " + input_roll_string)
            return False
        roll_modifier = "0"

    for character in die_value:
        if not character.isdigit():
            if debug:
                print("Non digit found in the dice value. Given " + input_roll_string)
            return False

    if int(die_value) <= 0:
        if debug:
            print("Die value can not be 0 or less. Given " + input_roll_string)
        return False

    if int(num_dice) <= 0:
        if debug:
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
                    if debug:
                        print ("Invalid roll modifer. Given " + str(input_roll_string))
                    return False

                first_character = False
                continue
            if not character.isdigit():
                if debug:
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
        if debug:
            print("Roll list is not a list. Passed " + str(roll_list))
        return False

    if not len(roll_list) == 3:
        if debug:
            print("Invalid roll list, passed " + str(roll_list))
        return False

    for num in roll_list:
        # Because I'm not above giving StackOverflow some credit
        # https://stackoverflow.com/questions/27050570/how-would-i-account-for-negative-values-in-python
        try:
            int(num)
        except ValueError:
            if debug:
                print("Roll list contains non-numbers. Passed " + str(roll_list))
            return False

    num_dice = int(roll_list[0])
    die_value = int(roll_list[1])
    modifier = int(roll_list[2])

    if num_dice <= 0:
        if debug:
            print("Invalid number of dice. Passed " + str(roll_list))
        return False
    if die_value <= 0:
        if debug:
            print("Invalid die value. Passed " + str(roll_list))
        return False
    rolls = []

    for x in range(0, num_dice):
        roll_result = random.randint(1, die_value)
        if debug:
            print(("roll: " + str(roll_result)))
        rolls.append(roll_result)

    return sum(rolls) + modifier


def parse_slack_message(slack_message):
    '''
    Slack POST messages send JSON that looks like the following:
    {"token": "uto4ItLoT82ceQoBpIvgtzzz",
              "team_id": "T0C3TFAGL",
              "team_domain": "my_team_name",
              "channel_id": "D0C3VQDAS",
              "channel_name": "directmessage",
              "user_id": "U0C3TFAQ4",
              "user_name": "my_username",
              "command": "/weather",
              "text": "2d6",
              "response_url": "https://hooks.slack.com/commands/T0C3TFAGL/112373954929/8k4mT8sMpIRdslA0IOMKvWSS"}
    '''

    if "user_name" not in slack_message:
        if debug:
            print("No user_name field in slack message: " + slack_message)
        return False

    if "command" not in slack_message:
        if debug:
            print("No command in slack message: " + slack_message)
        return False

    if "text" not in slack_message:
        if debug:
            print("No text in slack message: " + slack_message)
        return False

    if "channel_name" not in slack_message:
        if debug:
            print("No channel in slack message: " + slack_message)
        return False

    return {"user_name": slack_message["user_name"],
            "command": slack_message["command"],
            "text": slack_message["text"],
            "channel_name": slack_message["channel_name"]}


def generate_slack_response(text):
    # if SLACK_WEBHOOK in os.environ:
    #      webhook = os.environ["SLACK_WEBHOOK"]
    #      token = os.environ["SLACK_TOKEN"]

    response = dict()
    response["response_type"] = "in_channel"
    response["text"] = text
    response["attachments"] = []

    if debug:
        print("Slack Response: " + str(response))

    return response


@app.route('/test', methods=["GET", "POST"])
def roll():

    slack_dict = parse_slack_message(request.form)
    print request.form

    if not slack_dict:
        jsonify(generate_slack_response("Invalid Slack Message"))

    roll_list = valid_roll(slack_dict["text"])

    if not roll_list:
        jsonify(generate_slack_response("Invalid Roll"))

    roll = generate_roll(roll_list)

    print("Final Roll: " + str(roll))

    return jsonify(generate_slack_response(roll))


if __name__ == "__main__":
    app.run()
