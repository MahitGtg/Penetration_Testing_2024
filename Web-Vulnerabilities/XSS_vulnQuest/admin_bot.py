import requests
import time
import random

# Constants
BASE_URL = 'http://0.0.0.0:5004'
LOGIN_URL = f'{BASE_URL}/login'
HOME_URL = f'{BASE_URL}/home'
LOGOUT_URL = f'{BASE_URL}/logout'
SESSION_INFO_URL = f'{BASE_URL}/session_info'
SESSION = requests.Session()

# Admin credentials
ADMIN_CREDENTIALS = {
    'username': 'admin',
    'password': 'adminpassword@89'
}

def admin_login():
    print("[*] Admin is trying to log in...")
    response = SESSION.post(LOGIN_URL, data=ADMIN_CREDENTIALS)
    
    # Check if the login was successful and retrieve session key
    if "Welcome, admin" in response.text:
        print("[+] Admin logged in successfully.")
        # Print the session key from the cookies
        if 'session' in SESSION.cookies:
            session_key = SESSION.cookies['session']
            # print(f"[+] Admin session key: {session_key}") -- remove this line in final vm
            print("[*] Retrieving full session data...")
            session_data = SESSION.get(SESSION_INFO_URL).text
            print(f"[+] Full session data: {session_data}")
        else:
            print("[-] No session key found.")
    else:
        print("[-] Admin failed to log in.")

def visit_home():
    print("[*] Admin is visiting the home page...")
    response = SESSION.get(HOME_URL)
    if "Comments:" in response.text:
        print("[+] Admin viewed the comments successfully.")
    else:
        print("[-] Admin could not access the home page.")

def admin_logout():
    print("[*] Admin is logging out...")
    response = SESSION.get(LOGOUT_URL)
    if response.status_code == 200:
        print("[+] Admin logged out successfully.")
    else:
        print("[-] Admin failed to log out.")

def simulate_admin_activity():
    while True:
        admin_login()
        visit_home()
        admin_logout()
        # Wait for a random time between 10 to 30 seconds before next activity
        time.sleep(random.randint(60, 180))

if __name__ == "__main__":
    simulate_admin_activity()
