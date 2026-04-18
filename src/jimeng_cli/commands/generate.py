"""
生圖命令模組

NOTE: 實作完整圖片生成流程：
      1. 還原 session，導航至生圖頁
      2. 關閉彈窗
      3. 確認圖片生成模式（非 Agent 模式）
      4. 記錄既有圖片，送出提示詞，等待新圖生成
      5. 下載並存檔新生成的 4 張圖片
"""

import sys
import time
import urllib.request
from pathlib import Path
from typing import Optional
from urllib.error import URLError

from loguru import logger
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

from jimeng_cli import browser as browser_mod
from jimeng_cli.selectors import (
    AGENT_MODE_SELECTORS,
    GENERATED_IMAGE_SELECTORS,
    IMAGE_GENERATION_URL,
    LOGIN_PAGE_URL_PATTERNS,
    MODAL_CLOSE_SELECTORS,
    PROMPT_INPUT_SELECTORS,
)

# 生圖完成後等待圖片 src 穩定的輪詢間隔（秒）
_POLL_INTERVAL = 3


def _is_on_login_page(page: Page) -> bool:
    """
    判斷當前頁面是否為登入頁（session 過期跳轉）

    Args:
        page: Playwright Page 實例

    Returns:
        True 表示已跳轉至登入頁
    """
    current_url = page.url
    return any(pattern in current_url for pattern in LOGIN_PAGE_URL_PATTERNS)


def _dismiss_modals(page: Page, max_wait_seconds: int = 5) -> None:
    """
    嘗試關閉頁面上的所有彈窗

    NOTE: 依「彈窗關閉策略」設計決策：
          依序嘗試各關閉按鈕選擇器，任一命中即點擊，
          最多等待 max_wait_seconds 秒，無彈窗時安靜繼續。

    Args:
        page: Playwright Page 實例
        max_wait_seconds: 最大等待秒數
    """
    deadline = time.time() + max_wait_seconds
    closed_count = 0

    while time.time() < deadline:
        found_any = False
        for selector in MODAL_CLOSE_SELECTORS:
            try:
                btn = page.query_selector(selector)
                if btn and btn.is_visible():
                    btn.click()
                    logger.debug("已關閉彈窗（選擇器：{}）", selector)
                    closed_count += 1
                    found_any = True
                    time.sleep(0.5)  # 等待關閉動畫
                    break
            except Exception as e:  # noqa: BLE001
                logger.debug("選擇器 {} 點擊失敗：{}", selector, e)

        if not found_any:
            break  # 沒有彈窗，結束迴圈

    if closed_count > 0:
        logger.info("共關閉 {} 個彈窗", closed_count)
    else:
        logger.debug("未偵測到需要關閉的彈窗")
        
    # HACK: 即夢網頁常有新型彈窗（例如 1080P 上線）無法被現有選擇器匹配，
    #       增加通用方案：對頁面發送 Escape 鍵。
    try:
        page.keyboard.press("Escape")
        time.sleep(0.5)
        page.keyboard.press("Escape")
        logger.debug("已發送 Escape 鍵嘗試關閉未知彈窗")
    except Exception:
        pass


def _is_agent_mode(page: Page) -> bool:
    """
    偵測當前是否處於 Agent 模式

    NOTE: 依「Agent 模式偵測與重新整理策略」設計決策：
          偵測到 Agent 相關元素或文字即視為 Agent 模式。

    Args:
        page: Playwright Page 實例

    Returns:
        True 表示 Agent 模式
    """
    for selector in AGENT_MODE_SELECTORS:
        try:
            el = page.query_selector(selector)
            if el and el.is_visible():
                logger.debug("偵測到 Agent 模式元素：{}", selector)
                return True
        except Exception:  # noqa: BLE001
            pass
    return False


def _ensure_image_mode(page: Page, max_retries: int = 3) -> None:
    """
    確認創作模式為「圖片生成」，若為 Agent 模式則重新整理

    NOTE: 依「Agent 模式偵測與重新整理策略」設計決策：
          最多重試 max_retries 次，每次重試後重新關閉彈窗。

    Args:
        page: Playwright Page 實例
        max_retries: 最大重試次數

    Raises:
        RuntimeError: 重試次數用盡仍為 Agent 模式
    """
    for attempt in range(max_retries + 1):
        if not _is_agent_mode(page):
            logger.debug("確認處於圖片生成模式")
            return

        if attempt >= max_retries:
            raise RuntimeError(
                f"重試 {max_retries} 次後仍處於 Agent 模式，請手動確認即夢網頁狀態。"
            )

        logger.warning("偵測到 Agent 模式，正在重新整理頁面（第 {}/{} 次）...", attempt + 1, max_retries)
        page.reload(wait_until="domcontentloaded", timeout=15_000)
        time.sleep(2)
        _dismiss_modals(page)


