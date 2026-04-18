"""
登出命令模組

NOTE: 實作登出流程：
      1. 瀏覽即夢登出 URL（Navigate to logout URL）
      2. 刪除本機 session 檔案（Clear session on logout）
"""

import sys

from loguru import logger
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

from jimeng_cli import browser as browser_mod
from jimeng_cli.browser import SESSION_PATH
from jimeng_cli.selectors import LOGOUT_URL


def run() -> None:
    """
    執行完整登出流程：開啟登出頁並清除本機 Session
    """
    with sync_playwright() as playwright:
        browser = browser_mod.launch_browser(playwright)
        context = browser_mod.create_browser_context(browser)
        page = context.new_page()

        try:
            # ── 步驟 1：導航至登出 URL ────────────────────────────────────────
            logger.info("正在開啟即夢登出頁：{}", LOGOUT_URL)
            try:
                page.goto(LOGOUT_URL, wait_until="domcontentloaded", timeout=10_000)
                logger.debug("登出頁已載入：{}", page.url)
            except PlaywrightTimeoutError:
                # NOTE: 依設計決策：登出 URL 無法連線時，記錄警告但繼續清除 session
                logger.warning("登出頁載入超時，跳過瀏覽器登出步驟")
            except Exception as e:  # noqa: BLE001
                logger.warning("登出頁載入失敗（{}），跳過瀏覽器登出步驟", e)

        finally:
            context.close()
            browser.close()

    # ── 步驟 2：清除本機 session 檔案 ────────────────────────────────────────
    if SESSION_PATH.exists():
        try:
            SESSION_PATH.unlink()
            logger.debug("Session 檔案已刪除：{}", SESSION_PATH)
        except OSError as e:
            logger.error("無法刪除 Session 檔案：{}", e)
            sys.exit(1)
    else:
        logger.debug("Session 檔案不存在，無需清除")

    print("✅ Logged out successfully.")
