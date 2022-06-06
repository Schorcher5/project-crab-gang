import os
from flask import Flask, render_template, request, session
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
                 education, location, song, platform, filename, title, query,
                 resume):
        self.fname: str = first_name
        self.lname: str = last_name
        self.summary: str = summary
        self.email: str = email
        self.experience: List[str] = work_exp
        self.hobbies: List[str] = hobbies
        self.education: List[str] = education
        self.location: str = location
        self.song: str = song
        self.platform: str = platform
        self.pic_path: str = filename
        self.title: str = title
        self.query: str = query
        self.resume: str = resume


@app.errorhandler(404)
def not_found(e):
    return render_template("error.html", title="Page Not Found", error="Page not found")


@app.route('/')
def index():
    print('current_user' in session)
    return render_template('index.html', title="Homepage")


@app.route('/karl')
def karl():
    first_name = "Karl"
    last_name = "Hernandez"
    summary = "I am a person"
    email = "cjh16@rice.edu"
    experience = "what"
    hobbies = ["Sleep"]
    education = "heck"
    location= ""
    song = ""
    platform = ""
    filename = "signal-2022-05-31-163344_001.jpeg"
    title = first_name + " " + last_name
    places_api = str(os.getenv("GOOGLE_PLACES_API"))
    query = "https://www.google.com/maps/embed/v1/place?key={}&q=place_id:ChIJCSF8lBZEwokRhngABHRcdoI&center=40.6781784,-73.9441579&zoom=5".format(
        places_api)

    resume = "karl.pdf"

    karl = Data(first_name, last_name, summary, email, experience, hobbies,
                education, location, song, platform, filename, title, query,
                resume)

    session['current_user'] = pickle.dumps(karl)
    print('current_user' in session)
    # krl = pickle.loads(session['current_user'])

    return render_template("portfolio.html", **karl.__dict__)


@app.route('/joaquin')
def joaquin():
    first_name = "Joaquin"
    last_name = "Cisneros"
    summary = "I'm a 3rd year computer science major at the University of the Fraser Valley. Aspiring full-stack developer who is always looking to improve themself"
    email = "2014joaquincisneros@gmaill.com"
    work_exp = ["University of the Fraser Valley: Computer Lab Monitor (2021)","Major League Hacking: Production engineer fellow (2022)"]
    hobby = ["Videogames", "Anime", "Leetcoding"]
    education = "University of the Fraser Valley: Bachelor of Science"
    impression = ""
    song = ""
    platform = "https://www.linkedin.com/in/joaquin-cisneros-271256225/"
    filename = "profilePicture.jpg"
    return render_template('portfolio.html', fname=first_name, lname=last_name,
                           summary=summary, experience=work_exp, email=email, hobby=hobby,
                           location=location, education=education, song=song,
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
    title = first_name + " " + last_name

    summary = request.form["summary"].replace('\r\n', '\\n')
    email = request.form["email"]
    experience = request.form["experience"]
    hobbies = [x for x in request.form["hobbies"].split(',')]
    education = request.form["education"]
    location = request.form["location"]

    song = request.form["song"]
    platform = request.form["platform"]

    # pictures are a bit more hard :(
    picture = request.files["picture"]
    filename = secure_filename(picture.filename)  # type: ignore
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    picture.save(path)

    # resumes are a bit more hard :(
    resume = request.files["resume"]
    resume_path = secure_filename(resume.filename)  # type: ignore
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    resume.save(path)

    # google maps stuff
    long = request.form["long"]
    lat = request.form["lat"]
    place_id = request.form["place_id"]
    places_api = str(os.getenv("GOOGLE_PLACES_API"))

    query = "https://www.google.com/maps/embed/v1/place?key={}&q=place_id:{}&center={},{}&zoom=5".format(
        places_api, place_id, lat, long)

    user = Data(first_name, last_name, summary, email, experience, hobbies,
                education, location, song, platform, filename, title, query,
                resume_path)

    session['current_user'] = pickle.dumps(user)

    return render_template("portfolio.html", **user.__dict__)


@app.route('/hobbies')
def hobbies():
    if 'current_user' not in session:
        return render_template("error.html", title="Error", error="User is not in session")
    user = pickle.loads(session['current_user'])
    return render_template("hobbies.html", hobbies=user.hobbies)


if __name__ == "__main__":
    app.run(debug=True)
