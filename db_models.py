from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    bank_account = relationship("BankAccount", back_populates="owner", uselist=False)
    tax_record = relationship("TaxRecord", back_populates="user", uselist=False)

class BankAccount(Base):
    __tablename__ = "bank_accounts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    annual_income = Column(Float)

    owner = relationship("User", back_populates="bank_account")

class TaxRecord(Base):
    __tablename__ = "tax_records"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    tax_paid = Column(Float)
    is_tax_compliant = Column(Boolean)
    warning_message = Column(String, nullable=True)

    user = relationship("User", back_populates="tax_record")
