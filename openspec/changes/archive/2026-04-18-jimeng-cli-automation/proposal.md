## Why

即夢（Jimeng）是字節跳動旗下的 AI 圖片生成平台，需要透過抖音 QR Code 掃碼登入。在無 X-Window 的 Ubuntu VPS 環境中，現有的桌面操作工具無法使用，因此需要一個純 CLI 工具，透過 headless 瀏覽器自動化完成 QR Code 登入、頁面操控與生圖存檔的完整流程。

## What Changes

- 新增 `jimeng` CLI 工具，以 Python 撰寫，支援 headless Playwright 瀏覽器自動化
- 新增 `login` 子命令：開啟即夢 OAuth 登入頁，等待 QR Code 出現後擷取並存檔，輪詢登入狀態直到掃碼成功
- 新增 `generate` 子命令：開啟即夢生圖頁，關閉任何強制彈窗，確認創作類型為「圖片生成」（若停在 Agent 模式則重新整理），輸入提示詞並送出，等待本次生成的 4 張圖片完成後全部存檔
- 新增 `logout` 子命令：瀏覽即夢登出網址
- 瀏覽器 session（cookies / localStorage）在命令之間持久化，存於本機路徑，避免每次重新登入
- 所有子命令支援 `--output-dir` 參數指定圖片存檔路徑

## Non-Goals

- 不支援影片生成功能
- 不自動安裝 Playwright 瀏覽器依賴（由使用者手動執行 `playwright install chromium`）
- 不提供 Web UI 或 REST API 介面
- 不處理抖音 App 掃碼以外的登入方式（如帳號密碼）

## Capabilities

### New Capabilities

- `cli-entrypoint`：CLI 主程式入口，支援子命令路由（login / generate / logout）與共用選項解析
- `qrcode-login`：開啟即夢 OAuth 登入頁，偵測 QR Code 出現，存檔 QR Code 圖片，輪詢跳轉狀態直到登入完成
- `image-generation`：開啟即夢生圖頁，處理彈窗干擾，確認圖片生成模式，輸入提示詞並觸發生成，辨識本次新生成的 4 張圖片並存檔
- `session-persistence`：將 Playwright browser context（cookies / localStorage）序列化至本機 JSON 檔，跨命令重用登入狀態
- `logout`：瀏覽即夢登出網址並清除本機 session 檔案

### Modified Capabilities

（無）

## Impact

- 受影響的程式碼：全新專案，無既有程式碼
- 新增依賴：
  - `playwright`（Python 繫結，headless Chromium）
  - `typer`（CLI 框架）
  - `pillow`（圖片處理，輔助 QR Code 截圖裁切）
  - `loguru`（日誌輸出）
- 執行環境：Ubuntu VPS（無 X-Window），需 Chromium headless 模式
- Python 版本：≥ 3.10，使用 `uv` 管理相依套件
