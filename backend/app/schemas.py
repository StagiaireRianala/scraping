from pydantic import BaseModel, EmailStr,Field
from datetime import datetime
from typing import Optional
class MessageCreate(BaseModel):
    id_conversation: int
    sender: str
    type: str
    message: str

class LoginRequest(BaseModel):
    email: str
    password: str

class UtilisateurCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="Le nom de l'utilisateur")
    email: EmailStr = Field(..., description="Adresse email de l'utilisateur")
    mdp: str = Field(..., min_length=8, max_length=128, description="Mot de passe")

class UtilisateurOut(BaseModel):
    id_utilisateur: int
    name: str
    email: str
    date_creation: datetime = Field(alias="date")
    status: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
