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
