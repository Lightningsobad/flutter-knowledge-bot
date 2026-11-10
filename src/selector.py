from typing import Any

TARGET_GROUPS = [
    "1. Kiến thức Flutter",
    "2. Kiến thức hệ thống",
    "3. Thư viện bên thứ ba",
]

def extract_page_info(page: dict[str, Any]) -> dict[str, Any]:
    """Extract clean title, id, url, and knowledge group from a Notion page object."""
    page_id = page.get("id") or ""
    url = page.get("url") or f"https://notion.so/{page_id.replace('-', '')}"

    properties = page.get("properties") or {}
    name_prop = properties.get("Name") or properties.get("title") or {}
    title_list = (name_prop.get("title") or []) if isinstance(name_prop, dict) else []
    title = "".join(part.get("plain_text", "") for part in title_list if isinstance(part, dict)).strip() or "Untitled"

    group_prop = properties.get("Nhóm kiến thức") or {}
    group_name = None
    if isinstance(group_prop, dict):
        select_obj = group_prop.get("select") or {}
        if isinstance(select_obj, dict):
            group_name = select_obj.get("name")

    return {
        "id": page_id,
        "title": title,
        "url": url,
        "group": group_name,
    }

def select_topics_per_group(
    pages: list[dict[str, Any]],
    target_groups: list[str] = TARGET_GROUPS,
) -> dict[str, dict[str, Any] | None]:
    """Select 1 candidate topic for each specified target group."""
    group_buckets: dict[str, list[dict[str, Any]]] = {group: [] for group in target_groups}

    for page in pages:
        info = extract_page_info(page)
        group = info.get("group")
        if group in group_buckets:
            group_buckets[group].append(info)

    return {
        group: (group_buckets[group][0] if group_buckets[group] else None)
        for group in target_groups
    }
