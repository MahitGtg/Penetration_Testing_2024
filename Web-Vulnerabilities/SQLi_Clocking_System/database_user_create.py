import sqlite3
import hashlib

# Database connection
def get_db_connection():
    conn = sqlite3.connect('clocking_database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create tables if they don't exist
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
    conn.close()

# Generate a SHA-1 hash for the password
def password_generate(password):
    sha1_hash = hashlib.sha1(password.encode()).hexdigest()
    return sha1_hash

# Add default users with hashed passwords
def add_users():
    conn = get_db_connection()
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
    conn.close()

if __name__ == '__main__':
    init_db()
    add_users()
    print("Database initialized and users added successfully.")
