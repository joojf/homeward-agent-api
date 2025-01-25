import pytest
from fastapi import HTTPException

from app.models import Application, Customer
from app.schemas import AgentCreate, AgentUpdate
from app.services.agent_service import AgentService


def test_get_all_agents_empty(db_session):
    agents = AgentService.get_all_agents(db_session)
    assert len(agents) == 0


def test_create_agent(db_session, sample_agent_data):
    agent_data = AgentCreate(**sample_agent_data)
    agent = AgentService.create_agent(db_session, agent_data)

    assert agent.name == sample_agent_data["name"]
    assert agent.email == sample_agent_data["email"]
    assert agent.phone_number == sample_agent_data["phone_number"]
    assert agent.location == sample_agent_data["location"]


def test_create_duplicate_agent(db_session, sample_agent_data):
    agent_data = AgentCreate(**sample_agent_data)
    AgentService.create_agent(db_session, agent_data)

    with pytest.raises(HTTPException) as exc_info:
        AgentService.create_agent(db_session, agent_data)
    assert exc_info.value.status_code == 400
    assert "already exists" in str(exc_info.value.detail)


def test_get_agent(db_session, sample_agent_data):
    agent_data = AgentCreate(**sample_agent_data)
    created_agent = AgentService.create_agent(db_session, agent_data)

    agent = AgentService.get_agent(db_session, created_agent.id)
    assert agent.id == created_agent.id
    assert agent.email == sample_agent_data["email"]


def test_get_nonexistent_agent(db_session):
    with pytest.raises(HTTPException) as exc_info:
        AgentService.get_agent(db_session, 999)
    assert exc_info.value.status_code == 404
    assert "not found" in str(exc_info.value.detail)


def test_update_agent(db_session, sample_agent_data):
    agent_data = AgentCreate(**sample_agent_data)
    created_agent = AgentService.create_agent(db_session, agent_data)

    update_data = AgentUpdate(name="Updated Name", location="Updated Location")
    updated_agent = AgentService.update_agent(db_session, created_agent.id, update_data)

    assert updated_agent.name == "Updated Name"
    assert updated_agent.location == "Updated Location"
    assert updated_agent.email == sample_agent_data["email"]


def test_update_nonexistent_agent(db_session):
    update_data = AgentUpdate(name="Updated Name")
    with pytest.raises(HTTPException) as exc_info:
        AgentService.update_agent(db_session, 999, update_data)
    assert exc_info.value.status_code == 404
    assert "not found" in str(exc_info.value.detail)


def test_get_agent_with_customer_connection(db_session, sample_agent_data, sample_customer_data):
    agent_data = AgentCreate(**sample_agent_data)
    agent = AgentService.create_agent(db_session, agent_data)

    customer = Customer(**sample_customer_data)
    db_session.add(customer)
    db_session.commit()

    application = Application(
        customer_id=customer.id,
        agent_id=agent.id,
        purchasing_address="456 New Home St"
    )
    db_session.add(application)
    db_session.commit()

    agent_result = AgentService.get_agent(db_session, agent.id, customer.id)
    assert agent_result.id == agent.id


def test_get_agent_with_invalid_customer_connection(db_session, sample_agent_data):
    agent_data = AgentCreate(**sample_agent_data)
    agent = AgentService.create_agent(db_session, agent_data)

    with pytest.raises(HTTPException) as exc_info:
        AgentService.get_agent(db_session, agent.id, customer_id=999)
    assert exc_info.value.status_code == 404
    assert "not connected to customer" in str(exc_info.value.detail)
