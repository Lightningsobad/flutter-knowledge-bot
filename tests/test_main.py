from unittest.mock import patch
from main import run_daily_job

def test_run_daily_job_missing_env():
    # When required env vars are missing
    code = run_daily_job(env={})
    assert code == 1

def test_run_daily_job_success():
    env = {
        "NOTION_TOKEN": "mock-notion-token",
        "NOTION_DATABASE_ID": "mock-db-id",
        "TELEGRAM_BOT_TOKEN": "mock-tg-token",
        "TELEGRAM_CHAT_ID": "mock-chat-id",
    }
    mock_pages = [
        {
            "id": "p1",
            "url": "https://notion.so/p1",
            "properties": {
                "Name": {"title": [{"plain_text": "Flutter Topic"}]},
                "Nhóm kiến thức": {"select": {"name": "1. Kiến thức Flutter"}},
            }
        }
    ]

    with patch("main.fetch_done_pages", return_value=mock_pages) as mock_fetch, \
         patch("main.send_telegram_message", return_value=True) as mock_send, \
         patch("main.update_page_status", return_value=True) as mock_update:

        code = run_daily_job(env=env)
        assert code == 0
        mock_fetch.assert_called_once_with("mock-db-id", "mock-notion-token")
        mock_send.assert_called_once()
        mock_update.assert_called_once_with("p1", "Ôn Tập", "mock-notion-token")

def test_run_daily_job_telegram_failure_does_not_update_notion():
    env = {
        "NOTION_TOKEN": "mock-notion-token",
        "NOTION_DATABASE_ID": "mock-db-id",
        "TELEGRAM_BOT_TOKEN": "mock-tg-token",
        "TELEGRAM_CHAT_ID": "mock-chat-id",
    }
    mock_pages = [
        {
            "id": "p1",
            "url": "https://notion.so/p1",
            "properties": {
                "Name": {"title": [{"plain_text": "Flutter Topic"}]},
                "Nhóm kiến thức": {"select": {"name": "1. Kiến thức Flutter"}},
            }
        }
    ]

    with patch("main.fetch_done_pages", return_value=mock_pages), \
         patch("main.send_telegram_message", return_value=False) as mock_send, \
         patch("main.update_page_status") as mock_update:

        code = run_daily_job(env=env)
        assert code == 1
        mock_send.assert_called_once()
        mock_update.assert_not_called()


def test_run_daily_job_notion_update_failure_returns_1():
    env = {
        "NOTION_TOKEN": "mock-notion-token",
        "NOTION_DATABASE_ID": "mock-db-id",
        "TELEGRAM_BOT_TOKEN": "mock-tg-token",
        "TELEGRAM_CHAT_ID": "mock-chat-id",
    }
    mock_pages = [
        {
            "id": "p1",
            "url": "https://notion.so/p1",
            "properties": {
                "Name": {"title": [{"plain_text": "Flutter Topic"}]},
                "Nhóm kiến thức": {"select": {"name": "1. Kiến thức Flutter"}},
            }
        }
    ]

    with patch("main.fetch_done_pages", return_value=mock_pages), \
         patch("main.send_telegram_message", return_value=True), \
         patch("main.update_page_status", return_value=False) as mock_update:

        code = run_daily_job(env=env)
        assert code == 1
        mock_update.assert_called_once_with("p1", "Ôn Tập", "mock-notion-token")
