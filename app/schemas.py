from typing import Optional

from pydantic import BaseModel, EmailStr


class AgentBase(BaseModel):
    name: str
    email: EmailStr
    phone_number: Optional[str] = None
    location: Optional[str] = None


class AgentCreate(AgentBase):
    pass


class AgentUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    phone_number: Optional[str]
    location: Optional[str]


class AgentOut(AgentBase):
    id: int

    class Config:
        from_attributes = True
