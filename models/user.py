from models.base import Base
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
from flask_login import UserMixin
import bcrypt

class User(Base, UserMixin):
    __tablename__ = 'Users'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    username = mapped_column(String(255), nullable=False, unique=True)
    email = mapped_column(String(255) ,nullable=False, unique=True)
    password_hash = mapped_column(String(255), nullable=False)
    create_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    update_at = mapped_column(DateTime(timezone=True), onupdate=func.now(), server_oninsert=func.now())

    def __repr__(self):
        return f'<User {self.username}>'

    def  set_password(self, password_hash):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password_hash):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))