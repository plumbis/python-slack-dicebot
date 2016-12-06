from flask import Flask
from flask import request

app = Flask(__name__)


@app.route("/test")
def roll():
    return "Hello World!"


@app.route('/<name>', methods=["GET", "POST"])
def hello_name(name):
    print(request.form)

    return name


if __name__ == "__main__":
    app.run()
