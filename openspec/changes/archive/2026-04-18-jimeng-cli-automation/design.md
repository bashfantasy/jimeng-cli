## Context

即夢（Jimeng）是字節跳動旗下的 AI 圖片生成 SaaS 平台，登入方式採用抖音 OAuth QR Code 掃碼授權。目標部署環境為 Hostinger VPS（Ubuntu，無 X-Window），因此瀏覽器必須以 headless 模式運行。

本工具需自動化以下流程：
1. 開啟 OAuth 登入頁並擷取 QR Code 圖片存檔（供使用者以抖音 App 掃碼）
2. 輪詢頁面是否完成跳轉（掃碼成功）
3. 開啟生圖頁，處理彈窗干擾，確認創作模式，輸入提示詞並觸發生成
4. 擷取本次新生成的 4 張圖片並存檔
5. 在命令之間持久化瀏覽器 session（避免每次重新登入）

## Goals / Non-Goals

**Goals:**
- 在無 GUI 的 Ubuntu VPS 環境中，以 headless Playwright + Chromium 自動化即夢網站
- 提供清晰的 CLI 介面（`jimeng login`、`jimeng generate`、`jimeng logout`）
- QR Code 圖片正確截圖並存檔，方便使用者掃碼
- 生圖時只存檔「本次生成」的新圖，不重複存入舊圖
- Session 持久化至本機 JSON 檔，跨命令重用

**Non-Goals:**
- 不支援影片生成功能
- 不自動安裝 Playwright Chromium 依賴
- 不提供 Web UI 或 REST API 介面
- 不支援帳號密碼登入方式
- 不處理驗證碼（CAPTCHA）繞過

## Decisions

### 選擇 Playwright（Python）作為瀏覽器自動化框架

**決策**：使用 `playwright`（Python）+ headless Chromium

**理由**：
- Playwright 原生支援 headless 模式，在無 X-Window 的 Linux 環境可靠運行
- 相較 Selenium，Playwright 的 `page.wait_for_selector()` 和網路等待 API 更現代且穩定
- 支援 `browser_context.storage_state()` 直接序列化整個 session（cookies + localStorage），是 session 持久化的最簡潔方案
- 實作已套用反 bot 參數：`--no-sandbox`、`--disable-blink-features=AutomationControlled`、`--disable-dev-shm-usage`，並注入 `navigator.webdriver = undefined`

**替代方案考量**：
- Selenium：API 較舊，session 序列化需手動處理 cookies，淘汰
- Puppeteer（Node.js）：Python 技術棧統一性考量，不採用

---

### 選擇 Typer 作為 CLI 框架

**決策**：使用 `typer` 建構 CLI 入口

**理由**：
- Typer 基於 Python type hints 自動生成命令說明與參數解析，代碼量少且可維護性高
- 支援子命令（subcommand）結構，符合 `jimeng login/generate/logout` 的命令設計
- 相較 Click，Typer 更接近現代 Python 風格

---

### Session 持久化策略

**決策**：使用 Playwright 的 `browser_context.storage_state(path=...)` 存至 `~/.jimeng/session.json`

**理由**：
- Playwright 內建支援，一行呼叫即可序列化完整的 cookies + localStorage
- 下次啟動時透過 `browser.new_context(storage_state=path)` 還原，確保已登入狀態
- Session 檔存於 `~/.jimeng/` 讓所有子命令共用

---

### 輸出目錄預設值策略

**決策**：所有命令的 `--output-dir` 預設值使用 `~/.openclaw/media/browser`

**理由**：
- 實作已將預設輸出路徑統一到 openclaw 的 media 目錄，便於與既有工作流整合
- 路徑位於使用者 home 目錄下，適合 headless VPS 長期運行

---

### QR Code 截圖策略

**決策**：等待 QR Code 元素出現後，對該元素使用 `element.screenshot(path=...)` 精確截圖；若選擇器都未命中則退回頁面截圖 `qrcode_fallback.png`

**理由**：
- 元素級截圖比頁面截圖更精確，QR Code 圖片品質更佳，方便抖音 App 掃碼
- 若無法定位元素，退回頁面截圖以保留當前畫面供人工確認

---

