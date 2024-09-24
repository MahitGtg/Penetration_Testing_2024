import hashlib

password = "nInJaP3NgUiN"
hashed_password = hashlib.sha256(password.encode()).hexdigest()
print(hashed_password)
