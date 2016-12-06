# from flask import Flask
# app = Flask(__name__)

# @app.route("/test")
# def roll():
#     return "Hello World!"

# @app.route('/<name>')
# def hello_name(name):
#     return "Hello {}!".format(name)

# if __name__ == "__main__":
#     app.run()

from flask_slack import Slack

slack = Slack(app)

@slack.command('test', token="not_required", methods=['POST'])

def your_method(**kwargs):
    text = kwargs.get('text')
    return slack.response(text)
