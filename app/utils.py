from passlib.context import CryptContext

#set up the hash function
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

# verify passwords
def verify(plain_password, hashed_password):
    if plain_password == hashed_password:
        return True
    else:
        return False 

