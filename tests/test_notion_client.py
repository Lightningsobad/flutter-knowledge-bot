import pytest
import requests_mock
from src.notion_client import fetch_done_pages, update_page_status

def test_fetch_done_pages_success():
    database_id = "test-database-id"
    token = "secret-token"
    expected_results = [
        {
            "id": "page-1",
            "url": "https://notion.so/page-1",
            "properties": {
                "Name": {"title": [{"plain_text": "Widget Lifecycle"}]},
                "Status": {"select": {"name": "Done 🙌"}},
                "Nhóm kiến thức": {"select": {"name": "1. Kiến thức Flutter"}},
            },
        }
    ]

    with requests_mock.Mocker() as m:
        m.post(
            f"https://api.notion.com/v1/databases/{database_id}/query",
            json={"results": expected_results},
            status_code=200,
        )
        results = fetch_done_pages(database_id, token)
        assert results == expected_results
        last_request = m.last_request
        assert last_request.headers["Authorization"] == f"Bearer {token}"
        assert last_request.headers["Notion-Version"] == "2022-06-28"
        assert last_request.json() == {
            "filter": {
                "property": "Status",
                "select": {"equals": "Done 🙌"},
            }
        }

def test_fetch_done_pages_raises_on_error():
    database_id = "test-database-id"
    token = "secret-token"

    with requests_mock.Mocker() as m:
        m.post(
            f"https://api.notion.com/v1/databases/{database_id}/query",
            status_code=401,
            json={"message": "API token is invalid."},
        )
        with pytest.raises(RuntimeError, match="Notion API error: 401"):
            fetch_done_pages(database_id, token)

def test_update_page_status_success():
    page_id = "page-123"
    token = "secret-token"

    with requests_mock.Mocker() as m:
        m.patch(
            f"https://api.notion.com/v1/pages/{page_id}",
            json={"id": page_id},
            status_code=200,
        )
        success = update_page_status(page_id, "Ôn Tập", token)
        assert success is True
        last_request = m.last_request
        assert last_request.headers["Authorization"] == f"Bearer {token}"
        assert last_request.json() == {
            "properties": {
                "Status": {
                    "select": {"name": "Ôn Tập"}
                }
            }
        }

def test_update_page_status_failure_returns_false():
    page_id = "page-123"
    token = "secret-token"

    with requests_mock.Mocker() as m:
        m.patch(
            f"https://api.notion.com/v1/pages/{page_id}",
            status_code=403,
            json={"message": "Forbidden"},
        )
        success = update_page_status(page_id, "Ôn Tập", token)
        assert success is False