def _collect_existing_image_srcs(page: Page) -> set[str]:
    """
    收集頁面上現有的圖片 src 集合（生圖前快照）

    NOTE: 依「新圖辨識策略（避免存到舊圖）」設計決策：
          生圖前記錄此集合，生圖後以差集取得本次新圖。

    Args:
        page: Playwright Page 實例

    Returns:
        現有圖片 src URL 的集合
    """
    srcs: set[str] = set()
    for selector in GENERATED_IMAGE_SELECTORS:
        try:
            elements = page.query_selector_all(selector)
            for el in elements:
                src = el.get_attribute("src")
                if src and src.startswith("http"):
                    srcs.add(src)
        except Exception:  # noqa: BLE001
            pass
    logger.debug("生圖前既有圖片數量：{}", len(srcs))
    return srcs


def _submit_prompt(page: Page, prompt: str) -> bool:
    """
    在提示詞輸入框輸入文字並送出

    NOTE: 若輸入框 15 秒內找不到，則回傳 False 以便外層重試。

    Args:
        page: Playwright Page 實例
        prompt: 要輸入的提示詞
        
    Returns:
        bool: 是否成功送出提示詞
    """
    Path("debug_dom.html").write_text(page.content(), encoding="utf-8")

    for selector in PROMPT_INPUT_SELECTORS:
        try:
            el = page.wait_for_selector(selector, timeout=15_000, state="visible")
            if el:
                el.click()
                el.fill(prompt)
                logger.debug("提示詞已輸入（選擇器：{}）", selector)
                el.press("Enter")
                logger.info("提示詞已送出：{}", prompt)
                return True
            else:
                logger.debug("選擇器 {} 未能匹配可見的元素", selector)
        except PlaywrightTimeoutError:
            logger.debug("輸入框選擇器 {} 超時", selector)
        except Exception as e:  # noqa: BLE001
            logger.debug("選擇器 {} 發生錯誤: {}", selector, e)

    logger.error("找不到提示詞輸入框（已嘗試所有選擇器）")
    return False


def _wait_for_new_images(
    page: Page,
    existing_srcs: set[str],
    expected_count: int,
    timeout_seconds: int,
) -> list[str]:
    """
    等待頁面出現指定數量的新生成圖片

    NOTE: 依「新圖辨識策略（避免存到舊圖）」設計決策：
          輪詢直到出現 expected_count 個不在 existing_srcs 中的新 src。

    Args:
        page: Playwright Page 實例
        existing_srcs: 生圖前既有的圖片 src 集合
        expected_count: 期望的新圖數量
        timeout_seconds: 最大等待秒數

    Returns:
        新圖的 URL 清單

    Raises:
        RuntimeError: 超時或 session 過期
    """
    logger.info("等待圖片生成完成（最多 {} 秒）...", timeout_seconds)
    deadline = time.time() + timeout_seconds

    while time.time() < deadline:
        # NOTE: 檢查是否 session 過期跳轉至登入頁
        if _is_on_login_page(page):
            raise RuntimeError(
                "圖片生成中 Session 已過期，頁面跳轉至登入頁。\n"
                "請重新執行 `jimeng login`。"
            )

        # 蒐集所有當前圖片 src
        current_srcs: set[str] = set()
        for selector in GENERATED_IMAGE_SELECTORS:
            try:
                elements = page.query_selector_all(selector)
                for el in elements:
                    src = el.get_attribute("src")
                    if src and src.startswith("http"):
                        current_srcs.add(src)
            except Exception:  # noqa: BLE001
                pass

        new_srcs = current_srcs - existing_srcs
        logger.debug("目前新圖數量：{}/{}", len(new_srcs), expected_count)

        if len(new_srcs) >= expected_count:
            logger.info("偵測到 {} 張新圖，生成完成！", len(new_srcs))
            # NOTE: 只取前 expected_count 張，避免取到無關圖片
            return list(new_srcs)[:expected_count]

        time.sleep(_POLL_INTERVAL)

    raise RuntimeError(
        f"等待超時（{timeout_seconds} 秒），"
        f"只找到 {len(new_srcs)} 張新圖，期望 {expected_count} 張。"
    )


