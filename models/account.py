from .base import Base
from .user import User
from sqlalchemy import Integer, String, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import func
from flask_login import UserMixin
import bcrypt

class Account(Base, UserMixin):
    __tablename__ = 'Accounts'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id = mapped_column(Integer, ForeignKey('Users.id'))
    account_type = mapped_column(String(255), nullable=False)
    account_number = mapped_column(String(255) ,nullable=False, unique=True)
    balance = mapped_column(Numeric(10,2), nullable=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


    def __repr__(self):
        return f'<Account {self.user_id}>'