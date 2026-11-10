<div align="center">

# Flutter Knowledge Telegram Bot 🚀

Bot tự động gửi tin nhắn ôn tập kiến thức Flutter mỗi ngày vào Telegram cá nhân từ bảng Notion của bạn, chạy tự động 100% miễn phí qua **GitHub Actions**.

[English](README.md) | [Tiếng Việt](README.vn.md)

</div>

---

## 📌 Cách Thức Hoạt Động

1. **Lịch chạy tự động:** 08:00 sáng hàng ngày (giờ Việt Nam, tương ứng `01:00 UTC`).
2. **Bộ lọc kiến thức:** Quét bảng Notion lấy các bài có `Status` là `Done 🙌`.
3. **Phân nhóm thông minh:** Chọn đúng **1 bài cho mỗi nhóm kiến thức**:
   * `1. Kiến thức Flutter`
   * `2. Kiến thức hệ thống`
   * `3. Thư viện bên thứ ba`
4. **Gửi tin nhắn Telegram:** Định dạng HTML gọn gàng, hiển thị tiêu đề và link trực tiếp mở bài Notion.
5. **Cập nhật trạng thái:** Sau khi Telegram xác nhận gửi thành công, bot tự động cập nhật `Status` của các bài vừa gửi sang cột `Ôn Tập` trên Notion để không bị gửi lặp lại trong các ngày sau.

---

## 🛠 Hướng Dẫn Cấu Hình Chi Tiết

Để bot hoạt động, bạn chỉ cần chuẩn bị **4 thông tin bí mật (Secrets)**:

### 1. Lấy `NOTION_TOKEN` & Kết nối Notion
1. Truy cập [Notion Developers - My Integrations](https://www.notion.so/my-integrations).
2. Bấm **New integration**:
   * Đặt tên gợi nhớ (ví dụ: `Flutter Bot`).
   * Chọn đúng Workspace chứa bảng Notion của bạn.
   * Phần **Capabilities**: Bật **Read content** và **Update content**.
3. Bấm **Save** và sao chép **Internal Integration Secret** (có dạng `secret_xxxxxxxx...`). Đây chính là `NOTION_TOKEN`.
4. **QUAN TRỌNG (Cấp quyền cho trang Notion):**
   * Mở trang Notion bảng kiến thức của bạn.
   * Bấm vào nút dấu ba chấm `...` ở góc trên bên phải màn hình -> chọn **Connections** (hoặc mở popup **Share**).
   * Tìm và chọn Integration bạn vừa tạo (ví dụ `Flutter Bot`) rồi bấm **Confirm** để mời bot vào bảng.

---

### 2. Lấy `NOTION_DATABASE_ID`
* Mở bảng Notion trên trình duyệt, đường link sẽ có dạng:
  ```
  https://www.notion.so/workspace/<DATABASE_ID>?v=<VIEW_ID>
  ```
  hoặc
  ```
  https://app.notion.com/p/<DATABASE_ID>?v=<VIEW_ID>...
  ```
* Chuỗi 32 ký tự (chữ và số) nằm ngay trước dấu `?v=` chính là `NOTION_DATABASE_ID`.  
  *(Ví dụ: `b5188acb4fbb45049e9a4c5f93059c5a` hoặc `1a29fb0910fe42f4adbb5ddada0ee6e0`)*.

---

### 3. Lấy `TELEGRAM_BOT_TOKEN`
1. Mở ứng dụng Telegram, tìm bot [@BotFather](https://t.me/botfather).
2. Gửi lệnh `/newbot`, sau đó làm theo hướng dẫn để đặt tên và username cho bot của bạn.
3. BotFather sẽ trả về một token API có dạng: `123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ`. Đây là `TELEGRAM_BOT_TOKEN`.
4. **Lưu ý:** Tìm kiếm bot của bạn trên Telegram và bấm nút **Start** (`/start`) để mở luồng chat với bot.

---

### 4. Lấy `TELEGRAM_CHAT_ID`
1. Tìm bot [@userinfobot](https://t.me/userinfobot) hoặc [@getmyid_bot](https://t.me/getmyid_bot) trên Telegram và bấm **Start**.
2. Bot sẽ gửi lại thông tin cá nhân của bạn. Dòng `Id:` (chuỗi số, ví dụ `123456789`) chính là `TELEGRAM_CHAT_ID` của bạn.

---

## 🔐 Cài Đặt GitHub Secrets (Trên GitHub Repo)

1. Mở Repository này trên GitHub.
2. Vào **Settings** -> Mục bên trái chọn **Secrets and variables** -> Chọn **Actions**.
3. Bấm nút **New repository secret** và thêm lần lượt 4 biến sau:

| Secret Name | Giá trị mẫu / Mô tả |
|---|---|
| `NOTION_TOKEN` | `secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxx` |
| `NOTION_DATABASE_ID` | `b5188acb4fbb45049e9a4c5f93059c5a` |
| `TELEGRAM_BOT_TOKEN` | `123456789:ABCdefGhIJK...` |
| `TELEGRAM_CHAT_ID` | `987654321` |

---

## ⚡ Kiểm Tra Chạy Thử Ngay (Test Manual)

Bạn không cần chờ đến 8:00 sáng để kiểm tra:
1. Trên repo GitHub, vào tab **Actions**.
2. Ở danh sách bên trái, chọn workflow **Daily Flutter Review Bot**.
3. Bấm vào nút **Run workflow** -> Chọn branch `main` -> Bấm nút xanh **Run workflow**.
4. Chờ khoảng 15-30 giây, kiểm tra Telegram để nhận tin nhắn và mở Notion để thấy các bài vừa gửi đã tự động chuyển sang cột `Ôn Tập`!

---

## 💻 Chạy Thử Trên Máy Cục Bộ (Local)

Nếu bạn muốn chạy thử trực tiếp trên máy tính:
1. Cài đặt thư viện:
   ```bash
   pip install -r requirements.txt
   ```
2. Thiết lập biến môi trường (Windows PowerShell):
   ```powershell
   $env:NOTION_TOKEN="secret_..."
   $env:NOTION_DATABASE_ID="b518..."
   $env:TELEGRAM_BOT_TOKEN="1234..."
   $env:TELEGRAM_CHAT_ID="987..."
   python main.py
   ```
3. Chạy toàn bộ Unit Tests:
   ```bash
   python -m pytest -v
   ```
