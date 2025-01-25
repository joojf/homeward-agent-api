from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict


class AgentBase(BaseModel):
    name: str
    email: EmailStr
    phone_number: Optional[str] = None
    location: Optional[str] = None


class AgentCreate(AgentBase):
    pass


class AgentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    location: Optional[str] = None


class AgentOut(AgentBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
