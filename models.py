from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/projects.db'

db = SQLAlchemy(app)

class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    type = db.Column(db.String)
    date_started = db.Column(db.Date)
    date_finished = db.Column(db.Date)
    description = db.Column(db.Text)
    skills = db.Column(db.Text)
    url_to_project = db.Column(db.Text)