def _download_images(srcs: list[str], output_dir: Path) -> list[Path]:
    """
    從 URL 下載圖片並存檔

    Args:
        srcs: 圖片 URL 清單
        output_dir: 存檔目錄

    Returns:
        存檔路徑清單
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    saved: list[Path] = []

    for i, src in enumerate(srcs, start=1):
        save_path = output_dir / f"image_{i}.png"
        try:
            # NOTE: 設定 User-Agent 避免下載被伺服器拒絕
            req = urllib.request.Request(
                src,
                headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"},
            )
            with urllib.request.urlopen(req, timeout=30) as resp:  # noqa: S310
                save_path.write_bytes(resp.read())
            logger.info("圖片已存至：{}", save_path)
            print(str(save_path))
            saved.append(save_path)
        except URLError as e:
            logger.error("圖片下載失敗（{}）：{}", src, e)

    return saved


def run(prompt: str, output_dir: Path, generation_timeout: int) -> None:
    """
    執行完整圖片生成流程

    Args:
        prompt: 圖片生成提示詞
        output_dir: 圖片存檔目錄
        generation_timeout: 等待生成完成的秒數上限
    """
    with sync_playwright() as playwright:
        browser = browser_mod.launch_browser(playwright)

        try:
            # ── 步驟 1：還原 session，導航至生圖頁 ──────────────────────────
            try:
                context = browser_mod.load_session_context(browser)
            except (FileNotFoundError, ValueError) as e:
                logger.error("{}", e)
                sys.exit(1)

            page = context.new_page()
            logger.info("正在開啟即夢生圖頁...")
            page.goto(IMAGE_GENERATION_URL, wait_until="domcontentloaded", timeout=15_000)

            if _is_on_login_page(page):
                logger.error("Session 已過期，頁面跳轉至登入頁。\n請重新執行 `jimeng login`。")
                sys.exit(1)

            logger.debug("生圖頁已載入：{}", page.url)

            # ── 步驟 2：關閉彈窗 ─────────────────────────────────────────────
            _dismiss_modals(page)

            # ── 步驟 3：確認圖片生成模式 ──────────────────────────────────────
            try:
                _ensure_image_mode(page)
            except RuntimeError as e:
                logger.error("{}", e)
                sys.exit(1)

            # ── 步驟 2~5：處理模式、關閉彈窗與送出提示詞，支援重新載入防呆 ──
            submit_success = False
            for attempt in range(2):
                _ensure_image_mode(page)
                _dismiss_modals(page)
                
                # ── 步驟 4：記錄既有圖片（避免誤存舊圖）────────────────────────
                existing_srcs = _collect_existing_image_srcs(page)
                
                # ── 步驟 5：送出提示詞 ───────────────────────────────────────────
                if _submit_prompt(page, prompt):
                    submit_success = True
                    break
                else:
                    if attempt == 0:
                        logger.warning("提示詞欄位偵測失敗，重新載入頁面並重試一次...")
                        page.reload(wait_until="domcontentloaded")
                    else:
                        raise RuntimeError("無法送出提示詞，已超過重試次數")
            
            logger.info("提示詞已送出，等待圖片生成中...")

            # ── 步驟 6：等待並下載新圖 ────────────────────────────────────────
            try:
                new_srcs = _wait_for_new_images(
                    page,
                    existing_srcs,
                    expected_count=4,
                    timeout_seconds=generation_timeout,
                )
            except RuntimeError as e:
                logger.error("{}", e)
                sys.exit(1)

            saved_paths = _download_images(new_srcs, output_dir)

            if not saved_paths:
                logger.error("沒有圖片成功存檔")
                sys.exit(1)

            print(f"\n✅ 共存檔 {len(saved_paths)} 張圖片至 {output_dir}")

        except PlaywrightTimeoutError as e:
            logger.error("頁面操作超時：{}", e)
            sys.exit(1)
        except Exception as e:
            logger.error("生圖流程發生未預期錯誤：{}", e)
            sys.exit(1)
        finally:
            context.close()
            browser.close()
