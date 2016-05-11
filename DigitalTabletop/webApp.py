import os
import json
from flask import Flask, render_template, request, redirect, url_for
from werkzeug import secure_filename


mapDict = {"size":[2, 2]} # Default map size is 2x2
UPLOAD_FOLDER = 'static/' # this means that all files uploaded will be accessable at /static/<filename>
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg"]) # Allowed image extensions for stuff and things


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename): # return true if file is of allowed type
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("grid.html", MAP=mapDict) # Return the grid software thing

@app.route("/dm", methods=["POST","GET"]) # map configuration
def dm():
    global mapDict # allow local mapDict varialbe to influence global one.
    if request.method == "POST": # if its a post request, process form
        if request.form.get("background") != "": # incase background is not defined
            mapDict["background"] = request.form.get("background")
        if request.form.get("size") != "": # incase size is not defined
            mapDict["size"] = request.form.get("size").split(",")
        mapDict["props"] = {}

        pn = 1 # this is the prop number
        try: # incase props arent defined
            for key in request.form.keys():
                if "prop"+str(pn) == key:
                    mapDict["props"][key] = {
                        "image" : request.form.get(key+".image"),
                        "sizeX" : request.form.get(key+".size").split(",")[0],
                        "sizeY" : request.form.get(key+".size").split(",")[1],
                        "x": request.form.get(key+".position").split(",")[0],
                        "y": request.form.get(key+".position").split(",")[1]
                    }
                    pn+=1 # update the iterator i to make sure that the prop number is correct
        except IndexError: # if there is not a correctly defined prop, ignore the error
            pass

    files = os.listdir(app.config["UPLOAD_FOLDER"]) # Show all images...
    return render_template("dm.html", files=files)

@app.route("/assets", methods=["POST", "GET"]) # Upload new files
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
