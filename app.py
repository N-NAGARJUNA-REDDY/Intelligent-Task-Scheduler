# app.py
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from flask import send_file
from datetime import datetime, timedelta
import os
import joblib

app = Flask(__name__)
TASKS_FILE = 'data_smart_scheduler_tasks.csv'
MODEL_FILE = 'urgency_predictor.pkl'

priority_map = {'Low': 1, 'Medium': 2, 'High': 3}

@app.route('/')
def index():
    if os.path.exists(TASKS_FILE):
        df = pd.read_csv(TASKS_FILE)
        schedule = run_scheduler(df)
        return render_template('schedule.html', schedule=schedule)
    else:
        return render_template('schedule.html', schedule=[])

@app.route('/add_task')
def add_task():
    return render_template('add_task.html')

@app.route('/submit', methods=['POST'])
def submit():
    task_name = request.form['task_name']
    deadline = request.form['deadline']
    priority = request.form['priority']
    effort = int(request.form['effort'])

    task_id = int(datetime.now().timestamp())

    if os.path.exists(MODEL_FILE):
        clf = joblib.load(MODEL_FILE)
        days_left = (pd.to_datetime(deadline) - pd.Timestamp.today()).days
        urgency = clf.predict([[priority_map[priority], effort, days_left]])[0]
    else:
        urgency = "Medium"

    new_row = pd.DataFrame([{
        'TaskID': task_id,
        'TaskName': task_name,
        'Deadline': deadline,
        'PriorityLevel': priority,
        'EstimatedEffortHours': effort,
        'Urgency': urgency,
        'Completed': 'No'
    }])

    if os.path.exists(TASKS_FILE):
        df = pd.read_csv(TASKS_FILE)
        df = pd.concat([df, new_row], ignore_index=True)
    else:
        df = new_row

    df.to_csv(TASKS_FILE, index=False)
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    if os.path.exists(TASKS_FILE):
        df = pd.read_csv(TASKS_FILE)
        df = df[df['TaskID'] != task_id]
        df.to_csv(TASKS_FILE, index=False)
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def mark_complete(task_id):
    if os.path.exists(TASKS_FILE):
        df = pd.read_csv(TASKS_FILE)
        df.loc[df['TaskID'] == task_id, 'Completed'] = 'Yes'
        df.to_csv(TASKS_FILE, index=False)
    return redirect(url_for('index'))

@app.route('/tasks')
def view_tasks():
    if os.path.exists(TASKS_FILE):
        df = pd.read_csv(TASKS_FILE)
        return render_template('view_tasks.html', tasks=df.to_dict(orient='records'))
    return render_template('view_tasks.html', tasks=[])

@app.route('/download')
def download_tasks():
    if os.path.exists(TASKS_FILE):
        return send_file(TASKS_FILE, mimetype='text/csv', as_attachment=True, download_name='all_tasks.csv')
    return redirect(url_for('index'))


@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit(task_id):
    df = pd.read_csv(TASKS_FILE)
    task = df[df['TaskID'] == task_id].iloc[0]

    if request.method == 'POST':
        df.loc[df['TaskID'] == task_id, 'TaskName'] = request.form['task_name']
        df.loc[df['TaskID'] == task_id, 'Deadline'] = request.form['deadline']
        df.loc[df['TaskID'] == task_id, 'PriorityLevel'] = request.form['priority']
        df.loc[df['TaskID'] == task_id, 'EstimatedEffortHours'] = int(request.form['effort'])
        df.to_csv(TASKS_FILE, index=False)
        return redirect(url_for('index'))

    return render_template('edit_task.html', task=task)

def run_scheduler(df):
    df['PriorityScore'] = df['PriorityLevel'].map(priority_map)
    df['DeadlineDate'] = pd.to_datetime(df['Deadline'], format='%Y-%m-%d')
    df['DaysLeft'] = (df['DeadlineDate'] - pd.Timestamp.today()).dt.days
    df['TaskScore'] = df['PriorityScore'] * 2 - df['EstimatedEffortHours'] + (10 - df['DaysLeft'])
    df_sorted = df.sort_values(by='TaskScore', ascending=False).reset_index(drop=True)

    schedule = []
    day_pointer = datetime.today()
    day_hours = 0

    for _, task in df_sorted.iterrows():
        if task['Completed'] == 'Yes':
            continue

        if day_hours + task['EstimatedEffortHours'] > 8:
            day_pointer += timedelta(days=1)
            day_hours = 0

        schedule.append({
            'TaskID': task['TaskID'],
            'TaskName': task['TaskName'],
            'ScheduledDate': day_pointer.strftime('%Y-%m-%d'),
            'EffortHours': task['EstimatedEffortHours'],
            'Urgency': task['Urgency'],
            'Priority': task['PriorityLevel'],
            'Completed': task.get('Completed', 'No')
        })
        day_hours += task['EstimatedEffortHours']

    return schedule

if __name__ == '__main__':
    app.run(debug=True)
