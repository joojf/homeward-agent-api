from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app import models, schemas
from app.exceptions import AgentNotFoundError, AgentCustomerConnectionError, DuplicateAgentError


class AgentService:
    @staticmethod
    def get_all_agents(db: Session):
        try:
            return db.query(models.Agent).order_by(models.Agent.id).all()
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error occurred while fetching agents: {str(e)}"
            )

    @staticmethod
    def get_agent(db: Session, agent_id: int, customer_id: int = None):
        try:
            agent = db.query(models.Agent).filter(models.Agent.id == agent_id).first()
            if not agent:
                raise AgentNotFoundError(str(agent_id))

            if customer_id:
                application = db.query(models.Application).filter(
                    models.Application.agent_id == agent_id,
                    models.Application.customer_id == customer_id
                ).first()
                if not application:
                    raise AgentCustomerConnectionError(
                        agent_id=str(agent_id),
                        customer_id=str(customer_id)
                    )
            return agent
        except AgentNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except AgentCustomerConnectionError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error occurred while fetching agent: {str(e)}"
            )

    @staticmethod
    def create_agent(db: Session, agent_data: schemas.AgentCreate):
        try:
            existing = db.query(models.Agent).filter(models.Agent.email == agent_data.email).first()
            if existing:
                raise DuplicateAgentError(f"Agent with email={agent_data.email} already exists.")

            new_agent = models.Agent(**agent_data.model_dump())
            db.add(new_agent)
            db.commit()
            db.refresh(new_agent)
            return new_agent
        except DuplicateAgentError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Database integrity error: {str(e)}"
            )
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error occurred while creating agent: {str(e)}"
            )

    @staticmethod
    def update_agent(db: Session, agent_id: int, update_data: schemas.AgentUpdate):
        try:
            agent = db.query(models.Agent).filter(models.Agent.id == agent_id).first()
            if not agent:
                raise AgentNotFoundError(f"Agent with id={agent_id} not found.")

            for field, value in update_data.model_dump(exclude_unset=True).items():
                setattr(agent, field, value)

            db.commit()
            db.refresh(agent)
            return agent
        except AgentNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Database integrity error: {str(e)}"
            )
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error occurred while updating agent: {str(e)}"
            )
