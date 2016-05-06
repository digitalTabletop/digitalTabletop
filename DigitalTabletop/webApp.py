import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug import secure_filename


mapDict = {}
UPLOAD_FOLDER = 'static/'
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg"])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    global MAP
    return render_template("grid.html", MAP=mapDict)

@app.route("/dm", methods=["POST","GET"])
def dm():
    if request.method == "POST":
        mapDict["background"] = request.form.get("background")
        mapDict["props"] = {}
        for key in request.form:
            if "prop" in key and "." not in key:
                mapDict["props"][key] = {
                    "sizeX" : request.form.get(key+".size").split(",")[0],
                    "sizeY" : request.form.get(key+".size").split(",")[1],
                    "x"
                }

    files = os.listdir(app.config["UPLOAD_FOLDER"])
    return render_template("dm.html", files=files)

@app.route("/assets", methods=["POST", "GET"])
def assets():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


if __name__ == "__main__":
    app.run(debug=True)
