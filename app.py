from flask import Flask
app = Flask(__name__)


@app.route("/test")
def roll():
    return "Hello World!"


@app.route('/<name>', methods=["GET", "POST"])
def hello_name(name):
    return "Hello {}!".format(name)


if __name__ == "__main__":
    app.run()
