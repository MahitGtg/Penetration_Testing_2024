from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import re

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Secret key for session management
# Disable HttpOnly flag to allow JavaScript access to session cookies
app.config.update(
    SESSION_COOKIE_HTTPONLY=False
)

# Database connection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Encrypt the data
def encrypt_data(data):
    key = 'secretkey'
    return ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(data, key * len(data)))

# Decrypt the data
def decrypt_data(data):
    key = 'secretkey'
    return ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(data, key * len(data)))

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()

        if user:
            # Decrypt the stored password and compare it with the provided password
            decrypted_password = decrypt_data(user['password'])
            if decrypted_password == password:
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['session_key'] = user['session_key']  # Store session key
                
                # Check if it's the admin user
                if user['username'] == 'admin':
                    session['admin_session_key'] = user['session_key']
                return redirect(url_for('home'))
            else:
                return render_template('login.html', error='Invalid username or password.')
        else:
            return render_template('login.html', error='Invalid username or password.')

    return render_template('login.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    comments = conn.execute('SELECT * FROM comments').fetchall()
    conn.close()

    return render_template('home.html', username=session['username'], comments=comments)

@app.route('/comment', methods=['POST'])
def comment():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Sanitize comment input
    comment = sanitize_input(request.form['comment'])
    conn = get_db_connection()
    conn.execute("INSERT INTO comments (content) VALUES (?)", (comment,))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

@app.route('/public', methods=['GET', 'POST'])
def public():
    # Vulnerable public page to demonstrate XSS and reveal credentials
    hidden_credentials = "<div id='credentials' style='display:none;'>username=radin3600&password=xssvuln21</div>"
    if request.method == 'POST':
        feedback = request.form['feedback']
        sanitized_feedback = sanitize_input(feedback)
        return render_template('public.html', feedback=sanitized_feedback, hidden_credentials=hidden_credentials)
    
    return render_template('public.html', hidden_credentials=hidden_credentials)

@app.route('/flag')
def flag():
    if 'admin_session_key' in session and session['admin_session_key'] == 'default_admin_session':
        conn = get_db_connection()
        flag_value = conn.execute('SELECT flag_value FROM flags WHERE id = 1').fetchone()
        conn.close()
        if flag_value:
            decrypted_flag = decrypt_data(flag_value['flag_value'])
            return render_template('flag.html', flag=decrypted_flag)
    return "Access denied."

@app.route('/session_info')
def session_info():
    return str(session)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Function to sanitize comment input by removing <script> tags
def sanitize_input(input_text):
    return re.sub(r'<\s*script[^>]*>', '', input_text, flags=re.IGNORECASE)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5004)
