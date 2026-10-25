"""API de eventos usada em todas as etapas do projeto."""

from datetime import date

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import Base, make_engine
from app.db_session import get_session
from app.models import Event, Registration
from app.registrations import router as registrations_router


class EventInput(BaseModel):
    """Dados enviados pelo cliente ao cadastrar um evento."""

    title: str = Field(min_length=1)
    date: date
    capacity: int = Field(gt=0)


def create_app(database_url: str = "sqlite://") -> FastAPI:
    """Cria uma API; por padrão usa um banco em memória isolado por instância."""
    app = FastAPI(title="Eventos do Trilha")
    engine = make_engine(database_url)
    Base.metadata.create_all(engine)
    app.state.engine = engine

    @app.get("/events")
    def list_events(session: Session = Depends(get_session)):
        result = []
        for event in session.scalars(select(Event).order_by(Event.id)):
            registered = session.scalar(
                select(func.count()).select_from(Registration).where(Registration.event_id == event.id)
            )
            result.append(
                {
                    "id": event.id,
                    "title": event.title,
                    "date": event.date,
                    "capacity": event.capacity,
                    "available_slots": event.capacity - registered,
                }
            )
        return result

    @app.get("/events/{event_id}")
    def get_event(event_id: int, session: Session = Depends(get_session)):
        event = session.get(Event, event_id)
        if event is None:
            raise HTTPException(status_code=404, detail="Evento não encontrado")
        registered = session.scalar(
            select(func.count()).select_from(Registration).where(Registration.event_id == event.id)
        )
        return {
            "id": event.id,
            "title": event.title,
            "date": event.date,
            "capacity": event.capacity,
            "available_slots": event.capacity - registered,
        }

    @app.post("/events", status_code=201)
    def create_event(data: EventInput, session: Session = Depends(get_session)):
        if not data.title:
            raise HTTPException(status_code=422, detail="Título inválido")
        if data.capacity <= 0:
            raise HTTPException(status_code=422, detail="Capacidade inválida")

        event = Event(title=data.title, date=data.date, capacity=data.capacity)
        session.add(event)
        session.commit()
        session.refresh(event)
        return {
            "id": event.id,
            "title": event.title,
            "date": event.date,
            "capacity": event.capacity,
            "available_slots": event.capacity,
        }

    app.include_router(registrations_router)
    return app


app = create_app("sqlite:///events.db")