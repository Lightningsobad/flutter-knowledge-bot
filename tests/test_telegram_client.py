import requests_mock
from src.telegram_client import format_telegram_message, send_telegram_message

def test_format_telegram_message_normal():
    selection = {
        "1. Kiến thức Flutter": {
            "title": "Widget Lifecycle & BuildContext",
            "url": "https://notion.so/lifecycle",
        },
        "2. Kiến thức hệ thống": {
            "title": "Dart Event Loop <Microtask>",
            "url": "https://notion.so/event-loop",
        },
        "3. Thư viện bên thứ ba": {
            "title": "Dio & Retrofit",
            "url": "https://notion.so/dio",
        },
    }

    message = format_telegram_message(selection)
    assert "<b>ÔN TẬP FLUTTER HÔM NAY</b>" in message
    assert '<a href="https://notion.so/lifecycle">Widget Lifecycle &amp; BuildContext</a>' in message
    assert '<a href="https://notion.so/event-loop">Dart Event Loop &lt;Microtask&gt;</a>' in message
    assert '<a href="https://notion.so/dio">Dio &amp; Retrofit</a>' in message

def test_format_telegram_message_with_empty_group():
    selection = {
        "1. Kiến thức Flutter": {
            "title": "StatefulWidget",
            "url": "https://notion.so/sfw",
        },
        "2. Kiến thức hệ thống": None,
    }

    message = format_telegram_message(selection)
    assert '<a href="https://notion.so/sfw">StatefulWidget</a>' in message
    assert "<i>(Tạm thời hết bài mới)</i>" in message

def test_send_telegram_message_success():
    bot_token = "123456:ABC-DEF"
    chat_id = "987654321"
    text = "Hello Telegram"

    with requests_mock.Mocker() as m:
        m.post(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            json={"ok": True, "result": {"message_id": 100}},
            status_code=200,
        )
        success = send_telegram_message(bot_token, chat_id, text)
        assert success is True
        last_request = m.last_request
        assert last_request.json() == {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
        }

def test_send_telegram_message_failure():
    bot_token = "123456:ABC-DEF"
    chat_id = "987654321"
    text = "Hello Telegram"

    with requests_mock.Mocker() as m:
        m.post(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            json={"ok": False, "description": "Chat not found"},
            status_code=400,
        )
        success = send_telegram_message(bot_token, chat_id, text)
        assert success is False


def test_format_telegram_message_with_none_title_and_url():
    selection = {
        "1. Kiến thức Flutter": {
            "title": None,
            "url": None,
        }
    }
    message = format_telegram_message(selection)
    assert "Untitled" in message
