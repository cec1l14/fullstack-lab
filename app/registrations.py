"""Rota de inscrição a completar na atividade 3."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db_session import get_session


router = APIRouter()


class RegistrationInput(BaseModel):
    user_id: int


@router.post("/events/{event_id}/registrations", status_code=201)
def register(event_id: int, data: RegistrationInput, session: Session = Depends(get_session)):
    # Atividade 3: verifique evento, usuário, duplicidade e vagas. Só então
    # grave Registration e responda com event_id e user_id.
    raise HTTPException(status_code=501, detail="Inscrição ainda não implementada")
