## 1. 專案初始化與環境配置

- [x] 1.1 使用 `uv init` 初始化 Python 專案，設定 `pyproject.toml`，Python 版本 ≥ 3.10（依設計決策：選擇 Playwright（Python）作為瀏覽器自動化框架、選擇 Typer 作為 CLI 框架）
- [x] 1.2 [P] 使用 `uv add playwright typer loguru pillow` 安裝依賴套件
- [x] 1.3 [P] 建立專案目錄結構：`src/jimeng_cli/`，包含 `__init__.py`、`main.py`、`selectors.py`、`browser.py`、`commands/`
- [x] 1.4 在 `pyproject.toml` 中設定 `[project.scripts]` 將 `jimeng` 指令對應至 `jimeng_cli.main:app`

## 2. 選擇器常數模組（selectors.py）

- [x] 2.1 在 `selectors.py` 中集中定義所有 CSS/XPath 選擇器常數：QR Code 圖片選擇器、提示詞輸入框選擇器、彈窗關閉按鈕選擇器清單、生成結果圖片選擇器、Agent 模式文字選擇器

## 3. 瀏覽器管理模組（browser.py）

- [x] 3.1 實作 `create_browser_context()` 函式：依「選擇 Playwright（Python）作為瀏覽器自動化框架」設計決策，套用反bot偵測設定（Anti-bot browser configuration）：設定真實 User-Agent、停用 `AutomationControlled` blink feature
- [x] 3.2 實作 Session 持久化策略：`save_session(context)` 呼叫 `storage_state` 存至 `~/.jimeng/session.json`（Save browser session state）
- [x] 3.3 實作 Session 還原：`load_session_context(browser)` 從 `~/.jimeng/session.json` 建立 context（Restore browser session state）；若檔案不存在則拋出錯誤

## 4. CLI 入口點（main.py）

- [x] 4.1 依「選擇 Typer 作為 CLI 框架」設計決策，使用 Typer 建立 `app` 實例，實作 CLI entry point with subcommands（`login`、`generate`、`logout`）
- [x] 4.2 依「輸出目錄預設值策略」實作共用 Output directory option：`--output-dir`（預設 `~/.openclaw/media/browser`），對每個子命令均可用
- [x] 4.3 實作 Verbose logging option：`--verbose` 旗標，啟用 loguru DEBUG 層級輸出

## 5. 登入命令（commands/login.py）

- [x] 5.1 實作 Navigate to OAuth login page：以 headless Chromium 開啟即夢 OAuth 登入 URL，等待頁面 DOM 載入（最多 15 秒）
- [x] 5.2 依「QR Code 截圖策略」設計決策，實作 Detect and capture QR code image：等待 QR Code 元素出現（最多 30 秒），使用元素截圖存成 `qrcode.png`；若元素找不到則退回全頁截圖存成 `qrcode_fallback.png`，並列印路徑至 stdout
- [x] 5.3 依「登入完成偵測策略」設計決策，實作 Poll for login completion：輪詢當前 URL，偵測到 `/ai-tool/third-party-callback` 即視為成功，呼叫 `save_session()`，列印「Login successful」並以 exit code 0 退出；超過 120 秒則以非零 exit code 退出

## 6. 生圖命令（commands/generate.py）

- [x] 6.1 實作 Navigate to image generation page：還原 session 並導航至生圖 URL；若頁面重定向至登入頁則提示使用者執行 `jimeng login` 並退出
- [x] 6.2 依「彈窗關閉策略」設計決策，實作 Dismiss modal dialogs：頁面載入後 5 秒內嘗試點擊彈窗關閉按鈕（使用 `selectors.py` 中的清單，任一命中即點擊），迴圈直到無彈窗或時間耗盡
- [x] 6.3 依「Agent 模式偵測與重新整理策略」設計決策，實作 Verify image generation mode：偵測 Agent 模式文字，若存在則 `page.reload()`（最多 3 次重試），每次重試後重新執行彈窗關閉，確認圖片生成模式後繼續
- [x] 6.4 依「新圖辨識策略（避免存到舊圖）」與「新圖順序策略」設計決策，記錄生圖前的既有圖片 src 集合，並以集合差集處理新圖（為 Wait for and save newly generated images 的前置步驟）
- [x] 6.5 依「提示詞送出與重試策略」實作 Submit generation prompt：送出前輸出 `debug_dom.html`；找到提示詞輸入框後輸入提示詞並按 Enter；若輸入框 15 秒內找不到則重新載入並重試 1 次（共最多 2 次嘗試），超過則以非零 exit code 退出
- [x] 6.6 依「圖片下載完成條件策略」實作 Wait for and save newly generated images：輪詢直到出現 4 個新的圖片 src（不在既有集合內），或超過 timeout（預設 180 秒）；開始下載後若至少成功存檔 1 張則視為成功（0 張才失敗）；若頁面跳轉至登入頁則提示 session 過期

## 7. 登出命令（commands/logout.py）

- [x] 7.1 實作 Navigate to logout URL：導航至 `https://jimeng.jianying.com/passport/web/logout`，等待最多 10 秒；若網路失敗則記錄警告但繼續後續步驟
- [x] 7.2 實作 Clear session on logout：刪除 `~/.jimeng/session.json`（若存在），列印「Logged out successfully.」

## 8. 錯誤處理與日誌

- [x] 8.1 [P] 使用 loguru 統一日誌輸出：INFO 輸出至 stdout，WARNING/ERROR 輸出至 stderr；`--verbose` 時啟用 DEBUG 層級
- [x] 8.2 [P] 確認所有 `Unknown subcommand` 情境由 Typer 自動處理（內建行為），驗證 exit code 非零

## 9. 驗證與打包

- [x] 9.1 在本機以 `uv run jimeng --help` 驗證 CLI 入口點與子命令均正常顯示
- [x] 9.2 在本機以 headless 模式執行 `uv run jimeng login` 完整流程測試（產出 qrcode.png）
- [x] 9.3 撰寫 `README.md`，包含 Ubuntu VPS 安裝步驟（`playwright install chromium`、`playwright install-deps chromium`）與各子命令使用範例
