import os
from datetime import datetime
from flask import Flask, request, render_template, send_from_directory, redirect, url_for, flash
from main import infer_by_web
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
__author__ = 'Susan'

app = Flask(__name__)
app.secret_key = 'some_secret_key'
APP_ROOT = os.path.dirname(os.path.abspath(__file__)) # project abs path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ratings.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    rating = db.Column(db.Integer)

# create the ratings table
engine = create_engine('sqlite:///ratings.db')


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload_page", methods=["GET"])
def upload_page():
    return render_template("upload.html")


@app.route("/upload", methods=["POST"])
def upload():
    # folder_name = request.form['uploads']
    target = os.path.join(APP_ROOT, 'static/')
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    print(request.files.getlist("file"))
    option = request.form.get('optionsPrediction')
    print("Selected Option:: {}".format(option))
    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        # This is to verify files are supported
        ext = os.path.splitext(filename)[1]
        if (ext == ".jpg") or (ext == ".png"):
            print("File supported moving on...")
        else:
            render_template("Error.html", message="Files uploaded are not supported...")
        savefname = datetime.now().strftime('%Y-%m-%d_%H_%M_%S') + "."+ext
        destination = "/".join([target, savefname])
        print("Accept incoming file:", filename)
        print("Save it to:", destination)
        upload.save(destination)
        result = predict_image(destination, option)
        print("Prediction: ", result)
    # return send_from_directory("images", filename, as_attachment=True)
    return render_template("complete.html", image_name=savefname, result=result)

@app.route('/submit_rating', methods=['POST'])
def submit_rating():
    name = request.form['name']
    rating = request.form['rating']
    print("Name: ",name)
    print("Rating: ",rating)
    rating = Rating(name=name, rating=rating)
    db.session.add(rating)
    db.session.commit()
    flash('Thank you for your rating!')
    # save name and rating to database or do other processing here
    
    
    
    return redirect('/upload_page')

def predict_image(path, type):
    print(path)
    return infer_by_web(path, type)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=4555, debug=True)