### 登入完成偵測策略

**決策**：輪詢當前 URL，直到頁面跳轉至 `jimeng.jianying.com/ai-tool/third-party-callback`

**理由**：
- Playwright `page.wait_for_url()` 可精確等待跳轉，設定合理 timeout（120 秒）
- 比輪詢 DOM 元素更可靠，不受頁面結構變動影響

---

### 新圖辨識策略（避免存到舊圖）

**決策**：生圖前記錄當前已存在的圖片 DOM 元素（或圖片 URL 集合），觸發生成後等待出現新的圖片元素（數量超過原有）

**理由**：
- 即夢生圖頁的圖片以瀑布流方式呈現，新舊圖片同時存在
- 觸發生成前記錄既有圖片 src 集合，等待出現不在集合內的 4 個新 src 即為本次生成結果
- 等待策略：輪詢直到新圖數量 ≥ 4 或 timeout（預設 180 秒）

---

### 彈窗關閉策略

**決策**：頁面載入後，依序嘗試偵測並點擊常見的「關閉」按鈕選擇器，最多等待 5 秒

**理由**：
- 即夢可能出現公告、引導、活動彈窗，選擇器可能隨版本變動
- 採用多選擇器嘗試清單（`[aria-label="close"]`、`.modal-close`、`.lv-dialog__close` 等），任一命中即關閉
- 若無彈窗，超時後繼續，不中斷流程
- 若選擇器清單未命中，額外發送 `Escape` 鍵作為關閉未知彈窗的回退方案

---

### Agent 模式偵測與重新整理策略

**決策**：頁面載入後以 Agent 模式選擇器清單檢查狀態，若命中則 `page.reload()` 並重新檢查

**理由**：
- 即夢的創作類型（Agent 模式 vs 圖片生成模式）會影響提示詞送出後的行為
- 強制重新整理是最直接的重置方式，避免複雜的 DOM 操作

---

### 提示詞送出與重試策略

**決策**：每次送出提示詞前輸出 `debug_dom.html`；若找不到輸入框則重新整理並重試 1 次（共最多 2 次嘗試）

**理由**：
- `debug_dom.html` 可保留當下 DOM 供選擇器失效排查
- 生圖頁受彈窗與模式切換影響，重新整理可提升輸入框定位成功率
- 限制重試次數可避免無限等待

---

### 圖片下載完成條件策略

**決策**：偵測到 4 張新圖後開始下載；若至少 1 張成功存檔即視為命令成功，0 張才視為失敗

**理由**：
- 圖片 URL 可能因網路或權限短暫失敗，允許部分成功可提高流程可用性
- 仍保留 0 張失敗的明確錯誤界線

---

### 新圖順序策略

**決策**：新圖以 `set` 差集取得，下載順序不保證與頁面顯示順序一致

**理由**：
- 實作以集合差異判斷「是否新圖」，可快速避免誤抓舊圖
- 目前目標是存到本次新圖，不要求穩定排序

## Risks / Trade-offs

| 風險 | 緩解措施 |
|------|----------|
| 即夢網站 DOM 結構更新導致選擇器失效 | 將所有選擇器集中定義在 `selectors.py` 常數模組，易於維護更新 |
| headless Chromium 被即夢偵測為 bot | 設定 `user-agent`、關閉自動化標記（`--disable-blink-features=AutomationControlled`）|
| QR Code 有效期短（通常 60–120 秒） | 截圖後即時輸出提示，要求使用者儘快掃碼 |
| 生圖等待時間不確定（可能超過 180 秒） | `--timeout` 參數允許使用者自訂等待上限 |
| 圖片下載順序不穩定 | 目前允許任意順序存檔，若需穩定順序可於後續改以時間戳/DOM 順序排序 |
| 除錯輸出會產生額外檔案（`debug_dom.html`） | 視為現行行為；若需移除可在後續改為 `--verbose` 或專用 debug 旗標 |
| Session 過期需重新登入 | `generate` 命令若偵測到跳轉至登入頁，自動提示使用者執行 `jimeng login` |
| VPS 缺少 Chromium 系統依賴 | README 提供完整的 `playwright install-deps chromium` 安裝指令 |
