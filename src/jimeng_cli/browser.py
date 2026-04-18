"""
瀏覽器管理模組

NOTE: 依「選擇 Playwright（Python）作為瀏覽器自動化框架」設計決策，
      所有 browser / context 的建立、session 存取都集中在此模組。
"""

import json
import os
from pathlib import Path

from loguru import logger
from playwright.sync_api import Browser, BrowserContext, Playwright

# NOTE: Session 存放路徑，跨所有子命令共用
SESSION_PATH = Path.home() / ".jimeng" / "session.json"

# NOTE: 依「Anti-bot browser configuration」設計決策設定 User-Agent，
#       模擬真實 Chrome on Linux，降低被即夢偵測為 bot 的風險
_USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)

# NOTE: 停用 AutomationControlled blink feature，避免 navigator.webdriver 暴露
_CHROMIUM_ARGS = [
    "--no-sandbox",
    "--disable-blink-features=AutomationControlled",
    "--disable-dev-shm-usage",
]


def launch_browser(playwright: Playwright, headless: bool = True) -> Browser:
    """
    啟動 headless Chromium 瀏覽器

    Args:
        playwright: Playwright 實例
        headless: 是否以 headless 模式啟動（VPS 環境必須為 True）

    Returns:
        Browser 實例
    """
    logger.debug("正在啟動 Chromium (headless={})", headless)
    browser = playwright.chromium.launch(
        headless=headless,
        args=_CHROMIUM_ARGS,
    )
    logger.debug("Chromium 啟動完成：{}", playwright.chromium.executable_path)
    return browser


def create_browser_context(browser: Browser) -> BrowserContext:
    """
    建立新的瀏覽器 context，套用反 bot 偵測設定

    NOTE: 依「Anti-bot browser configuration」設計決策，
          設定 User-Agent 並注入 JS 隱藏 navigator.webdriver。

    Args:
        browser: 已啟動的 Browser 實例

    Returns:
        BrowserContext 實例
    """
    context = browser.new_context(
        user_agent=_USER_AGENT,
        viewport={"width": 1280, "height": 900},
        locale="zh-TW",
    )
    # NOTE: 注入 JS 覆蓋 navigator.webdriver，進一步隱藏自動化特徵
    context.add_init_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    logger.debug("已建立 BrowserContext（User-Agent 已設定）")
    return context


def save_session(context: BrowserContext) -> None:
    """
    將瀏覽器 context 狀態（cookies + localStorage）序列化並存至本機

    NOTE: 依「Session 持久化策略」設計決策，
          使用 Playwright 內建 storage_state() 一次序列化所有狀態。

    Args:
        context: 要儲存狀態的 BrowserContext
    """
    SESSION_PATH.parent.mkdir(parents=True, exist_ok=True)
    context.storage_state(path=str(SESSION_PATH))
    logger.info("Session 已儲存至 {}", SESSION_PATH)


def load_session_context(browser: Browser) -> BrowserContext:
    """
    從本機 session 檔案還原 BrowserContext

    NOTE: 依「Session 持久化策略」設計決策，
          透過 storage_state 參數還原已登入狀態。

    Args:
        browser: 已啟動的 Browser 實例

    Returns:
        帶有已儲存 session 的 BrowserContext

    Raises:
        FileNotFoundError: session.json 不存在時拋出
        ValueError: session.json 不是合法 JSON 時拋出
    """
    if not SESSION_PATH.exists():
        raise FileNotFoundError(
            f"Session 檔案不存在：{SESSION_PATH}\n"
            "請先執行 `jimeng login` 完成登入。"
        )

    # NOTE: 驗證 session 檔案為合法 JSON，防止損毀檔案造成不明錯誤
    try:
        with open(SESSION_PATH, encoding="utf-8") as f:
            json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Session 檔案損毀（不是合法 JSON）：{SESSION_PATH}\n"
            f"詳細錯誤：{e}\n"
            "請重新執行 `jimeng login`。"
        ) from e

    context = browser.new_context(
        storage_state=str(SESSION_PATH),
        user_agent=_USER_AGENT,
        viewport={"width": 1280, "height": 900},
        locale="zh-TW",
    )
    # NOTE: 同樣注入反 bot 腳本
    context.add_init_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    logger.debug("已從 {} 還原 Session", SESSION_PATH)
    return context
