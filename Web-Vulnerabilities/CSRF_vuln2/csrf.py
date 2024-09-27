from flask import Flask, request
import random

app = Flask(__name__)

# Secret Flag Obfuscated with more complex structure
part_1 = ''.join(['tu', 'vvw', 'xm_'])
part_2 = ''.join(['az', 'rj7', '89'])
parts = [part_1, part_2]
flag_prefix = "".join(chr(i) for i in [102, 108, 97, 103, 123])  # 'flag{'
flag_suffix = chr(125)  # '}'
SECRET_FLAG = flag_prefix + ''.join(parts) + flag_suffix

# Randomized function name
def uxrnyv_sdlmop(s):
    result = []
    for char in s:
        if 'a' <= char <= 'z':
            # Rotate alphabetic characters by 13 places
            result.append(chr((ord(char) - ord('a') + 13) % 26 + ord('a')))
        elif '0' <= char <= '9':
            # Rotate numeric characters by 5 places
            result.append(chr((ord(char) - ord('0') + 5) % 10 + ord('0')))
        else:
            result.append(char)
    return ''.join(result)

# Encrypt the flag with ROT18
encrypted_flag = uxrnyv_sdlmop(SECRET_FLAG)

# Vulnerable route expecting a specific form submission
@app.route('/submit_form', methods=['POST'])
def submit_form():
    expected_token = 'malicious_token'
    if request.form.get('username') == 'pentester' and request.form.get('token') == expected_token:
        return f'Encrypted Flag: {encrypted_flag}'
    return 'Form submission failed or invalid data.', 400

# Simple landing page
@app.route('/')
def index():
    return "Welcome to the vulnerable web app. Try submitting a form to /submit_form."

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5008)
