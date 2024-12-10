from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Utilisateur(Base):
    __tablename__ = "utilisateur"

    id_utilisateur = Column(Integer, primary_key=True, index=True, autoincrement=True)  # Ajoutez `autoincrement=True`
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    mdp = Column(String(255), nullable=False)
    date_creation = Column(TIMESTAMP, default=datetime.utcnow)
    status = Column(String(50), default="active")

class Conversation(Base):
    __tablename__ = "conversation"

    id_conversation = Column(Integer, primary_key=True, index=True)
    id_utilisateur = Column(Integer, ForeignKey("utilisateur.id_utilisateur"), nullable=False)
    id_contexte = Column(Integer, ForeignKey("contexte.id_contexte"))
    start_conv = Column(TIMESTAMP, default=datetime.utcnow)

class Contexte(Base):
    __tablename__ = "contexte"

    id_contexte = Column(Integer, primary_key=True, index=True)
    sujet = Column(String(255))
    description = Column(Text)
    date_creation = Column(TIMESTAMP, default=datetime.utcnow)

class Message(Base):
    __tablename__ = "message"

    id_message = Column(Integer, primary_key=True, index=True)
    id_conversation = Column(Integer, ForeignKey("conversation.id_conversation"), nullable=False)
    sender = Column(String(50))
    type = Column(String(50), default="text")
    message = Column(Text)
    timestamp = Column(TIMESTAMP, default=datetime.utcnow)
