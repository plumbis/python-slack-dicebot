# Dicebot - The Slack Slash Command Dice Roller
This is a slack slash command dicebot written entirely in Python.

The original idea came from https://github.com/jsprodotcom/getting-started-with-slack-bots

## Commands
Dicebot has four options:
 - `/roll`. Roll takes in a d20 style dice notation with any modifiers. For example `/roll 3d6 +3` or `/roll 1d100` or `/roll 4d8 -2`
 - `/adv`. Adv will roll 2d20 and return the higest value. Adv will apply any modifiers. `/adv +1` or `/adv -2`
 - `/dis`. Dis is the opposite of `/adv`. Dis will roll 2d20 and return the lowest value. Dis also applies any modifiers. For example, `/dis -1` or `/dis +4`
 - '/character'. Character rolls 4d6 and drops the lowest value. This is done 6 times. Character does not take any inputs or modifiers and will ignore any that are passed.

 ## Files
 `.slugignore` is used to tell Heroku to not copy files to Heroku when the app is deployed. Only `dicebot.py` is needed to run this application.
 `app.json` allows for the "Deploy to Heroku" button.
 `dicebot.py` is the dice rolling application that can take input from and return messages to Slack.
 `LICENSE.md` is the MIT License this software is licensed under.
 `Procfile` tells Heroku to launch this application with the [Gunicorn](http://gunicorn.org/) webserver front end.
 `requirements.txt` defines the python runtime to use on Heroku.
 `test_suite.py` is the set of python unittests for this software.

 ## Deploying to Heroku
 [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/plumbis/python-slack-dicebot)

The button is the easiest way. If you wish to deploy manually, create a new application and use the `heroku cli` instructions to clone this project or connect it directly to github.

### Heroku Free Tier
If you deploy on the Heroku free tier the instance will go to sleep when not in use. The first time you use dicebot after it is put in hibernation the command will timeout. Be patient and the app will restart within a minute and work normal after that. Only if you continue to receive timeout errors after 1-2 minutes should you consider something broken.

## Configuring the Application
Nothing needs to be done to configure dicebot. By default it is insecure and the unique slack token is not validated. If you wish to validate the slack token, please edit `parse_slack_message()` within `dicebot.py`.

No webhook configuration is required, as the message is sent back to Slack on the original inbound slash command.

## Configuring Slack.
To configure slack a slash command must be configured for each option (`roll`, `adv`, `dis`, `character`). Within the slash command configuration use the following settings
*Command:* - this is the name of the slash command to use, for example `/roll`
*URL:* - this is the name of your heroku instance URL and the slash command. Most likely something along the lines of "https://fluffy-bunny.herokuap.com/roll",
*Method* - POST
*Token* - Unused. For security you can use this token in the `dicebot.py` application.
*Customize Name` - This is the name that will appear when dicebot responds in slack. May I suggest "Dicebot"

## Background on The Code
Dictionaries are passed around to make accessing the data returned from each function easier.

The way Slack works, the `return` value of the entry point must be JSON formatted and is the only thing sent to slack. Failure to send data or incorrectly formatted data will end in an HTTP 500 error in Slack.

To simplify error handling across the code, everything is done with exceptions. If an input error is found within a function an exception is raised and an error message can be passed back to Slack.

Any `print()` statement is written directly to the Heroku logs. Setting the global `debug = True` setting to `debug = False` will reduce the amount of logging in Heroku.

### New Commands
If you wish to create a new command, follow these steps:

First, define the inbound slash command to be used and a function it is tied to. (These are [Flask](flask.pocoo.org) things)
```python
@app.route('/new_command', methods=["GET", "POST"])
def new_command_function():```

Built a try and except block. `DicebotExceptions` are known errors or conditions. The `except` case is for unexpected failures.
```python

    try:
        #
        # WHERE THE NEW CODE WILL GO
        #
    except DicebotException as dbe:
        return generate_slack_response("error: " + str(dbe) + "\n Please use /adv (+/-)<num>", in_channel=False)
    except:
        print("Unhandled traceback in /adv")
        print(traceback.format_exc())
        return generate_slack_response("Hmm....something went wrong. Try again?", in_channel=False)
```

Most commands will take in an input, do some dice related stuff, format the output and pass it back to the user.

First `parse_slack_message(request.form)` will make the inbound slack message easier to work with.
Next, see if the input matches a "4d6 +2" style with `parse_roll`
With valid input, use `generate_roll` to roll 4x 6 sided dice and add 2 at the end.
Now a custom output function, similar to `format_standard_roll` needs to be created to handle what's special about this roll type
And then take that output string and send it to `generate_slack_response` to get a valid JSON output. If you do not want to show the world the answer use `generate_slack_response(in_channel=False)`
