"""Connector-specific master-data trace coverage against isolated SQLite."""

import pytest
from sqlalchemy import text

from app.db.session import get_session_factory
from app.services.task_trace_service import TaskTraceService
from tests.test_auth import _login, client as client


def headers(client):
    token = _login(client, "admin", "AdminPass123!")["access_token"]
    return {"Authorization": f"Bearer {token}", "x-client-type": "workbuddy_connector",
            "x-client-request-id": "wb_acceptance_master_data"}


@pytest.mark.parametrize("resource", ["brands", "tile-categories"])
def test_connector_master_data_traces_success_and_failure(client, resource):
    auth = headers(client)
    created = client.post(f"/api/v1/admin/{resource}", headers=auth,
                          json={"name": "Synthetic", "sort_order": 1})
    assert created.status_code == 200
    failed = client.put(f"/api/v1/admin/{resource}/999999", headers=auth,
                        json={"name": "PRIVATE-PAYLOAD-MARKER", "sort_order": 2})
    # Use a valid name for the shorter category schema, so the failure is a business 404.
    if resource == "tile-categories":
        failed = client.put(f"/api/v1/admin/{resource}/999999", headers=auth,
                            json={"name": "Synthetic", "sort_order": 2})
    assert failed.status_code == 404
    with get_session_factory()() as session:
        traces = session.execute(text(
            "SELECT t.status, t.actor_user_id, t.parent_request_id, r.request_id, t.summary "
            "FROM task_traces t JOIN request_logs r ON r.request_id = t.parent_request_id "
            "WHERE t.client_type = 'workbuddy_connector'"
        )).all()
        assert len(traces) >= 2
        assert {row.status for row in traces} >= {"success", "failed"}
        assert all(row.actor_user_id and row.parent_request_id == row.request_id for row in traces)
        assert all("PRIVATE-PAYLOAD-MARKER" not in row.summary for row in traces)
        assert session.execute(text("SELECT count(*) FROM task_trace_spans")).scalar_one() >= 5


@pytest.mark.parametrize("resource", ["brands", "tile-categories"])
def test_trace_failure_does_not_change_business_success(client, monkeypatch, resource):
    def unavailable(*args, **kwargs):
        raise RuntimeError("synthetic-telemetry-failure")
    monkeypatch.setattr(TaskTraceService, "record_context_span", unavailable)
    response = client.post(f"/api/v1/admin/{resource}", headers=headers(client),
                           json={"name": "Synthetic", "sort_order": 1})
    assert response.status_code == 200
    assert response.json()["data"]["id"]


@pytest.mark.parametrize("resource", ["brands", "tile-categories"])
def test_normal_client_and_unauthorized_do_not_add_connector_trace(client, resource):
    path = f"/api/v1/admin/{resource}"
    payload = {"name": "Synthetic", "sort_order": 1}
    response = client.post(path, headers={"x-client-type": "workbuddy_connector"}, json=payload)
    assert response.status_code == 401
    auth = headers(client)
    auth["x-client-type"] = "web_admin"
    assert client.post(path, headers=auth, json=payload).status_code == 200
    with get_session_factory()() as session:
        assert session.execute(text("SELECT count(*) FROM task_traces")).scalar_one() == 0
