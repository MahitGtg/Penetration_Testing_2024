from flask import Flask, render_template, request, redirect, url_for, session, make_response
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Database connection
def get_db_connection():
    conn = sqlite3.connect('helpai_forum.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize the database with default users and comments
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create Users Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    ''')

    # Create Comments Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        comment TEXT NOT NULL
    )
    ''')

    # Create Answers Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS answers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        comment_id INTEGER NOT NULL,
        username TEXT NOT NULL,
        answer TEXT NOT NULL,
        FOREIGN KEY(comment_id) REFERENCES comments(id)
    )
    ''')

    # Create Flags Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS flags (
        id INTEGER PRIMARY KEY,
        flag TEXT NOT NULL
    )
    ''')

    # Insert a few users
    cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('john.doe', 'password123')")
    cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('jane.smith', 'password456')")
    cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('radin.mansouri', 'liverpool')")
    cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('samantha.smith', 'shadow')")
    cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('joseph.alexander', 'iloveyou2')")
    cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('admin', 'adminpassword')")

    # Insert a few comments
    cursor.execute("INSERT OR IGNORE INTO comments (id, username, comment) VALUES (1, 'john.doe', 'How do I reset my password?')")
    cursor.execute("INSERT OR IGNORE INTO comments (id, username, comment) VALUES (2, 'jane.smith', 'What is the AI used in HelpAI?')")
    cursor.execute("INSERT OR IGNORE INTO comments (id, username, comment) VALUES (3, 'samantha.smith', 'I keep getting logged out. Is there a way to stay signed in?')")
    cursor.execute("INSERT OR IGNORE INTO comments (id, username, comment) VALUES (4, 'joseph.alexander', 'Can I customize my notification preferences?')")
    cursor.execute("INSERT OR IGNORE INTO comments (id, username, comment) VALUES (5, 'admin', 'Is there an admin panel for managing users?')")
    cursor.execute("INSERT OR IGNORE INTO comments (id, username, comment) VALUES (6, 'radin.mansouri', 'For the last task, remember that the final user has unique capabilities. If needed, they can influence something significant.')")

    # Insert flags
    cursor.execute("INSERT OR IGNORE INTO flags (id, flag) VALUES (1, 'flag{Jerome:c4ctus_JuIcE}')")
    cursor.execute("INSERT OR IGNORE INTO flags (id, flag) VALUES (2, 'flag{LastOneStanding:t0uch_S0M3_gR4sS}')")

    conn.commit()
    conn.close()

# Home page displaying comments
@app.route('/')
def index():
    conn = get_db_connection()
    comments = conn.execute("SELECT * FROM comments").fetchall()
    conn.close()
    return render_template('index.html', comments=comments)

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password)).fetchone()
        conn.close()

        if user:
            session['username'] = user['username']
            resp = make_response(redirect(url_for('dashboard')))
            resp.set_cookie('username', user['username'])  # Setting a cookie for the logged-in user
            return resp
        else:
            return render_template('login.html', error='Invalid username or password.')

    return render_template('login.html')

# Registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        try:
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return render_template('register.html', error='Username already exists.')

    return render_template('register.html')

# Dashboard where users can post answers
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    comments = conn.execute("SELECT * FROM comments").fetchall()
    answers = conn.execute("SELECT * FROM answers").fetchall()
    conn.close()

    resp = make_response(render_template('dashboard.html', comments=comments, answers=answers))

    if session['username'] == 'admin':
        # Send the flags as cookies if the user is admin
        conn = get_db_connection()
        flag1 = conn.execute("SELECT flag FROM flags WHERE id = 1").fetchone()['flag']
        flag2 = conn.execute("SELECT flag FROM flags WHERE id = 2").fetchone()['flag']
        conn.close()

        resp.set_cookie('flag1', flag1)
        resp.set_cookie('flag2', flag2)

    if request.method == 'POST':
        comment_id = request.form['comment_id']
        answer = request.form['answer']
        username = session['username']

        conn = get_db_connection()
        conn.execute("INSERT INTO answers (comment_id, username, answer) VALUES (?, ?, ?)", (comment_id, username, answer))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))

    return resp

# Comment submission
@app.route('/comment', methods=['POST'])
def comment():
    username = request.form['username']
    comment = request.form['comment']

    conn = get_db_connection()
    conn.execute("INSERT INTO comments (username, comment) VALUES (?, ?)", (username, comment))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

# Logout function
@app.route('/logout')
def logout():
    session.clear()
    resp = make_response(redirect(url_for('login')))
    resp.delete_cookie('username')  # Delete the cookie on logout
    return resp

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5002)  # Change port to 5002 and host to 0.0.0.0
