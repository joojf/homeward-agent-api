from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas

class AgentService:
    @staticmethod
    def get_all_agents(db: Session):
        return db.query(models.Agent).all()

    @staticmethod
    def get_agent(db: Session, agent_id: int, customer_id: int = None):
        agent = db.query(models.Agent).filter(models.Agent.id == agent_id).first()
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent with id={agent_id} not found."
            )
        if customer_id:
            application = db.query(models.Application).filter(
                models.Application.agent_id == agent_id,
                models.Application.customer_id == customer_id
            ).first()
            if not application:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Agent with id={agent_id} is not connected to customer with id={customer_id}."
                )
        return agent

    @staticmethod
    def create_agent(db: Session, agent_data: schemas.AgentCreate):
        existing = db.query(models.Agent).filter(models.Agent.email == agent_data.email).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Agent with email={agent_data.email} already exists."
            )
        new_agent = models.Agent(**agent_data.model_dump())
        db.add(new_agent)
        db.commit()
        db.refresh(new_agent)
        return new_agent

    @staticmethod
    def update_agent(db: Session, agent_id: int, update_data: schemas.AgentUpdate):
        agent = db.query(models.Agent).filter(models.Agent.id == agent_id).first()
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent with id={agent_id} not found."
            )
        for field, value in update_data.model_dump(exclude_unset=True).items():
            setattr(agent, field, value)
        db.commit()
        db.refresh(agent)
        return agent
