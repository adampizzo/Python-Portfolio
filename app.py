from flask import (redirect, render_template, url_for, request, flash)
from models import db, app, Projects
import datetime




# Routes

# Index - Root Page
@app.route('/')
def index():
    project_df = Projects.query.order_by(Projects.date_finished.desc()).all()  # All projects sorted by date finished.
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
    project_df = Projects.query.order_by(Projects.date_finished.desc()).all()  # All projects sorted by date finished.
    if request.form:
        print(request.form)
        new_project = Projects(title=request.form['title'], type=request.form['type'],
                            date_started=clean_time(request.form['date_started']), 
                            date_finished=clean_time(request.form['date_finished']),
                            description=request.form['description'], skills=request.form['skills'], 
                            url_to_project=request.form['github'])
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('projectform.html', project_df=project_df)


# projects/<id> - Detail Route (View)
@app.route('/projects/<id>')
def project_detail(id):
    project_df = Projects.query.order_by(Projects.date_finished.desc()).all()  # All projects sorted by date finished.
    project = Projects.query.get_or_404(id)
    project.skills = project.skills.split(',')

    
    return render_template('detail.html', project=project, project_df=project_df)


# projecst/<id>/edit - Edit/Update Route
@app.route('/projects/<id>/edit', methods=['GET', 'POST'])
def edit_project(id):
    project_df = Projects.query.order_by(Projects.date_finished.desc()).all()  # All projects sorted by date finished.
    project = Projects.query.get_or_404(id)
    
    if request.form:
        project.title = request.form['title']
        project.type = request.form['type']
        project.data_started = clean_time(request.form['date_started'])
        project.date_finished = clean_time(request.form['date_finished'])
        project.description = request.form['description']
        project.skills = request.form['skills']
        project.url_to_project = request.form['github']
        db.session.commit()
        flash('User Successfully Updated')
        return redirect(url_for('project_detail', id=project.id))
    return render_template('projectform_edit.html', project=project, project_df=project_df)

# projects/<id>/delete - Delete Route
@app.route('/projects/<id>/delete', methods=['GET', 'POST'])
def delete_project(id):
    project = Projects.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('index'))




def clean_time(time_str):
    return datetime.datetime.strptime(time_str, '%Y-%m-%d')

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, port=8000, host='localhost')