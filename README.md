# Intelligent-Task-Scheduler

A Flask-based intelligent task scheduler that helps you manage and prioritize tasks efficiently.


## 🚀 Features

- ✅ Add, view, edit, and delete tasks
- 📌 Set deadlines, priorities, efforts, and urgency levels
- 📊 Mark tasks as completed
- 🧠 AI-inspired scoring logic (planned)
- 📁 Data stored in a CSV file
- 🖼️ Image support in task views



## 🛠️ Tech Stack

- Python 3.10+
- Flask
- Pandas
- HTML, CSS (Bootstrap)
- Jinja2 templates

---

## 📁 Project Structure

```

TechSophy2/
├── app.py                       # Main Flask app
├── data\_smart\_scheduler\_tasks.csv  # Task storage in CSV format
├── static/
│   ├── style.css               # Optional styles
│   └── task.png                # Icon shown in "All Tasks" page
├── templates/
│   ├── add\_task.html
│   ├── completed.html
│   ├── edit\_task.html
│   ├── schedule.html
│   └── view\_tasks.html         # Displays all tasks
└── README.md

````

---

## 📸 Image Support

To show an image beside your heading (like in "All Tasks"), include:

```html
<h2>
  <img src="{{ url_for('static', filename='task.png') }}" height="40" style="margin-right: 10px;">
  All Tasks
</h2>
````

Make sure `task.png` exists in the `/static/` folder.

---

## 🧪 How to Run

1. Install dependencies:

```bash
pip install flask pandas
```

2. Run the app:

```bash
python app.py
```

3. Open in your browser:

```
http://127.0.0.1:5000
```

---

## 🔮 Future Ideas

* Task priority scoring (AI/ML or heuristic)
* Schedule optimization with working hours
* Calendar/Gantt view for better visualization
* User accounts and login system
* SQLite/PostgreSQL database support

---

## 👨‍💻 Developed By

**Nomula Nagarjuna Reddy**
BVRIT Narsapur
Final Year – CSE

Happy coding! 💻✨
