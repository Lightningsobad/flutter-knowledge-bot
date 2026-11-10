import html
import logging
from typing import Any
import requests

logger = logging.getLogger(__name__)

def format_telegram_message(selection: dict[str, dict[str, Any] | None]) -> str:
    """Format selected topics into clean Telegram HTML message."""
    lines = [
        "📚 <b>ÔN TẬP FLUTTER HÔM NAY</b>",
        "",
    ]
    for group, item in selection.items():
        escaped_group = html.escape(group)
        lines.append(f"🔹 <b>{escaped_group}:</b>")
        if item:
            title = item.get("title") or "Untitled"
            escaped_title = html.escape(title)
            raw_url = (item.get("url") or "").strip()
            if raw_url:
                escaped_url = html.escape(raw_url, quote=True)
                lines.append(f'• <a href="{escaped_url}">{escaped_title}</a>')
            else:
                lines.append(f"• {escaped_title}")
        else:
            lines.append("• <i>(Tạm thời hết bài mới)</i>")
        lines.append("")

    return "\n".join(lines).strip()

def send_telegram_message(bot_token: str, chat_id: str, html_text: str) -> bool:
    """Send HTML message via Telegram Bot API."""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": html_text,
        "parse_mode": "HTML",
    }
    try:
        response = requests.post(url, json=payload, timeout=15)
        if not response.ok:
            logger.error(f"Telegram API error: {response.status_code} - {response.text}")
            return False
        return True
    except Exception as e:
        logger.error(f"Telegram connection error: {e}")
        return False
