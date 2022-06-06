import os
from flask import Flask, render_template, request, session
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from os import urandom
from typing import List
from google_images_search import GoogleImagesSearch
import pickle

config = load_dotenv("example.env")
UPLOAD_FOLDER = "./app/static/img/"
app = Flask(__name__)
app.secret_key = urandom(32)  # random 32 bit key
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
gis = GoogleImagesSearch(os.getenv("GOOGLE_PLACES_API"), '5415378a637e6f6e0')


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
        self.resume_path: str = resume


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
    summary = "I am a Mathematics and Linguistics major at Rice University hoping to go to grad school. Currently very interested in CS Theory!"
    email = "cjh16@rice.edu"
    experience = ["Rice Lambda Group", "Rice Linux Group", "Open Source Experience", "StuyvesantCCC"]
    hobbies = ["Reading", "Cooking", "Coding", "Mathematical Problem Solving", "Sleeping"]
    education = ["Rice University", "Stuyvesant High School"]
    location = ""
    song = ""
    platform = "https://github.com/KarlWithK/"
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
    experience = ["University of the Fraser Valley: Computer Lab Monitor (2021)","Major League Hacking: Production engineer fellow (2022)"]
    hobbies = ["Videogames", "Anime", "Leetcoding"]
    education = ["University of the Fraser Valley: Bachelor of Science"]
    location = ""
    song = ""
    platform = "https://www.linkedin.com/in/joaquin-cisneros-271256225/"
    filename = "profilePicture.jpg"
    title = first_name + " " + last_name

    places_api = str(os.getenv("GOOGLE_PLACES_API"))
    query = "https://www.google.com/maps/embed/v1/place?key={}&q=place_id:ChIJg7dqcMY1hFQRYAV7KhU1AQU&center=49.0504377,-122.3044697&zoom=5".format(
        places_api)

    resume = "JoaquinCisnerosResume.pdf"

    joaquin = Data(first_name, last_name, summary, email, experience, hobbies,
                education, location, song, platform, filename, title, query,
                resume)

    session['current_user'] = pickle.dumps(joaquin)


    return render_template('portfolio.html', **joaquin.__dict__)



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
    experience = [x for x in request.form["experience"].split(',')]
    hobbies = [x for x in request.form["hobbies"].split(',')]
    education = [x for x in request.form["education"].split(',')]
    location = request.form["location"]

    song = request.form["song"]
    platform = request.form["platform"]

    # pictures are a bit more hard :(
    picture = request.files["picture"]
    filename = secure_filename(picture.filename)  # type: ignore
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    print(path)
    picture.save(path)

    # resumes are a bit more hard :(
    resume = request.files["resume"]
    resume_path = secure_filename(resume.filename)  # type: ignore
    path = os.path.join(app.config['UPLOAD_FOLDER'], resume_path)
    print(path)
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

    hobbies = {}
    for hobby in user.hobbies:
        gis.search(search_params={'q': hobby})
        for image in gis.results():
            hobbies[hobby] = str(image.url)


    return render_template("hobbies.html", hobbies=hobbies)


if __name__ == "__main__":
    app.run(debug=True)
