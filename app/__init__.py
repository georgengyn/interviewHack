from flask import Flask

app = Flask(__name__)

@app.route("/")
def welcome():
    return "<p>Hello, World</p>"

if __name__ == '__main__':
    app.run()