# Design Document: Flutter Knowledge Telegram Bot

**Date:** 2026-11-10  
**Status:** In Review  
**Target Path:** `docs/superpowers/specs/2026-11-10-telegram-flutter-bot-design.md`

---

## 1. Intent & The Why
Establish an automated daily habit for reviewing Flutter knowledge. The user has curated learning materials on a Notion Board ("Flutter Knowledge") categorized into 3 distinct knowledge groups. The bot automatically selects 1 completed topic from each group, sends the 3 topics to Telegram every morning, and automatically transitions their status in Notion to "Ôn Tập" to prevent future duplicates.

---

## 2. Goals, Non-Goals & Anti-Goals

### Goals
- Run automatically every day via GitHub Actions cron (08:00 AM UTC+7 / 01:00 UTC).
- Keep repository **100% Public-safe**: All sensitive data (Notion database ID, Notion API token, Telegram token, chat ID) strictly managed via GitHub Secrets with zero hardcoded URLs/IDs in source code.
- Query Notion Database for pages where `Status == "Done 🙌"`.
- Group candidates by the property `Nhóm kiến thức` (Knowledge Group):
  1. `1. Kiến thức Flutter`
  2. `2. Kiến thức hệ thống`
  3. `3. Thư viện bên thứ ba`
- Select exactly **1 topic per group** (up to 3 topics in total per daily message).
- Send a clean Telegram message containing title + direct Notion page URL.
- On successful Telegram delivery, update the `Status` property of the sent pages to `Ôn Tập` in Notion.

### Non-Goals
- Parsing deep block contents inside Notion pages (title + link only).
- Interactive bot chat commands (`/start`, `/quiz`, etc.).
- External databases or git-commit state tracking.

### Anti-Goals
- Leaking private Notion links or database IDs in public code or commit history.
- Transitioning Notion status before confirming successful Telegram message delivery.

---

## 3. Approaches Considered

1. **GitHub Actions Scheduled Workflow + Python (Chosen)**
   - *Why chosen:* 0 cost, zero server maintenance, native GitHub Secrets management for public repos, runs reliably once per day.
   - *Trade-off:* Scheduled cron can jitter by 5-15 minutes during GitHub peak loads (acceptable for daily morning digests).

2. **Self-Hosted Service / Local Cron (Rejected)**
   - *Trade-off:* High maintenance, requires always-on machine or paid VPS.

---

## 4. Architecture & Security Specifications

### 4.1 Security for Public Repository
All credentials and workspace identifiers MUST be injected via environment variables (GitHub Secrets):
- `NOTION_TOKEN`: Internal Notion integration token with read & write capabilities.
- `NOTION_DATABASE_ID`: 32-character Notion database identifier.
- `TELEGRAM_BOT_TOKEN`: Secret token from `@BotFather`.
- `TELEGRAM_CHAT_ID`: Recipient Telegram chat ID.

No URLs referencing the user's workspace, database IDs, or tokens may appear in source code or default configuration files.

### 4.2 Selection & Grouping Logic
1. Call Notion API: `POST /v1/databases/{NOTION_DATABASE_ID}/query` with filter:
   - `Status` equals `Done 🙌`.
2. Group returned pages by `Nhóm kiến thức` property.
3. For each of the 3 target groups:
   - Pick 1 candidate (first available, or random if multiple exist).
4. Edge Case Handling:
   - If a group has 0 `Done 🙌` items, proceed with available groups and optionally note in the digest (e.g. "Nhóm kiến thức hệ thống: Đã hết bài mới").

### 4.3 Telegram Delivery Format
- Uses Telegram HTML mode for clean, bulleted styling without Markdown escaping traps.
- Template:
  ```html
  📚 <b>ÔN TẬP FLUTTER HÔM NAY</b>

  🔹 <b>1. Kiến thức Flutter:</b>
  • <a href="{url}">{title}</a>

  🔹 <b>2. Kiến thức hệ thống:</b>
  • <a href="{url}">{title}</a>

  🔹 <b>3. Thư viện bên thứ ba:</b>
  • <a href="{url}">{title}</a>
  ```

### 4.4 Notion Status Update (Write Action)
- Only executed after HTTP status 200 is confirmed from Telegram `sendMessage`.
- For each sent page ID, call Notion API: `PATCH /v1/pages/{page_id}`:
  ```json
  {
    "properties": {
      "Status": {
        "select": { "name": "Ôn Tập" }
      }
    }
  }
  ```
- Any failure in update is logged with error trace without terminating already sent deliveries.

---

## 5. What's Left to the Builder
- Python script implementation (`main.py` using `requests` or `urllib.request`).
- `.github/workflows/daily_review.yml` with cron schedule and `workflow_dispatch` trigger for manual on-demand execution.
- `.gitignore` (standard Python + `.env`).
- Clear setup guide in `README.md` instructing the user how to configure Notion integration permissions and add the 4 GitHub Secrets.
