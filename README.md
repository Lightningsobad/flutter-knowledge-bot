<div align="center">

# Flutter Knowledge Telegram Bot 🚀

An automated Telegram bot that delivers daily Flutter review topics from your Notion board, running 100% free via **GitHub Actions**.

[English](README.md) | [Tiếng Việt](README.vn.md)

</div>

---

## 📌 How It Works

1. **Daily Schedule:** Runs every morning at 08:00 AM UTC+7 (`01:00 UTC`).
2. **Status Filter:** Queries Notion for topics marked as `Done 🙌`.
3. **Smart Categorization:** Picks exactly **1 topic from each knowledge group**:
   * `1. Kiến thức Flutter` (Flutter Core)
   * `2. Kiến thức hệ thống` (System / Architecture)
   * `3. Thư viện bên thứ ba` (Third-Party Packages)
4. **Telegram Digest:** Sends a clean HTML-formatted message with direct Notion links.
5. **State Transition:** Automatically updates the status of delivered topics to `Ôn Tập` (Review) in Notion to prevent duplicates in future runs.

---

## 🛠 Configuration & Setup

You only need **4 secrets** configured in your GitHub repository:

### 1. `NOTION_TOKEN` & Connect Integration
1. Visit [Notion Developers - My Integrations](https://www.notion.so/my-integrations).
2. Click **New integration**:
   * Set a name (e.g., `Flutter Bot`).
   * Select the workspace containing your Notion board.
   * Under **Capabilities**, enable both **Read content** and **Update content**.
3. Click **Save** and copy the **Internal Integration Secret** (`secret_...`). This is your `NOTION_TOKEN`.
4. **IMPORTANT (Grant Board Access):**
   * Open your Flutter Knowledge Notion board in your browser.
   * Click the `...` menu in the top-right corner -> select **Connections** (or open **Share**).
   * Search for your integration name (`Flutter Bot`) and click **Confirm** to invite the bot.

---

### 2. `NOTION_DATABASE_ID`
* Open your Notion board in a web browser. The URL will look like:
  ```
  https://www.notion.so/workspace/<DATABASE_ID>?v=<VIEW_ID>
  ```
  or
  ```
  https://app.notion.com/p/<DATABASE_ID>?v=<VIEW_ID>...
  ```
* The 32-character alphanumeric string right before `?v=` is your `NOTION_DATABASE_ID`.

---

### 3. `TELEGRAM_BOT_TOKEN`
1. Open Telegram and search for [@BotFather](https://t.me/botfather).
2. Send `/newbot` and follow the prompts to choose a name and username.
3. BotFather will provide an API token (`123456789:ABCdefGhIJK...`). This is `TELEGRAM_BOT_TOKEN`.
4. **Note:** Open a chat with your new bot and click **Start** (`/start`).

---

### 4. `TELEGRAM_CHAT_ID`
1. Search for [@userinfobot](https://t.me/userinfobot) or [@getmyid_bot](https://t.me/getmyid_bot) on Telegram and click **Start**.
2. Copy the numeric ID from the `Id:` field (e.g., `987654321`). This is `TELEGRAM_CHAT_ID`.

---

## 🔐 GitHub Secrets Setup (Public Repository Safe)

1. Open your repository on GitHub.
2. Go to **Settings** -> **Secrets and variables** -> **Actions**.
3. Click **New repository secret** and add the following 4 secrets:

| Secret Name | Description / Example |
|---|---|
| `NOTION_TOKEN` | `secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxx` |
| `NOTION_DATABASE_ID` | `b5188acb4fbb45049e9a4c5f93059c5a` |
| `TELEGRAM_BOT_TOKEN` | `123456789:ABCdefGhIJK...` |
| `TELEGRAM_CHAT_ID` | `987654321` |

---

## ⚡ Manual Testing (Run On-Demand)

You don't need to wait for 8:00 AM:
1. Go to the **Actions** tab on your GitHub repository.
2. In the left sidebar, click the **Daily Flutter Review Bot** workflow.
3. Click **Run workflow** -> select branch `main` -> click the green **Run workflow** button.
4. Within 15-30 seconds, check your Telegram for the digest and verify in Notion that the sent topics transitioned to `Ôn Tập`!

---

## 💻 Local Development & Testing

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run with environment variables (PowerShell)
$env:NOTION_TOKEN="secret_..."
$env:NOTION_DATABASE_ID="b518..."
$env:TELEGRAM_BOT_TOKEN="1234..."
$env:TELEGRAM_CHAT_ID="987..."
python main.py

# 3. Run unit tests
pip install -r requirements-dev.txt
python -m pytest -v
```
