"""Cria dados pequenos e reproduzíveis para explorar o banco local."""

from datetime import date

from sqlalchemy.orm import Session

from app.database import Base, make_engine
from app.models import Event, User


def seed(engine):
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        examples = [
            Event(id=1, title="Oficina de Python", date=date(2026, 10, 10), capacity=2),
            User(id=1, name="Ana", email="ana@example.org"),
            User(id=2, name="Bruno", email="bruno@example.org"),
        ]
        for item in examples:
            if session.get(type(item), item.id) is None:
                session.add(item)
        session.commit()


if __name__ == "__main__":
    seed(make_engine())
