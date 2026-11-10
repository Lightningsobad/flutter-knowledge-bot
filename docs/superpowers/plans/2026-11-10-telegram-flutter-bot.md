# Flutter Knowledge Telegram Bot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a zero-maintenance, public-safe GitHub Actions automation in Python that queries a Notion board for "Done 🙌" Flutter topics, selects 1 topic per knowledge group, sends them to Telegram, and updates their Notion status to "Ôn Tập".

**Architecture:** A lightweight Python script reading environment secrets (`NOTION_TOKEN`, `NOTION_DATABASE_ID`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`) queries the Notion API for pages with `Status == 'Done 🙌'`, groups them by `Nhóm kiến thức`, selects 1 candidate per group, formats and sends an HTML message to Telegram, and then updates the sent pages' status to `Ôn Tập` in Notion. Scheduled daily via GitHub Actions.

**Tech Stack:** Python 3.11+, standard `urllib` / `requests`, `pytest`, GitHub Actions.

**Spec:** [`docs/superpowers/specs/2026-11-10-telegram-flutter-bot-design.md`](file:///d:/flutter-knowledge-bot/docs/superpowers/specs/2026-11-10-telegram-flutter-bot-design.md)

## Global Constraints

- 100% Public Repo Safe: Zero hardcoded secrets, database IDs, or private URLs in code or commits.
- Notion Filter: Exact property name `Status` matching select value `Done 🙌`.
- Target Knowledge Groups: `1. Kiến thức Flutter`, `2. Kiến thức hệ thống`, `3. Thư viện bên thứ ba`.
- Target Transition Status: `Ôn Tập`.
- Schedule: `0 1 * * *` (01:00 UTC = 08:00 AM UTC+7) plus `workflow_dispatch`.

## Review Focus

1. Notion page with empty title or missing properties: Should fall back cleanly without raising unhandled KeyError.
2. Group has 0 candidates with `Done 🙌`: Should still send the available groups and note the empty group instead of crashing.
3. Telegram message fails (non-200): Must NOT update Notion status to "Ôn Tập" (prevent state desync).
4. HTML special characters in article titles (`<`, `>`, `&`): Must be HTML-escaped so Telegram API does not reject formatting.
5. Missing or invalid environment variables: Must exit with descriptive error message before attempting network calls.

---

### Task 1: Project Setup & Test Scaffolding

**Files:**
- Create: `.gitignore`
- Create: `requirements.txt`
- Create: `requirements-dev.txt`

**Interfaces:**
- Produces: Clean virtual environment setup with `pytest` and `requests`.

- [ ] **Step 1: Write `.gitignore` and dependency manifests**
- [ ] **Step 2: Install dependencies into local environment**
  Run: `pip install -r requirements-dev.txt`
  Expected: Successful installation of `pytest`, `requests`.
- [ ] **Step 3: Verify pytest runs empty test suite**
  Run: `pytest`
  Expected: PASS (0 tests or no tests collected).
- [ ] **Step 4: Commit**
  ```bash
  git add .gitignore requirements.txt requirements-dev.txt
  git commit -m "chore: initialize project dependencies and gitignore"
  ```

---

### Task 2: Notion API Client

**Files:**
- Create: `src/notion_client.py`
- Test: `tests/test_notion_client.py`

**Interfaces:**
- Produces:
  - `fetch_done_pages(database_id: str, token: str) -> list[dict]`
  - `update_page_status(page_id: str, status_name: str, token: str) -> bool`

- [ ] **Step 1: Write failing test for Notion fetching and status updating**
  ```python
  def test_fetch_done_pages_parses_results(requests_mock):
      # Mock POST https://api.notion.com/v1/databases/{id}/query
      ...
  def test_update_page_status(requests_mock):
      # Mock PATCH https://api.notion.com/v1/pages/{page_id}
      ...
  ```
- [ ] **Step 2: Run test to verify it fails**
  Run: `pytest tests/test_notion_client.py -v`
  Expected: FAIL with ModuleNotFoundError or import error.
- [ ] **Step 3: Implement `src/notion_client.py`**
  Implement `fetch_done_pages` with `Notion-Version: 2022-06-28` header and filter `{"property": "Status", "select": {"equals": "Done 🙌"}}`.
  Implement `update_page_status` with PATCH payload updating `Status` select property.
- [ ] **Step 4: Run test to verify it passes**
  Run: `pytest tests/test_notion_client.py -v`
  Expected: PASS.
- [ ] **Step 5: Commit**
  ```bash
  git add src/notion_client.py tests/test_notion_client.py
  git commit -m "feat: implement Notion API client for fetching and updating page status"
  ```

---

### Task 3: Knowledge Group Selector

**Files:**
- Create: `src/selector.py`
- Test: `tests/test_selector.py`

**Interfaces:**
- Consumes: Raw Notion page dicts.
- Produces:
  - `TARGET_GROUPS: list[str]`
  - `extract_page_info(page: dict) -> dict`: extracts `id`, `title`, `url`, `group`.
  - `select_topics_per_group(pages: list[dict], target_groups: list[str] = TARGET_GROUPS) -> dict[str, dict | None]`

- [ ] **Step 1: Write failing test for grouping and extraction**
  Test 1: Selects exactly 1 item for each of the 3 groups.
  Test 2: When a group has no candidates, returns `None` for that group without crashing.
  Test 3: Handles page with missing title gracefully.
- [ ] **Step 2: Run test to verify it fails**
  Run: `pytest tests/test_selector.py -v`
  Expected: FAIL with ModuleNotFoundError.
- [ ] **Step 3: Implement `src/selector.py`**
  Implement property parsers for Notion `title`, `select`, and page `url`.
  Group items by `Nhóm kiến thức` and pick the first available candidate for each target group.
- [ ] **Step 4: Run test to verify it passes**
  Run: `pytest tests/test_selector.py -v`
  Expected: PASS.
- [ ] **Step 5: Commit**
  ```bash
  git add src/selector.py tests/test_selector.py
  git commit -m "feat: implement topic selection logic across knowledge groups"
  ```

---

### Task 4: Telegram Message Formatter & Dispatcher

**Files:**
- Create: `src/telegram_client.py`
- Test: `tests/test_telegram_client.py`

**Interfaces:**
- Consumes: Selected topics dictionary from `selector.py`.
- Produces:
  - `format_telegram_message(selection: dict[str, dict | None]) -> str`
  - `send_telegram_message(bot_token: str, chat_id: str, html_text: str) -> bool`

- [ ] **Step 1: Write failing test for Telegram formatting and delivery**
  Test 1: HTML entity escaping (`<`, `>`, `&` in titles are escaped to `&lt;`, `&gt;`, `&amp;`).
  Test 2: Proper formatting when a group has a topic vs when a group is empty.
  Test 3: Telegram API call `POST https://api.telegram.org/bot<token>/sendMessage` with `parse_mode=HTML`.
- [ ] **Step 2: Run test to verify it fails**
  Run: `pytest tests/test_telegram_client.py -v`
  Expected: FAIL.
- [ ] **Step 3: Implement `src/telegram_client.py`**
  Implement `format_telegram_message` with `html.escape` on titles.
  Implement `send_telegram_message` returning `True` on HTTP 200, logging error on non-200.
- [ ] **Step 4: Run test to verify it passes**
  Run: `pytest tests/test_telegram_client.py -v`
  Expected: PASS.
- [ ] **Step 5: Commit**
  ```bash
  git add src/telegram_client.py tests/test_telegram_client.py
  git commit -m "feat: implement Telegram message formatter and sender"
  ```

---

### Task 5: Orchestration Entrypoint (`main.py`)

**Files:**
- Create: `main.py`
- Test: `tests/test_main.py`

**Interfaces:**
- Consumes: Environment variables (`NOTION_TOKEN`, `NOTION_DATABASE_ID`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`).
- Produces: Exit code 0 on success, exit code 1 on configuration or unrecoverable error.

- [ ] **Step 1: Write failing test for main orchestration**
  Test 1: Full success flow: fetches -> selects 3 -> sends Telegram -> updates Notion status for 3 pages.
  Test 2: Telegram fails: does NOT update Notion status.
  Test 3: Missing environment variables: exits with code 1.
- [ ] **Step 2: Run test to verify it fails**
  Run: `pytest tests/test_main.py -v`
  Expected: FAIL.
- [ ] **Step 3: Implement `main.py`**
  Read env variables with clean error reporting.
  Wire `fetch_done_pages` -> `select_topics_per_group` -> `format_telegram_message` -> `send_telegram_message` -> `update_page_status`.
- [ ] **Step 4: Run test to verify it passes**
  Run: `pytest tests/test_main.py -v`
  Expected: PASS.
- [ ] **Step 5: Commit**
  ```bash
  git add main.py tests/test_main.py
  git commit -m "feat: implement end-to-end orchestration in main.py"
  ```

---

### Task 6: GitHub Actions Workflow & Documentation

**Files:**
- Create: `.github/workflows/daily_review.yml`
- Create: `README.md`

**Interfaces:**
- GitHub Actions cron trigger at `0 1 * * *` and `workflow_dispatch`.
- Comprehensive setup guide for the public repository.

- [ ] **Step 1: Create `.github/workflows/daily_review.yml`**
  Set up Python environment, install `requirements.txt`, run `python main.py` passing secrets from `secrets.NOTION_TOKEN`, `secrets.NOTION_DATABASE_ID`, `secrets.TELEGRAM_BOT_TOKEN`, `secrets.TELEGRAM_CHAT_ID`.
- [ ] **Step 2: Create `README.md`**
  Clear, step-by-step instructions:
  1. How to create Telegram Bot via `@BotFather` and obtain `TELEGRAM_BOT_TOKEN` & `TELEGRAM_CHAT_ID`.
  2. How to create Notion Internal Integration, obtain `NOTION_TOKEN`, share the database with the integration with edit access.
  3. How to extract `NOTION_DATABASE_ID`.
  4. How to add the 4 secrets into GitHub Repo Settings -> Secrets and variables -> Actions.
- [ ] **Step 3: Verify all unit tests pass across the entire suite**
  Run: `pytest -v`
  Expected: All tests pass.
- [ ] **Step 4: Commit**
  ```bash
  git add .github/workflows/daily_review.yml README.md
  git commit -m "docs: add GitHub Actions workflow and setup instructions"
  ```

