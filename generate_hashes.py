import bcrypt

password_admin = "coder"
password_clark = "clark"

hash_admin = bcrypt.hashpw(password_admin.encode(), bcrypt.gensalt())
hash_clark = bcrypt.hashpw(password_clark.encode(), bcrypt.gensalt())

print("Hash admin:", hash_admin.decode())
print("Hash clark:", hash_clark.decode())
