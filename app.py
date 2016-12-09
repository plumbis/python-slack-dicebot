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


class DicebotException(Exception):
    def __init__(self, value):
        self.value = value
        if debug:
            print(value)

    def __str__(self):
        return str(self.value)


def parse_roll(input_roll_string):
    '''
    Takes in a roll_string from the slack command.
    Expected format is <num_dice>d<die_value>.
    Examples: 1d4, 2d6, 3d8, 99d100

    A valid roll can also include "+<num>" or "-<num>"
    Spaces are allowed on either side of the +/-

    Examples: 4d4 + 2, 2d6+1, 8d12 +11

    Valid numbers are between 1d1 and 99d100

    returns a dict of:
    {"num_dice": int(number_of_dice),
     "die": int(die),
     "modifier": modifier}
    '''
    if not isinstance(input_roll_string, str):
        raise DicebotException("Input not a string, given" + str(input_roll_string))

    # Remove the whitespace
    roll_string = input_roll_string.replace(" ", "")

    # 1d6 is minimum roll string length
    # 100d100+100 is the maximum roll string
    if len(roll_string) < 3 or len(roll_string) > 11:
        raise DicebotException("Roll string too short. Given " + input_roll_string)

    d_position = roll_string.find("d")

    if d_position < 0:
        raise DicebotException("'d' found in incorrect position. Given " + input_roll_string)

    num_dice = roll_string[:d_position]

    # Because I'm not above giving StackOverflow some credit
    # https://stackoverflow.com/questions/27050570/how-would-i-account-for-negative-values-in-python
    try:
        int(num_dice)
    except:
        raise DicebotException("Non digit found in the number of dice provided. Given " + input_roll_string)

    plus_pos = roll_string.find("+")
    minus_pos = roll_string.find("-")

    if plus_pos > 0:  # We have a + modifier
        die_value = roll_string[d_position + 1:plus_pos]
        if len(die_value) == 0:
            raise DicebotException("No dice value provided. Given " + input_roll_string)

        roll_modifier = roll_string[plus_pos + 1:]

    elif minus_pos > 0:  # We have a - modifier
        die_value = roll_string[d_position + 1:minus_pos]
        if len(die_value) == 0:
            raise DicebotException("No dice value provided. Given " + input_roll_string)

        roll_modifier = roll_string[minus_pos:]

    else:  # No modifier exists. Mark it zero dude.
        die_value = roll_string[d_position + 1:]
        if len(die_value) == 0:
            raise DicebotException("No dice value provided. Given " + input_roll_string)

        roll_modifier = "0"

    try:
        int(die_value)
    except:
        raise DicebotException("Non digit found in the dice value. Given " + input_roll_string)

    if int(die_value) <= 0:
        raise DicebotException("Die value can not be 0 or less. Given " + input_roll_string)

    if int(num_dice) <= 0:
        raise DicebotException("Number of dice can not be 0 or less. Given " + input_roll_string)

    # This will accept modifiers like "2-3" (and consider it -1)
    if len(roll_modifier) > 0:
        try:
            int(roll_modifier)
        except:
            raise DicebotException("Invalid roll modifer. Given " + str(input_roll_string))

    return {"num_dice": int(num_dice),
            "die": int(die_value),
            "modifier": int(roll_modifier)}


def generate_roll(roll_dict):
    '''
    Takes in a valid roll string and returns the sum of the roll with modifiers.
    Assumes roll_list is a dict containing:
    {"num_dice": <int>, "die": <int>, "modifier": <int>}

    Returns False if the output is invalid.
    Returns dict containing {"total": <int>, "modifer": <modifer_int>, "rolls": [roll_int]}
    '''

    if not isinstance(roll_dict, dict):
        raise DicebotException("Roll dict is not a dict and can't be cast to string")

    if "num_dice" not in roll_dict or "die" not in roll_dict or "modifier" not in roll_dict:
        raise DicebotException("Missing dictionary key in roll_dict. Passed " + str(roll_dict))

    try:
        num_dice = int(roll_dict["num_dice"])
        die_value = int(roll_dict["die"])
        modifier = int(roll_dict["modifier"])
    except:
        raise DicebotException("Roll dict contains non-numbers. Passed " + str(roll_dict))

    if num_dice <= 0:
        raise DicebotException("Invalid number of dice. Passed " + str(roll_dict))

    if die_value <= 0:
        raise DicebotException("Invalid die value. Passed " + str(roll_dict))

    rolls = []
    for x in range(0, num_dice):
        roll_result = random.randint(1, die_value)
        rolls.append(roll_result)

    return {"total": sum(rolls) + modifier,
            "rolls": rolls,
            "modifier": modifier}


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
        raise DicebotException("Invalid Slack message, no user_name in slack message: " + slack_message)

    if "command" not in slack_message:
        raise DicebotException("No command in slack message: " + slack_message)

    if "text" not in slack_message:
        raise DicebotException("No text in slack message: " + slack_message)

    if "channel_name" not in slack_message:
        raise DicebotException("No channel in slack message: " + slack_message)

    return {"username": slack_message["user_name"],
            "command": slack_message["command"],
            "text": slack_message["text"],
            "channel_name": slack_message["channel_name"]}


