from flask import (redirect, render_template, url_for, request)
from models import GithubInfo, db, app, Projects
import datetime
from utils import clean_time


project_df = Projects.query.order_by(Projects.last_commit.desc()).all()  # All projects sorted by date finished.
print(project_df)
# Routes

# Index - Root Page
@app.route('/')
def index():
    skill_set = set()
    projects = Projects.query.all()
    for skill in projects:
        skill = skill.skills.split(',')
        for item in skill:
            skill_set.add(item)
    skill_set = sorted(skill_set)
    return render_template('index.html', skill_set=skill_set, project_df=project_df)


# About Me 
@app.route('/about')
def about():
    return render_template('about.html', project_df=project_df)

# projects/new - Create Route
@app.route('/projects/new', methods=['GET', 'POST'])
def create_project():
    if request.form:
        print(request.form)
        git_proj = GithubInfo.query.filter(GithubInfo.url==request.form['github']).first()
        new_project = Projects(title = request.form['title'], type = request.form['type'],
                            first_commit = git_proj.first_commit, last_commit = git_proj.last_commit,
                            description = request.form['description'], skills = request.form['skills'], 
                            url_to_project = request.form['github'], num_commits = git_proj.num_commits)
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('projectform.html', project_df=project_df)


# projects/<id> - Detail Route (View)
@app.route('/projects/<id>')
def project_detail(id):
    project = Projects.query.get_or_404(id)
    project.skills = project.skills.split(',')

    
    return render_template('detail.html', project=project, project_df=project_df)


# projecst/<id>/edit - Edit/Update Route
@app.route('/projects/<id>/edit', methods=['GET', 'POST'])
def edit_project(id):
    project = Projects.query.get_or_404(id)
    
    if request.form:
        project.title = request.form['title']
        project.type = request.form['type']
        project.first_commit = clean_time(request.form['date_started'])
        project.last_commit = clean_time(request.form['date_finished'])
        project.description = request.form['description']
        project.skills = request.form['skills']
        project.url_to_project = request.form['github']
        db.session.commit()
        return redirect(url_for('project_detail', id=project.id))
    return render_template('projectform_edit.html', project=project, project_df=project_df)

# projects/<id>/delete - Delete Route
@app.route('/projects/<id>/delete')
def delete_project(id):
    pass


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, port=8000, host='localhost')