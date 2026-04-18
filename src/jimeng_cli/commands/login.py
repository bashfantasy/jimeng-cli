"""
登入命令模組

NOTE: 實作 QR Code 登入流程：
      1. 開啟即夢 OAuth 登入頁（Navigate to OAuth login page）
      2. 截圖 QR Code 元素存檔（Detect and capture QR code image）
      3. 輪詢 URL 等待登入完成（Poll for login completion）
"""

import sys
import time
from pathlib import Path

from loguru import logger
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

from jimeng_cli import browser as browser_mod
from jimeng_cli.selectors import (
    LOGIN_CALLBACK_URL_PATTERN,
    OAUTH_LOGIN_URL,
    QRCODE_SELECTORS,
)


def _capture_qrcode(page, output_dir: Path) -> Path:
    """
    嘗試截圖 QR Code 元素，失敗則退回全頁截圖

    NOTE: 依「QR Code 截圖策略」設計決策：
          優先使用元素截圖（精確），失敗時退回全頁截圖（qrcode_fallback.png）。

    Args:
        page: Playwright Page 實例
        output_dir: 輸出目錄

    Returns:
        存檔的圖片 Path
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # 依序嘗試各個 QR Code 選擇器
    for selector in QRCODE_SELECTORS:
        try:
            logger.debug("嘗試 QR Code 選擇器：{}", selector)
            element = page.wait_for_selector(selector, timeout=30_000, state="visible")
            if element:
                save_path = output_dir / "qrcode.png"
                element.screenshot(path=str(save_path))
                logger.info("QR Code 已精確截圖存至：{}", save_path)
                return save_path
        except PlaywrightTimeoutError:
            logger.debug("選擇器 {} 超時，嘗試下一個", selector)
        except Exception as e:  # noqa: BLE001
            logger.debug("選擇器 {} 失敗：{}", selector, e)

    # NOTE: 所有元素選擇器均失敗，退回全頁截圖
    logger.warning("找不到 QR Code 元素，退回全頁截圖")
    fallback_path = output_dir / "qrcode_fallback.png"
    page.screenshot(path=str(fallback_path), full_page=False)
    logger.info("全頁截圖已存至：{}", fallback_path)
    return fallback_path


def _poll_login_completion(page, timeout_seconds: int) -> bool:
    """
    輪詢 URL，等待登入完成跳轉

    NOTE: 依「登入完成偵測策略」設計決策：
          使用 wait_for_url() 偵測 callback URL，比輪詢 DOM 更穩定。

    Args:
        page: Playwright Page 實例
        timeout_seconds: 最大等待秒數

    Returns:
        True 表示登入成功，False 表示超時
    """
    logger.info("等待掃碼完成（最多 {} 秒）...", timeout_seconds)
    logger.info("請用抖音 App 掃描上方 QR Code")

    try:
        page.wait_for_url(
            f"**{LOGIN_CALLBACK_URL_PATTERN}**",
            timeout=timeout_seconds * 1000,
        )
        logger.info("偵測到登入回調 URL，登入成功！")
        return True
    except PlaywrightTimeoutError:
        logger.error("等待超時（{} 秒），請重新執行 `jimeng login`", timeout_seconds)
        return False


def run(output_dir: Path, login_timeout: int) -> None:
    """
    執行完整 QR Code 登入流程

    Args:
        output_dir: QR Code 圖片存檔目錄
        login_timeout: 等待掃碼完成的秒數上限
    """
    with sync_playwright() as playwright:
        browser = browser_mod.launch_browser(playwright)
        context = browser_mod.create_browser_context(browser)
        page = context.new_page()

        try:
            # ── 步驟 1：開啟 OAuth 登入頁 ────────────────────────────────────
            logger.info("正在開啟即夢登入頁...")
            page.goto(OAUTH_LOGIN_URL, wait_until="domcontentloaded", timeout=15_000)
            logger.debug("頁面 title：{}", page.title())

            # ── 步驟 2：截圖 QR Code ──────────────────────────────────────────
            qr_path = _capture_qrcode(page, output_dir)
            print(f"\n📱 請用抖音 App 掃描 QR Code：{qr_path}\n")

            # ── 步驟 3：輪詢登入完成 ──────────────────────────────────────────
            success = _poll_login_completion(page, login_timeout)

            if not success:
                sys.exit(1)

            # 等待頁面穩定後儲存 session
            time.sleep(2)
            browser_mod.save_session(context)
            print("✅ Login successful")

        except PlaywrightTimeoutError as e:
            logger.error("頁面載入超時：{}", e)
            sys.exit(1)
        except Exception as e:
            logger.error("登入流程發生未預期錯誤：{}", e)
            sys.exit(1)
        finally:
            context.close()
            browser.close()
