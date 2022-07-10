FROM python:3.9-slim-buster

WORKDIR /myportfolio

COPY requirements.txt .

RUN pip3 install -r requirements.txt && pip3 install google_images_search

COPY . .

CMD ["flask", "run", "--host=0.0.0.0"]

EXPOSE 5000
