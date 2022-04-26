from flask import (redirect, render_template, url_for, request, flash)
from models import db, app, Projects
from datetime import datetime, timedelta


# Routes
# Index - Root Page
@app.route('/')
def index():
    # All projects sorted by date finished.
    project_df = Projects.query.order_by(Projects.last_commit.desc()).all()
    skill_set = set()
    projects = Projects.query.all()
    for skill in projects:
        skill = skill.skills.split(', ')
        for item in skill:
            skill_set.add(item)
    skill_set = sorted(skill_set)
    return render_template(
        'index.html',
        skill_set=skill_set,
        project_df=project_df
        )


# About Me
@app.route('/about')
def about():
    # All projects sorted by date finished.
    project_df = Projects.query.order_by(Projects.last_commit.desc()).all()
    total_time = 0
    for project in project_df:
        project_time = (
            project.last_commit-project.first_commit) + timedelta(days=1)
        total_time += project_time.days
    total_projects = len(project_df)
    
    return render_template(
        'about.html',
        project_df=project_df,
        total_projects=total_projects,
        total_time=total_time
    )


# projects/new - Create Route
@app.route('/projects/new', methods=['GET', 'POST'])
def create_project():
    # All projects sorted by date finished.
    project_df = Projects.query.order_by(Projects.last_commit.desc()).all()
    if request.form:
        print(request.form)
        new_project = Projects(
            title=request.form['title'],
            type=request.form['type'],
            first_commit=clean_time(request.form['first_commit']),
            last_commit=clean_time(request.form['last_commit']),
            description=request.form['description'],
            skills=request.form['skills'],
            url_to_project=request.form['github']
        )
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template(
        'projectform.html',
        project_df=project_df
    )


# projects/<id> - Detail Route (View)
@app.route('/projects/<id>')
def project_detail(id):
    # All projects sorted by date finished.
    project_df = Projects.query.order_by(Projects.last_commit.desc()).all()
    project = Projects.query.get_or_404(id)
    project.skills = project.skills.split(',')
    time_taken = (project.last_commit-project.first_commit)+timedelta(days=1)
    project.first_commit = project.first_commit.strftime('%m/%d/%Y')
    project.last_commit = project.last_commit.strftime('%m/%d/%Y')
    return render_template(
        'detail.html',
        project=project,
        project_df=project_df,
        time_taken=time_taken
    )


# projecst/<id>/edit - Edit/Update Route
@app.route('/projects/<id>/edit', methods=['GET', 'POST'])
def edit_project(id):
    # All projects sorted by date finished.
    project_df = Projects.query.order_by(Projects.last_commit.desc()).all()
    project = Projects.query.get_or_404(id)
    if request.form:
        project.title = request.form['title']
        project.type = request.form['type']
        project.data_started = clean_time(request.form['first_commit'])
        project.last_commit = clean_time(request.form['last_commit'])
        project.description = request.form['description']
        project.skills = request.form['skills']
        project.url_to_project = request.form['github']
        db.session.commit()
        flash('User Successfully Updated')
        return redirect(url_for('project_detail', id=project.id))
    return render_template(
        'projectform_edit.html',
        project=project,
        project_df=project_df
    )


# projects/<id>/delete - Delete Route
@app.route('/projects/<id>/delete', methods=['GET', 'POST'])
def delete_project(id):
    project = Projects.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('index'))

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', msg=error), 404

def clean_time(time_str):
    return datetime.datetime.strptime(time_str, '%Y-%m-%d')


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, port=8000, host='localhost')
