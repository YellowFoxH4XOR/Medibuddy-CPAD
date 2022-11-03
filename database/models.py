from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON, DATE
from database.db import Base


class User(Base):
    __tablename__ = "users"

    email = Column(String, primary_key=True, index=True)
    hashed_password = Column(String)
    cart = Column(JSON)

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String)
    ordered_items = Column(JSON)
    order_status = Column(String, default="Processing")
    ordered_on = Column(Integer)


class Medicine(Base):
    __tablename__ = "medicine"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    details = Column(JSON)
    quantity = Column(Integer)
    type = Column(String, default="medicine")
    price = Column(Integer)
