"""Rota de inscrição a completar na atividade 3."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db_session import get_session
from app.models import Event, Registration, User


router = APIRouter()


class RegistrationInput(BaseModel):
    user_id: int


@router.post("/events/{event_id}/registrations", status_code=201)
def register(event_id: int, data: RegistrationInput, session: Session = Depends(get_session)):
    # Atividade 3: verifique evento, usuário, duplicidade e vagas. Só então
    # grave Registration e responda com event_id e user_id.
    event = session.get(Event, event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Evento não encontrado")

    if session.get(User, data.user_id) is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    already_registered = session.scalar(
        select(Registration).where(
            Registration.event_id == event_id, Registration.user_id == data.user_id
        )
    )
    if already_registered is not None:
        raise HTTPException(status_code=409, detail="Usuário já inscrito")

    registered = session.scalar(
        select(func.count()).select_from(Registration).where(Registration.event_id == event_id)
    )
    if registered >= event.capacity:
        raise HTTPException(status_code=409, detail="Evento lotado")

    session.add(Registration(event_id=event_id, user_id=data.user_id))
    session.commit()
    return {"event_id": event_id, "user_id": data.user_id}
