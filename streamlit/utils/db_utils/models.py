from utils.db_utils import Base
from sqlalchemy import Column, Integer, String
from datetime import datetime
from utils.generic import parse_timestamp, get_hashed_password
import bcrypt
from sqlalchemy.orm import validates
import re


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(100), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)

    def __init__(self, username, first_name, last_name, password):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.account_created = datetime.now()
        self.account_updated = datetime.now()
        self.set_password(password)

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def __repr__(self):
        return "Print " + self.username

    def __iter__(self):
        for key in ["id", "first_name", "last_name", "username", "account_created", "account_updated"]:
            if key in ["account_created", "account_updated"]:
                yield key, parse_timestamp(getattr(self, key))
            else:
                yield key, getattr(self, key)
    
    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise Exception('No username provided')

        if not isinstance(username, str):
            raise Exception('Username should be a string')

        if self.username:
            if self.username != username:
                raise Exception('Username update not allowed')
            else:
                return username

        # if User.query.filter(User.username == username).first():
        #     raise Exception('Username is already in use')

        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if not re.fullmatch(regex, username):
            raise Exception(
                "Username doesn't have a valid email address")

        return username

    @validates('first_name')
    def validate_first_name(self, key, first_name):
        if not first_name:
            raise Exception('first name can\'t be empty')

        if not isinstance(first_name, str):
            raise Exception('First name should be a string')

        return first_name

    @validates('last_name')
    def validate_last_name(self, key, last_name):
        if not last_name:
            raise Exception('last name can\'t be empty')

        if not isinstance(last_name, str):
            raise Exception('last name should be a string')

        return last_name

    def set_password(self, password):
        if not password:
            raise Exception('Password not provided')

        if not isinstance(password, str):
            raise Exception('password should be a string')

        if len(password) < 8 or len(password) > 50:
            raise Exception(
                'Password must be between 8 and 50 characters')
        self.password_hash = get_hashed_password(password).decode('utf-8')
