from logging import debug
from flask import Flask, render_template,redirect,url_for

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template('main.html')

@app.route("/join")
def join():
    return render_template('join.html')

if __name__ == "__main__":
    app.run(debug=True)