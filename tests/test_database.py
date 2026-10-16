from pathlib import Path

import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from app.database import Base, make_engine
from database.seed import seed
import app.models  # noqa: F401 — registra as tabelas na metadata


def database(tmp_path):
    engine = make_engine(f"sqlite:///{tmp_path / 'events.db'}")
    Base.metadata.create_all(engine)
    return engine


def populate(engine):
    with engine.begin() as connection:
        connection.execute(text("INSERT INTO events (id, title, date, capacity) VALUES (1, 'Oficina', '2026-10-10', 2)"))
        connection.execute(text("INSERT INTO users (id, name, email) VALUES (1, 'Ana', 'ana@example.org'), (2, 'Bruno', 'bruno@example.org')"))


def test_stores_events_users_and_registrations(tmp_path):
    engine = database(tmp_path)
    populate(engine)
    with engine.begin() as connection:
        connection.execute(text("INSERT INTO registrations (event_id, user_id) VALUES (1, 1)"))
        assert connection.scalar(text("SELECT COUNT(*) FROM registrations")) == 1


def test_rejects_duplicate_registration(tmp_path):
    engine = database(tmp_path)
    populate(engine)
    with engine.begin() as connection:
        connection.execute(text("INSERT INTO registrations (event_id, user_id) VALUES (1, 1)"))
    with pytest.raises(IntegrityError):
        with engine.begin() as connection:
            connection.execute(text("INSERT INTO registrations (event_id, user_id) VALUES (1, 1)"))


def test_rejects_missing_references_and_invalid_capacity(tmp_path):
    engine = database(tmp_path)
    populate(engine)
    with pytest.raises(IntegrityError):
        with engine.begin() as connection:
            connection.execute(text("INSERT INTO registrations (event_id, user_id) VALUES (999, 1)"))
    with pytest.raises(IntegrityError):
        with engine.begin() as connection:
            connection.execute(text("INSERT INTO registrations (event_id, user_id) VALUES (1, 999)"))
    with pytest.raises(IntegrityError):
        with engine.begin() as connection:
            connection.execute(text("INSERT INTO events (title, date, capacity) VALUES ('Inválido', '2026-10-10', 0)"))


def test_participants_query_returns_names(tmp_path):
    engine = database(tmp_path)
    populate(engine)
    with engine.begin() as connection:
        connection.execute(text("INSERT INTO registrations (event_id, user_id) VALUES (1, 1), (1, 2)"))
        query = Path("database/participants.sql").read_text()
        names = connection.execute(text(query), {"event_id": 1}).scalars().all()
        assert names == ["Ana", "Bruno"]


def test_seed_preserves_existing_event_and_adds_missing_users(tmp_path):
    engine = database(tmp_path)
    with engine.begin() as connection:
        connection.execute(text("INSERT INTO events (id, title, date, capacity) VALUES (1, 'Meu evento', '2026-10-10', 2)"))
    seed(engine)
    seed(engine)
    with engine.connect() as connection:
        assert connection.scalar(text("SELECT title FROM events WHERE id = 1")) == "Meu evento"
        assert connection.scalar(text("SELECT COUNT(*) FROM users")) == 2
