import os
import sys
import logging
from typing import Mapping

from src.notion_client import fetch_done_pages, update_page_status
from src.selector import select_topics_per_group, TARGET_GROUPS
from src.telegram_client import format_telegram_message, send_telegram_message

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

REQUIRED_ENV_VARS = [
    "NOTION_TOKEN",
    "NOTION_DATABASE_ID",
    "TELEGRAM_BOT_TOKEN",
    "TELEGRAM_CHAT_ID",
]

def run_daily_job(env: Mapping[str, str] | None = None) -> int:
    config = os.environ if env is None else env

    missing = [var for var in REQUIRED_ENV_VARS if not config.get(var)]
    if missing:
        logger.error(f"Missing required environment variables: {', '.join(missing)}")
        return 1

    notion_token = config["NOTION_TOKEN"]
    database_id = config["NOTION_DATABASE_ID"]
    telegram_bot_token = config["TELEGRAM_BOT_TOKEN"]
    telegram_chat_id = config["TELEGRAM_CHAT_ID"]

    logger.info("Fetching 'Done 🙌' pages from Notion database...")
    try:
        pages = fetch_done_pages(database_id, notion_token)
    except Exception as e:
        logger.error(f"Failed to query Notion database: {e}")
        return 1

    logger.info(f"Found {len(pages)} candidate pages with status 'Done 🙌'.")
    selection = select_topics_per_group(pages, TARGET_GROUPS)

    # Format Telegram message
    message = format_telegram_message(selection)

    logger.info("Sending daily digest to Telegram...")
    if not send_telegram_message(telegram_bot_token, telegram_chat_id, message):
        logger.error("Failed to deliver Telegram message. Aborting Notion status update.")
        return 1

    logger.info("Telegram message delivered successfully.")

    # Update Notion status to 'Ôn Tập' for each selected topic
    for group, item in selection.items():
        if item and item.get("id"):
            page_id = item["id"]
            title = item.get("title", "")
            logger.info(f"Updating Notion status for page: {title} ({page_id}) -> 'Ôn Tập'")
            update_page_status(page_id, "Ôn Tập", notion_token)

    logger.info("Daily job finished successfully.")
    return 0

if __name__ == "__main__":
    sys.exit(run_daily_job())
