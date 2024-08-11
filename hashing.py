from passlib.context import CryptContext
pwd_cxt=CryptContext(schemes=["bcrypt"],deprecated="auto")
class hash():
    def bcrypt(password):
        return pwd_cxt.hash(password)
    def verify(plain,hashed):
        return pwd_cxt.verify(plain,hashed)

