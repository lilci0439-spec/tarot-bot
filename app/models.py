from sqlalchemy import Column, Integer, BigInteger, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True) 
    username = Column(String, nullable=True)
    stars = Column(Integer, default=0) # Баланс звезд (реальные)
    coins = Column(Float, default=1000) # Баланс Бурса Коинов (игровые)