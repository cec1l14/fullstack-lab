"""Sessões usadas pelas rotas da API a partir do checkpoint 3."""

from fastapi import Request
from sqlalchemy.orm import Session

from app.models import Event


def get_session(request: Request):
    """Abre uma sessão para a requisição e a fecha ao responder."""
    with Session(request.app.state.engine) as session:
        yield session


def find_event(session: Session, event_id: int) -> Event | None:
    """Exemplo de consulta por chave primária para usar ou adaptar."""
    return session.get(Event, event_id)
