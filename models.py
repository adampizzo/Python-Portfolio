from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/projects.db'

db = SQLAlchemy(app)

class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    type = db.Column(db.String)
    skills = db.Column(db.Text)
    description = db.Column(db.Text)
    first_commit = db.Column(db.Date, db.ForeignKey('github_info.first_commit'))
    last_commit = db.Column(db.Date, db.ForeignKey('github_info.last_commit'))
    url_to_project = db.Column(db.Text, db.ForeignKey('github_info.url'))
    num_commits = db.Column(db.Integer, db.ForeignKey('github_info.num_commits'))
    
    first_commit_rel = db.relationship("GithubInfo", backref='fst_com_projects', lazy=True, foreign_keys=[first_commit])
    last_commit_rel = db.relationship("GithubInfo", backref='lst_com_projects', lazy=True, foreign_keys=[last_commit])
    url_to_project_rel = db.relationship("GithubInfo", backref='url_to_projects', lazy=True, foreign_keys=[url_to_project])
    num_commits_rel = db.relationship("GithubInfo", backref='num_commits_projects', lazy=True, foreign_keys=[num_commits])
    
    def __repr__(self):
        return f'Projects(id = {self.id}, title = {self.title}, type = {self.type}, url = {self.url_to_project}, number of commits = {self.num_commits}'

class GithubInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    user_name = db.Column(db.String)
    first_commit = db.Column(db.Date)
    last_commit = db.Column(db.Date)
    url = db.Column(db.Text)
    num_commits = db.Column(db.Integer)
    date_pulled = db.Column(db.Date)
    
    def __repr__(self):
        return f'GithubInfo(id = {self.id}, name = {self.name}, first commit date = {self.first_commit}, last commit date = {self.last_commit}, url = {self.url}, added to DB date = {self.date_pulled})'

class Security(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String)
    date_added = db.Column(db.Date)
    
    def __repr__(self):
        return f'Security(id = {self.id}, token = {self.token}, date_added = {self.date_added})'

if __name__ == '__main__':
    db.create_all()
    print(db.session.query(Projects.title).all())