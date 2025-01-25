import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from app.database import get_db
from app.main import app
from app.models import Base


@pytest.fixture
def db_engine():
    engine = create_engine(
        os.environ["DATABASE_URL"],
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture
def db_session(db_engine):
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture
def sample_agent_data():
    return {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone_number": "123-456-7890",
        "location": "Austin, TX"
    }


@pytest.fixture
def sample_customer_data():
    return {
        "name": "Jane Smith",
        "email": "jane.smith@example.com",
        "phone_number": "098-765-4321",
        "current_address": "123 Main St, Austin, TX"
    }
