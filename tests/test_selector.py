from src.selector import (
    TARGET_GROUPS,
    extract_page_info,
    select_topics_per_group,
)

def test_extract_page_info_normal():
    page = {
        "id": "1a29fb09-10fe-42f4-adbb-5ddada0ee6e0",
        "url": "https://www.notion.so/Flutter-Lifecycle-1a29fb0910fe42f4adbb5ddada0ee6e0",
        "properties": {
            "Name": {
                "title": [{"plain_text": "Flutter "}, {"plain_text": "Lifecycle"}]
            },
            "Nhóm kiến thức": {
                "select": {"name": "1. Kiến thức Flutter"}
            },
            "Status": {
                "select": {"name": "Done 🙌"}
            }
        }
    }
    info = extract_page_info(page)
    assert info["id"] == "1a29fb09-10fe-42f4-adbb-5ddada0ee6e0"
    assert info["title"] == "Flutter Lifecycle"
    assert info["url"] == "https://www.notion.so/Flutter-Lifecycle-1a29fb0910fe42f4adbb5ddada0ee6e0"
    assert info["group"] == "1. Kiến thức Flutter"

def test_extract_page_info_missing_fields():
    page = {
        "id": "page-missing",
        "properties": {}
    }
    info = extract_page_info(page)
    assert info["id"] == "page-missing"
    assert info["title"] == "Untitled"
    assert info["url"] == "https://notion.so/pagemissing"
    assert info["group"] is None

def test_select_topics_per_group_one_each():
    pages = [
        {
            "id": "p1",
            "url": "https://notion.so/p1",
            "properties": {
                "Name": {"title": [{"plain_text": "Topic 1A"}]},
                "Nhóm kiến thức": {"select": {"name": "1. Kiến thức Flutter"}},
            }
        },
        {
            "id": "p2",
            "url": "https://notion.so/p2",
            "properties": {
                "Name": {"title": [{"plain_text": "Topic 1B"}]},
                "Nhóm kiến thức": {"select": {"name": "1. Kiến thức Flutter"}},
            }
        },
        {
            "id": "p3",
            "url": "https://notion.so/p3",
            "properties": {
                "Name": {"title": [{"plain_text": "Topic 2A"}]},
                "Nhóm kiến thức": {"select": {"name": "2. Kiến thức hệ thống"}},
            }
        },
        {
            "id": "p4",
            "url": "https://notion.so/p4",
            "properties": {
                "Name": {"title": [{"plain_text": "Topic 3A"}]},
                "Nhóm kiến thức": {"select": {"name": "3. Thư viện bên thứ ba"}},
            }
        },
    ]

    selection = select_topics_per_group(pages, TARGET_GROUPS)
    assert selection["1. Kiến thức Flutter"] is not None
    assert selection["1. Kiến thức Flutter"]["id"] == "p1"
    assert selection["2. Kiến thức hệ thống"]["id"] == "p3"
    assert selection["3. Thư viện bên thứ ba"]["id"] == "p4"

def test_select_topics_per_group_empty_group():
    pages = [
        {
            "id": "p1",
            "url": "https://notion.so/p1",
            "properties": {
                "Name": {"title": [{"plain_text": "Topic 1A"}]},
                "Nhóm kiến thức": {"select": {"name": "1. Kiến thức Flutter"}},
            }
        }
    ]

    selection = select_topics_per_group(pages, TARGET_GROUPS)
    assert selection["1. Kiến thức Flutter"]["id"] == "p1"
    assert selection["2. Kiến thức hệ thống"] is None
    assert selection["3. Thư viện bên thứ ba"] is None


def test_extract_page_info_with_none_values():
    page1 = {"id": None, "url": None, "properties": None}
    info1 = extract_page_info(page1)
    assert info1["id"] == ""
    assert info1["title"] == "Untitled"
    assert info1["url"] == "https://notion.so/"
    assert info1["group"] is None

    page2 = {
        "id": "p2",
        "properties": {
            "Name": {"title": None},
            "Nhóm kiến thức": None,
        }
    }
    info2 = extract_page_info(page2)
    assert info2["id"] == "p2"
    assert info2["title"] == "Untitled"
    assert info2["group"] is None
