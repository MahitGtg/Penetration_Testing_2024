import hashlib

password = 'bestwestern'
hashed_password = hashlib.sha256(password.encode()).hexdigest()
print(hashed_password)
