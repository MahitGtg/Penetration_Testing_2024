import sqlite3

# Database connection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Encrypt the data
def encrypt_data(data):
    key = 'secretkey'
    return ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(data, key * len(data)))

# Initialize the database and create tables
def init_db():
    conn = get_db_connection()
    with conn:
        # Create users table with encrypted passwords
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                session_key TEXT
            )
        ''')

        # Create comments table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL
            )
        ''')

        # Create flags table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS flags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                flag_value TEXT NOT NULL
            )
        ''')

        # Add default users with encrypted passwords
        encrypted_admin_password = encrypt_data('adminpassword@89')
        encrypted_user_password = encrypt_data('xssvuln21')

        conn.execute("INSERT OR IGNORE INTO users (id, username, password, session_key) VALUES (1, 'admin', ?, 'default_admin_session')", (encrypted_admin_password,))
        conn.execute("INSERT OR IGNORE INTO users (id, username, password) VALUES (2, 'radin3600', ?)", (encrypted_user_password,))

        # Insert the encrypted flag
        encrypted_flag = encrypt_data('flag{LastOneStanding:t0uch_S0M3_gR4sS}')
        conn.execute("INSERT OR IGNORE INTO flags (id, flag_value) VALUES (1, ?)", (encrypted_flag,))

    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized with encrypted data.")
