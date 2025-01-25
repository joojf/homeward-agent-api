from typing import Optional, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import AgentCreate, AgentUpdate, AgentOut
from app.services.agent_service import AgentService

router = APIRouter(prefix="/agents", tags=["Agents"])


@router.get("", response_model=List[AgentOut])
def get_all_agents(db: Session = Depends(get_db)):
    return AgentService.get_all_agents(db)


@router.get("/{agent_id}", response_model=AgentOut)
def get_agent(agent_id: int, customer_id: Optional[int] = None, db: Session = Depends(get_db)):
    return AgentService.get_agent(db, agent_id, customer_id)


@router.post("", response_model=AgentOut, status_code=201)
def create_agent(agent_data: AgentCreate, db: Session = Depends(get_db)):
    return AgentService.create_agent(db, agent_data)


@router.patch("/{agent_id}", response_model=AgentOut)
def patch_agent(agent_id: int, update_data: AgentUpdate, db: Session = Depends(get_db)):
    return AgentService.update_agent(db, agent_id, update_data)
