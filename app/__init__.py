import os
from flask import Flask, render_template, request
from flask import url_for, redirect
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from os import urandom

load_dotenv()
UPLOAD_FOLDER = "./app/static/img/"
app = Flask(__name__)
app.secret_key = urandom(32)  # random 32 bit key
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.errorhandler(404)
def not_found(e):
    return render_template("error.html", title="Page Not Found", url=os.getenv("URL"))


@app.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"))


@app.route('/portfolio', methods=["POST"])
def portfolio():
    first_name = request.form["fname"]
    last_name = request.form["lname"]
    summary = request.form["summary"]
    email = request.form["email"]
    work_exp = request.form["experience"]
    hobby = request.form["hobby"]
    education = request.form["education"]
    impression = request.form["impression"]
    song = request.form["song"]
    platform = request.form["platform"]

    # pictures are a bit more hard :(
    picture = request.files["picture"]
    filename = secure_filename(picture.filename)  # type: ignore
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    picture.save(path)

    title = first_name + " " + last_name

    return render_template('portfolio.html', fname=first_name, lname=last_name,
                           summary=summary, experience=work_exp, email=email, hobby=hobby,
                           impression=impression, education=education, song=song,
                           platform=platform, pic_path=filename, title=title)


if __name__ == "__main__":
    app.run(debug=True)
