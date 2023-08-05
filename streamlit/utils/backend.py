from utils.db_utils import SessionLocal, crud, schemas, models, engine

models.Base.metadata.create_all(bind=engine)

def create_user(username, password, cnf_password, firstname, lastname):
    db = SessionLocal()
    data = {
        "username": username,
        "password": password,
        "cnf_password": cnf_password,
        "firstname": firstname,
        "lastname": lastname
    }
    user = schemas.UserCreate(**data)
    crud.create_user(db, user)

def authenticate_user(username, password):
    db = SessionLocal()
    data = {
        "username": username,
        "password": password
    }
    creds = schemas.UserAuthentication(**data)
    return crud.authenticate_user(db, creds)

# create_user("ashritha@gmail.com", "ashritha", "ashritha", "ashritha", "ashritha")
# print(authenticate_user("ashritha@gmail.com", "ashritha"))
