Transactions
from .base import Base
from .account import Account
from sqlalchemy import Integer, String, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import func
from flask_login import UserMixin
import bcrypt

class Transaction(Base, UserMixin):
    __tablename__ = 'Transactions'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    from_account_id = mapped_column(Integer, ForeignKey('Accounts.id'))
    to_account_id = mapped_column(Integer, ForeignKey('Accounts.id'))
    amount = mapped_column(Numeric(10,2))
    type = mapped_column(String(255), nullable=False)
    description = mapped_column(String(255))
    create_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    from_account = relationship("Account",foreign_keys=[from_account_id])
    to_account = relationship("Account", foreign_keys=[to_account_id])

    def __repr__(self):
        return f'<Transaction {self.id}>'