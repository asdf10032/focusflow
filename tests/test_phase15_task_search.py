from __future__ import annotations

import json
from typing import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app.db.base import Base
from backend.app.db.session import get_db
from backend.app.main import app


@pytest.fixture()
def client() -> Iterator[TestClient]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
    )
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    Base.metadata.create_all(bind=engine)

    def override_get_db() -> Iterator[Session]:
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=engine)


def assert_success_envelope(payload: dict) -> object:
    assert payload["status"] == "success"
    assert "data" in payload
    assert payload["error"] is None
    assert "meta" in payload
    return payload["data"]


def create_project(client: TestClient, name: str) -> dict:
    return assert_success_envelope(
        client.post("/api/v1/projects", json={"name": name, "priority": 5}).json()
    )


def create_task(
    client: TestClient,
    title: str,
    *,
    notes: str | None = None,
    status: str = "todo",
    project_id: int | None = None,
) -> dict:
    payload = {
        "title": title,
        "estimated_minutes": 30,
        "cognitive_load": 5,
        "status": status,
        "project_id": project_id,
    }
    if notes is not None:
        payload["notes"] = notes
    return assert_success_envelope(client.post("/api/v1/tasks", json=payload).json())


def task_titles(payload: object) -> list[str]:
    return [item["title"] for item in payload]


def test_task_create_update_and_list_include_notes(client: TestClient) -> None:
    task = create_task(client, "Capture notes", notes="Initial context")

    assert task["notes"] == "Initial context"

    updated = assert_success_envelope(
        client.put(
            f"/api/v1/tasks/{task['id']}",
            json={"notes": "Updated implementation notes"},
        ).json()
    )
    listed = assert_success_envelope(client.get("/api/v1/tasks").json())

    assert updated["notes"] == "Updated implementation notes"
    assert listed[0]["notes"] == "Updated implementation notes"


def test_task_search_matches_title_case_insensitively(client: TestClient) -> None:
    create_task(client, "Write Launch Brief")
    create_task(client, "Archive receipts")

    payload = assert_success_envelope(client.get("/api/v1/tasks?q=launch").json())

    assert task_titles(payload) == ["Write Launch Brief"]


def test_task_search_matches_notes_case_insensitively(client: TestClient) -> None:
    create_task(client, "Morning admin", notes="Prepare VISA paperwork")
    create_task(client, "Evening admin", notes="Clean inbox")

    payload = assert_success_envelope(client.get("/api/v1/tasks?q=visa").json())

    assert task_titles(payload) == ["Morning admin"]


def test_task_search_composes_with_status_and_project_filters(client: TestClient) -> None:
    project = create_project(client, "Search Project")
    other_project = create_project(client, "Other Project")
    create_task(client, "Draft roadmap", notes="alpha", status="todo", project_id=project["id"])
    create_task(client, "Ship roadmap", notes="alpha", status="done", project_id=project["id"])
    create_task(client, "Draft other", notes="alpha", status="todo", project_id=other_project["id"])

    payload = assert_success_envelope(
        client.get(f"/api/v1/tasks?q=alpha&status=todo&project_id={project['id']}").json()
    )

    assert task_titles(payload) == ["Draft roadmap"]


def test_blank_search_is_ignored(client: TestClient) -> None:
    create_task(client, "First")
    create_task(client, "Second")

    payload = assert_success_envelope(client.get("/api/v1/tasks?q=%20%20").json())

    assert task_titles(payload) == ["Second", "First"]


def test_task_export_includes_notes(client: TestClient) -> None:
    task = create_task(client, "Export note", notes="Portable context")

    export = assert_success_envelope(client.get("/api/v1/exports/tasks").json())
    content = json.loads(export["content"])

    assert export["record_count"] == 1
    assert content[0]["id"] == task["id"]
    assert content[0]["notes"] == "Portable context"
