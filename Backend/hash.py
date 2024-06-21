# from passlib.context import CryptContext
# import bcrypt

# password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def get_hash_password(password):
#     hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
#     return hashed_password


# def verify_password_hash(password, salt, hashed_password):
#     sallted_password = password + salt
#     is_matched = password_context.verify(sallted_password, hashed_password)
#     return is_matched



