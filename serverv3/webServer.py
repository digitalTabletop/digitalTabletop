from flask import Flask, render_template, redirect, url_for, session, request, abort, make_response
import json
import os

app = Flask(__name__)

USERS = {}
PORT = 5000

@app.route('/', methods=["GET", "POST"])
def index():
    global USERS

    # Get all images in avatars
    avatar_options = os.listdir("static/avatars")    

    if request.method == "POST": # if form submitted, do this
        resp = make_response(redirect(url_for("grid")))
        resp.set_cookie('uname', request.form.get("uname"))
        USERS[request.form.get("uname")] = {
            "avatar":"archer.png"
            }
        print(USERS)
        return resp

    return render_template('login.html')


@app.route("/grid")
def grid():
    return render_template("grid.html", host="localhost", port=8080)

@app.route("/user/<name>/avatar")
def user(name):
    try:
        return USERS[name]["avatar"]
    except:
        abort(404)


if __name__ == "__main__":
    app.run(debug=True)
