from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Agent(Base):
    __tablename__ = 'agents'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, nullable=True)
    location = Column(String, nullable=True)


class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, nullable=True)
    current_address = Column(String, nullable=True)


class Application(Base):
    __tablename__ = 'applications'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    purchasing_address = Column(String, nullable=True)
    application_approved = Column(Boolean, default=False)
    agent_id = Column(Integer, ForeignKey('agents.id'), nullable=False)
