from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(320), unique=True)
    occupation = Column(String(20))
    special_key = Column(String(320), unique=True)
    salt = Column(String(50))
    ac_creation_date = Column(Date)
    ac_creation_time = Column(Time)
    is_admin = Column(Boolean, default=False)


class Password(Base):
    __tablename__ = "passwords"

    id = Column(Integer, primary_key=True, index=True)
    password = Column(String(255))
    hashed_special_key = Column(String(255)) # , ForeignKey(User.special_key)

    # user = relationship('User', foreign_keys='Password.hashed_special_key')


class Otp(Base):
    __tablename__ = "otps"

    id = Column(Integer, primary_key=True, index=True)
    otp = Column(String(6))
    email = Column(String(320))
    counter = Column(Integer)
    used = Column(Integer)


