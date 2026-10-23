"""Configuração compartilhada do SQLite; os modelos ficam em ``app.models``."""

from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import StaticPool


class Base(DeclarativeBase):
    pass


def make_engine(url: str = "sqlite:///events.db"):
    """Cria uma conexão com verificação de chaves estrangeiras ativa."""
    options = {"poolclass": StaticPool} if url == "sqlite://" else {}
    engine = create_engine(url, connect_args={"check_same_thread": False}, **options)

    @event.listens_for(engine, "connect")
    def enable_foreign_keys(connection, _):
        connection.execute("PRAGMA foreign_keys=ON")

    return engine
