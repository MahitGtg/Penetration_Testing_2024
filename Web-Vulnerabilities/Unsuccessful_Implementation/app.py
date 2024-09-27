from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Secret key for session management

# Database connection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create tables if they don't exist and add default users
def init_db():
    conn = get_db_connection()
    with conn:
        # Create users table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        # Create shifts table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS shifts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                start_date TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_date TEXT NOT NULL,
                end_time TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
    add_users(conn)
    conn.close()

# Generate a SHA-1 hash for the password
def password_generate(password):
    sha1_hash = hashlib.sha1(password.encode()).hexdigest()
    return sha1_hash

# Check if the given plain-text password matches the stored SHA-1 hash
def password_check(stored_password, provided_password):
    return stored_password == password_generate(provided_password)

# Add default users with hashed passwords
def add_users(conn):
    users = [
        (6, password_generate('chelsea'), 'bradly.coopers'),
        (2, password_generate('flag{user:sam}'), 'anthony.creg'),
        (3, password_generate('flag{pass:p1zz4Heav3n}'), 'charlie.mazuri'),
        (4, password_generate('flag{user:Jasmin}'), 'sarah.taylor'),
        (5, password_generate('Welcome#2024'), 'emily.jones'),
        (7, password_generate('S3cureM3ssage@1'), 'michael.scott'),
        (1, password_generate('flag{pass:panda_hugger123}'), 'admin')
    ]

    for user in users:
        try:
            conn.execute("INSERT OR IGNORE INTO users (id, password, username) VALUES (?, ?, ?)", user)
        except sqlite3.IntegrityError as e:
            print(f"Error inserting user {user}: {e}")
    
    conn.commit()

init_db()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Generate SHA-1 hash for the entered password
        hashed_password = password_generate(password)
        
        conn = get_db_connection()
        
        # Vulnerable SQL query allowing SQL injection
        cursor = conn.execute(f"SELECT * FROM users WHERE username='{username}' AND password='{hashed_password}'") # Blind SQL Injection vulnerability
        user = cursor.fetchone()
        conn.close()

        # Check if the user exists and if the password is correct
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid username or password.')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = password_generate(request.form['password'])  # Hash the password before storing

        conn = get_db_connection()
        try:
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return render_template('register.html', error='Username already exists.')
        finally:
            conn.close()

    return render_template('register.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        start_date = request.form['start_date']
        start_time = request.form['start_time']
        end_date = request.form['end_date']
        end_time = request.form['end_time']
        user_id = session['user_id']

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO shifts (user_id, start_date, start_time, end_date, end_time) VALUES (?, ?, ?, ?, ?)",
            (user_id, start_date, start_time, end_date, end_time)
        )
        conn.commit()
        conn.close()

    return render_template('home.html', username=session['username'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
