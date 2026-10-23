from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.main import create_app
from app.models import Registration, User


EVENT = {"title": "Oficina", "date": "2026-10-10", "capacity": 2}


def app_at(tmp_path):
    return create_app(database_url=f"sqlite:///{tmp_path / 'app.db'}")


def add_user(app, user_id=1):
    with Session(app.state.engine) as session:
        session.add(User(id=user_id, name="Ana", email=f"ana{user_id}@example.org"))
        session.commit()


def test_event_survives_new_app_instance(tmp_path):
    with TestClient(app_at(tmp_path)) as api:
        created = api.post("/events", json=EVENT)
        assert created.status_code == 201
        event_id = created.json()["id"]

    with TestClient(app_at(tmp_path)) as api:
        assert api.get(f"/events/{event_id}").json()["title"] == "Oficina"


def test_registration_uses_a_slot_and_persists(tmp_path):
    app = app_at(tmp_path)
    add_user(app)
    with TestClient(app) as api:
        event_id = api.post("/events", json=EVENT).json()["id"]
        response = api.post(f"/events/{event_id}/registrations", json={"user_id": 1})
        assert response.status_code == 201
        assert response.json()["event_id"] == event_id
        assert response.json()["user_id"] == 1
        assert api.get(f"/events/{event_id}").json()["available_slots"] == 1

    with Session(app.state.engine) as session:
        assert len(session.scalars(select(Registration)).all()) == 1


def test_registration_rejects_missing_event_and_user(tmp_path):
    app = app_at(tmp_path)
    with TestClient(app) as api:
        assert api.post("/events/999/registrations", json={"user_id": 1}).status_code == 404
        event_id = api.post("/events", json=EVENT).json()["id"]
        assert api.post(f"/events/{event_id}/registrations", json={"user_id": 999}).status_code == 404


def test_registration_rejects_duplicate_and_full_event(tmp_path):
    app = app_at(tmp_path)
    add_user(app, 1)
    add_user(app, 2)
    with TestClient(app) as api:
        event_id = api.post("/events", json={**EVENT, "capacity": 1}).json()["id"]
        url = f"/events/{event_id}/registrations"
        assert api.post(url, json={"user_id": 1}).status_code == 201
        assert api.post(url, json={"user_id": 1}).status_code == 409
        assert api.post(url, json={"user_id": 2}).status_code == 409
        assert api.get(f"/events/{event_id}").json()["available_slots"] == 0

    with Session(app.state.engine) as session:
        assert len(session.scalars(select(Registration)).all()) == 1
