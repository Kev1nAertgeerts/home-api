from sqlalchemy import DateTime, Float, Column, ForeignKey, Integer, String, Boolean
from database.database import Base
from datetime import datetime

class Member(Base):
    __tablename__ = "member"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(15), index=True)
    last_name = Column(String(15), index=True)
    date = Column(DateTime, default=datetime.now)

    def __str__(self):
        return self.first_name
    

class Price(Base):
    __tablename__ = "price"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(15), index=True, unique=True)
    price = Column(Float, index=True)
    date = Column(DateTime, default=datetime.now)

    def __str__(self):
        return self.name
    

class Drink(Base):
    __tablename__ = "drink"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(15), index=True, unique=True)
    price = Column(Integer, ForeignKey("price.id"))
    date = Column(DateTime, default=datetime.now)

    def __str__(self):
        return self.name
    

class Consumption(Base):
    __tablename__ = "consumption"

    id = Column(Integer, primary_key=True, index=True)
    member = Column(Integer, ForeignKey("member.id"))
    drink = Column(Integer, ForeignKey("drink.id"))
    date = Column(DateTime, default=datetime.now)
    #payed = Column(Boolean, default=False)
    paydate = Column(DateTime, nullable=True)


class Payments(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    member = Column(Integer, ForeignKey("member.id"))
    date = Column(DateTime, default=datetime.now)
    quantity = Column(Float, index=True)
    verified = Column(Boolean, default=False)