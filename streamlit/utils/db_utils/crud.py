from sqlalchemy.orm import Session
from utils.db_utils import models, schemas

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username,
                          first_name=user.firstname,
                          last_name=user.lastname,
                          password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, credentials: schemas.UserAuthentication):
    result_user = db.query(models.User).filter(models.User.username == credentials.username).first()
    if not result_user:
        return False
    return result_user.check_password(credentials.password)
