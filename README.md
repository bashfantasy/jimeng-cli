# jimeng-cli

即夢（Jimeng）AI 圖片生成 CLI 工具，專為 **無 X-Window 的 Ubuntu VPS** 環境設計。

透過 headless Playwright + Chromium，自動化完成：
- 抖音 QR Code 掃碼登入
- 即夢 AI 圖片生成（提示詞輸入 → 等待生成 → 自動存檔 4 張圖）
- 安全登出並清除本機 Session

---

## 系統需求

- Ubuntu 22.04+（無 X-Window 的 VPS 環境）
- Python ≥ 3.10
- [uv](https://github.com/astral-sh/uv)（Python 套件管理器）

---

## 安裝步驟（VPS Ubuntu）

### 1. 安裝 uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.local/bin/env
```

### 2. 複製專案

```bash
git clone <repo-url> ~/jimeng-cli
cd ~/jimeng-cli
```

### 3. 安裝 Python 依賴

```bash
uv sync
```

### 4. 安裝 Playwright Chromium 瀏覽器

```bash
# 安裝 Playwright Python 套件（如未隨 uv sync 安裝）
uv run playwright install chromium

# 安裝 Chromium 的系統依賴（Ubuntu 必要步驟）
uv run playwright install-deps chromium
```

> **提示**：若 VPS 已有 `~/.cache/ms-playwright/` 目錄，則 Chromium 已下載，可略過 `playwright install` 步驟。

### 5. 驗證安裝

```bash
uv run jimeng --help
```

---

## 使用方式

### 登入（QR Code 掃碼）

```bash
uv run jimeng login
```

執行後會：
1. 開啟即夢 OAuth 登入頁（headless）
2. 截圖 QR Code 存至 `~/.openclaw/media/browser/qrcode.png`
3. 等待您用**抖音 App** 掃碼（最多 120 秒）
4. 登入成功後將 Session 存至 `~/.jimeng/session.json`

**如何取得 QR Code 圖片？**

VPS 上沒有螢幕，您可以用 scp/rsync 將圖片傳到本機後掃碼：

```bash
# 在本機執行（將 qrcode.png 下載至當前目錄）
scp claw:~/.openclaw/media/browser/qrcode.png .
open qrcode.png   # macOS
```

或直接在 VPS 上指定到 NFS / Samba 掛載目錄。

**可用選項：**

```bash
uv run jimeng login --output-dir /path/to/output --timeout 180 --verbose
```

---

### 生成圖片

```bash
uv run jimeng generate "一幅油畫風格的台北夜景"
```

執行後會：
1. 還原已登入的 Session
2. 開啟即夢生圖頁，關閉任何彈窗
3. 確認創作模式為「圖片生成」（若為 Agent 模式則自動重新整理）
4. 輸入提示詞並送出
5. 等待 4 張圖片生成完成後自動下載存檔

**存檔路徑：**

```
~/.openclaw/media/browser/image_1.png
~/.openclaw/media/browser/image_2.png
~/.openclaw/media/browser/image_3.png
~/.openclaw/media/browser/image_4.png
```

**可用選項：**

```bash
uv run jimeng generate "prompt" \
  --output-dir /path/to/output \
  --timeout 240 \
  --verbose
```

---

### 登出

```bash
uv run jimeng logout
```

登出後會清除 `~/.jimeng/session.json`，下次使用需重新 `jimeng login`。

---

## 目錄結構

```
jimeng-cli/
├── src/
│   └── jimeng_cli/
│       ├── __init__.py
│       ├── main.py          # CLI 入口點（Typer）
│       ├── browser.py       # 瀏覽器管理（Playwright + session 持久化）
│       ├── selectors.py     # CSS 選擇器常數（集中管理，易於維護）
│       └── commands/
│           ├── __init__.py
│           ├── login.py     # 登入命令
│           ├── generate.py  # 生圖命令
│           └── logout.py    # 登出命令
├── pyproject.toml
└── README.md
```

---

## 常見問題

### Session 過期

```
Session 已過期，頁面跳轉至登入頁。
請重新執行 `jimeng login`。
```

重新執行 `uv run jimeng login` 即可。

### 找不到 QR Code 元素

若出現 `qrcode_fallback.png`（全頁截圖），代表即夢網站 DOM 結構可能已更新。
請更新 `selectors.py` 中的 `QRCODE_SELECTORS` 清單。

### 選擇器失效（圖片找不到 / 提示詞框找不到）

即夢前端更新後，可能需要更新 `src/jimeng_cli/selectors.py` 中對應的選擇器清單。
建議開啟 `--verbose` 模式排查問題。

### Chromium 系統依賴缺失

```bash
uv run playwright install-deps chromium
```

---

## 授權

MIT