def generate_slack_response(text, in_channel=True):
    # if SLACK_WEBHOOK in os.environ:
    #      webhook = os.environ["SLACK_WEBHOOK"]
    #      token = os.environ["SLACK_TOKEN"]

    if in_channel:
        where = "in_channel"
    else:
        where = "ephemeral"
    response = dict()
    response["response_type"] = where
    response["text"] = text
    response["attachments"] = []

    if debug:
        print("Slack Response: " + str(response))

    return jsonify(response)


def format_standard_roll(rolled_dice, username, roll):
    '''
    Takes in a rolled_dice dict, slack username and the original parsed roll
    and returns a string.

    This assumes the output should be for a standard dice roll (not adv or dis).

    Format is
        <username> rolled <num>d<die> (+)<modifier>
        <roll> + <roll> + <roll> (+)<modifier> = <total>

    '''
    try:
        string_number_list = list(map(str, rolled_dice["rolls"]))
    except:
        print(rolled_dice)
        raise DicebotException("format_standard_roll passed values that can't be cast to string")

    output_text = []
    output_text.append(username + " rolled " + roll["num_dice"] + "d" + roll["die"])
    output_text.append("")

    for roll in string_number_list:
        if len(output_text) >= 1:
            output_text.append("+")
        output_text.append(roll)
    if rolled_dice["modifier"] > 0:
        output_text.append("(+" + str(rolled_dice["modifier"]) + ")")
    if rolled_dice["modifier"] < 0:
        output_text.append("(" + str(rolled_dice["modifier"]) + ")")

    output_text.append("=")
    output_text.append("*" + str(rolled_dice["total"]) + "*")
    output_text.append("")


@app.route('/test', methods=["GET", "POST"])
def test_roll():

    if debug:
        print(request.form)

    try:
        slack_dict = parse_slack_message(request.form)
        parsed_roll = parse_roll(slack_dict["text"])
        rolled_dice = generate_roll(parsed_roll)
        output = format_standard_roll(rolled_dice, slack_dict["username"], parsed_roll)
    except DicebotException as dbe:
        return generate_slack_response("error: " + str(dbe))

    return generate_slack_response(output)

'''
def normal_roll():

    slack_dict = parse_slack_message(request.form)
    print(request.form)

    if not slack_dict:
        return jsonify(generate_slack_response("Invalid Slack Message"))

    roll_string = slack_dict["text"]

    if not roll_string:
        return jsonify(generate_slack_response("Invalid Roll. <num>d<side> +/-<modifier>", in_channel=False))

    # {"total": <int>, "modifer": <modifer_int>, "rolls": [roll_int]}
    roll_dict = generate_roll(valid_roll(roll_string))

    if not isinstance(roll_dict, dict):
        if debug:
            print("valid_roll() failed to return a dict. Provided " + str(roll_dict))
        return jsonify(generate_slack_response("Invalid Roll. <num>d<side> +/-<modifier>", in_channel=False))

    if "rolls" not in roll_dict or "modifier" not in roll_dict or "total" not in roll_dict:
        if debug:
            print("Invalid Roll, Given " + str(roll_dict))
        return jsonify(generate_slack_response("Invalid Roll. <num>d<side> +/-<modifier>", in_channel=False))

    string_number_list = list(map(str, roll_dict["rolls"]))
    output_text = []

    for roll in string_number_list:
        if len(output_text) >= 1:
            output_text.append("+")
        output_text.append(roll)
    if roll_dict["modifier"] > 0:
        output_text.append("(+" + str(roll_dict["modifier"]) + ")")
    if roll_dict["modifier"] < 0:
        output_text.append("(" + str(roll_dict["modifier"]) + ")")

    output_text.append("=")
    output_text.append("*" + str(roll_dict["total"]) + "*")
    output_text.append("")

    return jsonify(generate_slack_response(" ".join(output_text)))
'''

if __name__ == "__main__":
    app.run()
