from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash:
    def hash_password(password):
        return pwd_context.hash(password)

    def verify_password(plain_password, password_hash):
        return pwd_context.verify(plain_password, password_hash) 