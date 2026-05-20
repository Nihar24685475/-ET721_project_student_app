import sqlite3
import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "student_project_secret"

# -----------------------------------
# DATABASE CONNECTION
# -----------------------------------
def get_db():
    conn = sqlite3.connect("Nihar_app.db")
    conn.row_factory = sqlite3.Row
    return conn

# -----------------------------------
# HOME PAGE
# -----------------------------------
@app.route('/')
def home():
    return render_template('index.html')

# -----------------------------------
# LOGIN PAGE
# -----------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE email = ? AND password = ?",
            (email, password)
        )
        user = cursor.fetchone()
        conn.close()
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid email or password")
    return render_template('login.html')

# -----------------------------------
# SIGNUP PAGE
# -----------------------------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO users (username, email, password)
                VALUES (?, ?, ?)
                """,
                (username, email, password)
            )
            conn.commit()
            flash("Account created successfully!")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Email already exists!")
        finally:
            conn.close()
    return render_template('signup.html')

# -----------------------------------
# DASHBOARD
# -----------------------------------
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db()
    cursor = conn.cursor()

    # TASKS
    cursor.execute(
        "SELECT COUNT(*) FROM tasks WHERE user_id = ?",
        (session['user_id'],)
    )
    total_tasks = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM tasks WHERE user_id = ? AND status = 'Completed'",
        (session['user_id'],)
    )
    completed_tasks = cursor.fetchone()[0]

    # BLOGS
    cursor.execute(
        "SELECT COUNT(*) FROM blogs WHERE user_id = ?",
        (session['user_id'],)
    )
    total_blogs = cursor.fetchone()[0]

    
    # NOTES
    cursor.execute(
        "SELECT COUNT(*) FROM images WHERE user_id = ?",
        (session['user_id'],)
    )
    total_images = cursor.fetchone()[0]

    conn.close()

    return render_template(
        'dashboard.html',
        username=session['username'],
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        total_blogs=total_blogs,
        total_images=total_images
    )

# -----------------------------------
# LOGOUT
# -----------------------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# -----------------------------------
# TODO PAGE
# -----------------------------------
@app.route('/todo')
def todo():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM tasks WHERE user_id = ?",
        (session['user_id'],))
    tasks = cursor.fetchall()
    conn.close()
    return render_template('todo.html', tasks=tasks)

# -----------------------------------
# ADD TASK
# -----------------------------------
@app.route('/add_task', methods=['POST'])
def add_task():
    task = request.form['task']
    user_id = session['user_id']
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (task, user_id) VALUES (?, ?)",
        (task, user_id))
    conn.commit()
    conn.close()
    return redirect(url_for('todo'))

# -----------------------------------
# DELETE TASK
# -----------------------------------
@app.route('/delete_task/<int:id>')
def delete_task(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM tasks WHERE id = ?",
        (id,)
    )
    conn.commit()
    conn.close()
    return redirect(url_for('todo'))

# -----------------------------------
# COMPLETE TASK
# -----------------------------------
@app.route('/complete_task/<int:id>')
def complete_task(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE tasks
        SET status = 'Completed'
        WHERE id = ?
        """,
        (id,)
    )
    conn.commit()
    conn.close()
    return redirect(url_for('todo'))

# -----------------------------------
# EDIT TASK
# -----------------------------------
@app.route('/update_task/<int:id>', methods=['POST'])
def update_task(id):
    new_task = request.form['task']
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tasks SET task = ? WHERE id = ?",
        (new_task, id)
    )
    conn.commit()
    conn.close()
    return redirect(url_for('todo'))

# -----------------------------------
# BLOG PAGE
# -----------------------------------
@app.route('/blog')
def blog():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM blogs WHERE user_id = ?",
        (session['user_id'],))
    posts = cursor.fetchall()
    conn.close()
    return render_template('blog.html', posts=posts)

# -----------------------------------
# CREATE BLOG
# -----------------------------------
@app.route('/add_blog', methods=['POST'])
def add_blog():
    title = request.form['title']
    content = request.form['content']
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
    "INSERT INTO blogs (title, content, user_id) VALUES (?, ?, ?)",
    (title, content, session['user_id']))
    conn.commit()
    conn.close()
    return redirect(url_for('blog'))

# delete blog
@app.route('/delete_blog/<int:id>')
def delete_blog(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM blogs WHERE id = ?",
        (id,)
    )
    conn.commit()
    conn.close()
    return redirect(url_for('blog'))


@app.route('/notes')
def notes():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM images WHERE user_id = ?",
        (session['user_id'],)
    )
    images = cursor.fetchall()
    conn.close()
    return render_template('notes.html', images=images)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
    "INSERT INTO images (filename, user_id) VALUES (?, ?)",
    (filename, session['user_id'])
)
        conn.commit()
        conn.close()
    return redirect(url_for('notes'))

# -----------------------------------
# DELETE IMAGE
# -----------------------------------
@app.route('/delete_image/<int:id>')
def delete_image(id):
    conn = get_db()
    cursor = conn.cursor()
    # get filename first
    cursor.execute(
        "SELECT filename FROM images WHERE id = ?",
        (id,)
    )
    image = cursor.fetchone()
    if image:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], image['filename'])
        # delete file from folder
        if os.path.exists(filepath):
            os.remove(filepath)
        # delete from database
        cursor.execute(
            "DELETE FROM images WHERE id = ?",
            (id,)
        )
        conn.commit()
    conn.close()
    return redirect(url_for('notes'))

# -----------------------------------
# RUN FLASK
# -----------------------------------
if __name__ == '__main__':

    app.run(debug=True)