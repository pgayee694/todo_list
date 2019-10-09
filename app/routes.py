from flask import (render_template, request, url_for, redirect, current_app, flash)
from datetime import datetime
from app import app, db, models

@app.route('/')
@app.route('/index')
def index():
    tasks = models.Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'GET': # display add form
        return render_template('add.html')
    elif request.method == 'POST':
        return add_task()
    else:
        current_app.logger.info('INVALID REQUEST')

@app.route('/del/<task_id>', methods=['GET'])
def delete(task_id):
    task = models.Task.query.filter_by(id=task_id).scalar()
    db.session.delete(task)
    db.session.commit()
    flash('Deleted clarification {}'.format(task_id), 'warning')

    return redirect(url_for('index'))

def add_task():
    name = request.form.get('name')
    deadline_input = request.form.get('deadline')
    priority = request.form.get('priority')

    if not name:
        error = 'No name given'
        current_app.logger.info(error)
        flash(error, 'danger')
    if not deadline_input:
        error = 'No deadline given'
        current_app.logger.info(error)
        flash(error, 'danger')
    if not priority:
        error = 'No priority given'
        current_app.logger.info(error)
        flash(error, 'danger')
    
    deadline_components = list(map(int, deadline_input.split('-')))
    deadline = None
    try:
        if deadline_components and len(deadline_components) >= 6:
            deadline = datetime(deadline_components[0], deadline_components[1], deadline_components[2], deadline_components[3], deadline_components[4], deadline_components[5])
    except:
        error = 'Did not submit a valid deadline'
        current_app.logger.info(error)
        flash(error, 'danger')

    task = models.Task(name=name, deadline=deadline, priority=priority)
    db.session.add(task)
    db.session.commit()
    info = 'Submitted new task'
    current_app.logger.info(info)
    flash(info, 'danger')

    return redirect(url_for('index'))