import logging
import requests

NOTION_API_VERSION = "2022-06-28"
NOTION_BASE_URL = "https://api.notion.com/v1"
DEFAULT_TIMEOUT = 15

logger = logging.getLogger(__name__)

def _get_headers(token: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_API_VERSION,
        "Content-Type": "application/json",
    }

def fetch_done_pages(database_id: str, token: str) -> list[dict]:
    """Query database for pages where Status == 'Done 🙌'."""
    url = f"{NOTION_BASE_URL}/databases/{database_id}/query"
    payload = {
        "filter": {
            "property": "Status",
            "select": {"equals": "Done 🙌"},
        }
    }
    response = requests.post(url, headers=_get_headers(token), json=payload, timeout=DEFAULT_TIMEOUT)
    if not response.ok:
        raise RuntimeError(f"Notion API error: {response.status_code} - {response.text}")
    return response.json().get("results", [])

def update_page_status(page_id: str, status_name: str, token: str) -> bool:
    """Update a Notion page's Status select property."""
    url = f"{NOTION_BASE_URL}/pages/{page_id}"
    payload = {
        "properties": {
            "Status": {
                "select": {"name": status_name}
            }
        }
    }
    try:
        response = requests.patch(url, headers=_get_headers(token), json=payload, timeout=DEFAULT_TIMEOUT)
        if not response.ok:
            logger.error(f"Failed to update page {page_id} status: {response.status_code} - {response.text}")
            return False
        return True
    except Exception as e:
        logger.error(f"Exception updating page {page_id} status: {e}")
        return False
