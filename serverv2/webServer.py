from flask import Flask, render_template, redirect, url_for, session, request, abort, make_response
import json

app = Flask(__name__)
app.secret_key = "thisisonlyatest"

USERS = {}
PORT = 5000

@app.route('/', methods=["GET", "POST"])
def index():
    global USERS
    if request.method == "POST":
        resp = make_response(redirect(url_for("grid")))
        resp.set_cookie('uname', request.form.get("uname"))
        USERS[session.get("uname")] = {
            "picture":"archer.png"
            }
        return resp
    return render_template('login.html')


@app.route("/grid")
def grid():
    return render_template("grid.html", host="localhost", port=8080)

@app.route("/user/<name>/avatar")
def user(name):
    try:
        return USERS[name]["picture"]
    except:
        abort(404)


if __name__ == "__main__":
    app.run(debug=True)
