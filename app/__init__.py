import os
from flask import Flask, render_template, request, session
from flask import url_for, redirect
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from os import urandom
from typing import List
import pickle

config = load_dotenv("example.env")
UPLOAD_FOLDER = "./app/static/img/"
app = Flask(__name__)
app.secret_key = urandom(32)  # random 32 bit key
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


class Data():
    def __init__(self, first_name, last_name, summary, email, work_exp, hobbies,
            education, impression, song, platform, filename, title):
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.summary: str = summary
        self.email: str = email
        self.work_exp: List[str] = work_exp
        self.hobby: List[str] = hobbies
        self.education: List[str] = education
        self.impression: str = impression
        self.song: str = song
        self.platform: str = platform
        self.filename: str = filename
        self.title: str = title


@app.errorhandler(404)
def not_found(e):
    return render_template("error.html", title="Page Not Found", url=os.getenv("URL"))


@app.route('/')
def index():
    return render_template('index.html', title="Homepage")

@app.route('/karl')
def karl():
    first_name = "Karl"
    last_name = "Hernandez"
    summary = ""
    email = "cjh16@rice.edu"
    work_exp = []
    hobbies = []
    education = []
    impression = ""
    song = ""
    platform = ""
    filename = "signal-2022-05-31-163344_001.jpeg"
    title = first_name + " " + last_name
    karl = Data(first_name, last_name, summary, email, work_exp, hobbies, education, impression, song, platform, filename, title)
    pickled_karl = pickle.dumps(karl)
    session['current_user'] = pickled_karl
    krl = pickle.loads(session['current_user'])

    return render_template('portfolio.html', fname=first_name, lname=last_name,
                           summary=summary, experience="", email=email,
                           hobby="none",
                           impression=impression, education="", song=song,
                           platform=platform, title="Karl Hernandez",
                           pic_path=filename)

@app.route('/joaquin')
def joaquin():
    first_name = "Karl"
    last_name = "Hernandez"
    summary = ""
    email = "cjh16@rice.edu"
    work_exp = ""
    hobby = ""
    education = ""
    impression = ""
    song = ""
    platform = ""
    filename = ""
    return render_template('portfolio.html', fname=first_name, lname=last_name,
                           summary=summary, experience=work_exp, email=email, hobby=hobby,
                           impression=impression, education=education, song=song,
                           platform=platform, title="Karl Hernandez",
                           pic_path=filename)

@app.route('/form')
def form():
    places_api = os.getenv("GOOGLE_PLACES_API")
    return render_template('form.html', title="Create Your Own Portfolio",
            places_api=places_api)

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

    summary = summary.replace('\r\n', '\\n')

    long = request.form["long"]
    lat = request.form["lat"]
    place_id = request.form["place_id"]
    places_api = str(os.getenv("GOOGLE_PLACES_API"))

    query = "https://www.google.com/maps/embed/v1/place?key={}&q=place_id:{}&center={},{}&zoom=5".format(places_api, place_id, lat, long)

    return render_template('portfolio.html', fname=first_name, lname=last_name,
                           summary=summary, experience=work_exp, email=email, hobby=hobby,
                           impression=impression, education=education, song=song,
                           platform=platform, pic_path=filename, title=title,
                           query=query)


@app.route('/hobbies')
def hobby():
    return "hobbyies"


if __name__ == "__main__":
    app.run(debug=True)
