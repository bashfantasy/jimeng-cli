"""
選擇器常數模組

NOTE: 將所有 CSS/XPath 選擇器集中在此處管理，
      當即夢網站 DOM 結構更新時，只需修改此檔案。
"""

# ── QR Code ──────────────────────────────────────────────────────────────────

# 即夢 OAuth 登入頁的 QR Code img 元素選擇器（優先嘗試順序）
QRCODE_SELECTORS: list[str] = [
    # NOTE: 即夢 OAuth 頁實際使用 ByteDance Semi Design 的 semi-image-img，
    #       QR Code 以 base64 data URI 方式內嵌（不是外部 URL）。
    "img.semi-image-img[src^='data:image/png;base64']",
    "img.semi-image-img",
    # 備用：更寬鬆的 class 匹配
    "img[class*='semi-image']",
    # 以下為其他可能的選擇器
    "canvas[class*='qrcode']",
    "img[class*='qrcode']",
    "img[class*='qr']",
    "canvas[class*='qr']",
    "[class*='qrcode'] img",
    "[class*='qrcode'] canvas",
    "[class*='qr-code'] img",
    "[class*='QrCode'] img",
    "[class*='QRCode'] img",
]

# ── 彈窗關閉按鈕 ──────────────────────────────────────────────────────────────

# NOTE: 即夢可能出現多種彈窗（公告、引導、活動），
#       依序嘗試這些選擇器，任一命中即點擊。
MODAL_CLOSE_SELECTORS: list[str] = [
    # 通用 aria-label
    "[aria-label='close']",
    "[aria-label='Close']",
    "[aria-label='關閉']",
    # Lark UI / ByteDance UI
    ".lv-modal-close-icon",
    ".lv-dialog__close",
    ".lv-modal__close",
    ".lv-popup__close",
    # 通用 class 模式
    ".modal-close",
    ".close-btn",
    ".close-button",
    "[class*='closeBtn']",
    "[class*='close-btn']",
    "[class*='CloseBtn']",
    "[class*='close-icon']",
    "[class*='closeIcon']",
    "[class*='CloseIcon']",
    # 帶有 × 文字的按鈕（回退方案）
    "button:has-text('×')",
    "button:has-text('✕')",
    "button:has-text('关闭')",
    "button:has-text('關閉')",
]

# ── 提示詞輸入框 ──────────────────────────────────────────────────────────────

# NOTE: 即夢生圖頁的提示詞輸入框選擇器（優先嘗試順序）
PROMPT_INPUT_SELECTORS: list[str] = [
    "[class*='prompt-editor'] .ProseMirror",
    ".prompt-editor-container-VmNauw .ProseMirror",
    ".tiptap.ProseMirror",
    "[placeholder*='上传参考图']",
    ".ProseMirror",
    "[contenteditable='true']",
]

# ── 生成結果圖片 ──────────────────────────────────────────────────────────────

# NOTE: 即夢生成後圖片以瀑布流呈現，使用此選擇器找出所有結果圖
GENERATED_IMAGE_SELECTORS: list[str] = [
    ".image-record-H9ZxhF img[src]",
    "[class*='image-record'] img[src]",
]

# ── Agent 模式偵測 ────────────────────────────────────────────────────────────

# NOTE: 偵測到以下任一選擇器可見，代表目前處於 Agent 模式，需要重新整理
AGENT_MODE_SELECTORS: list[str] = [
    "[class*='agentMode']",
    "[class*='AgentMode']",
    "[class*='agent-mode']",
    # 文字內容匹配（使用 Playwright :text() 語法）
    # 註解掉以下太寬鬆的匹配，避免誤判
    # ":text('Agent')",
    # ":text('智能体')",
    # ":text('agent模式')",
    # ":text('Agent模式')",
]

# ── 圖片生成模式確認 ──────────────────────────────────────────────────────────

# NOTE: 確認目前處於圖片生成模式（而非 Agent / 影片模式）
IMAGE_MODE_ACTIVE_SELECTORS: list[str] = [
    "[class*='imageMode'][class*='active']",
    "[class*='ImageMode'][class*='active']",
    "[class*='image-mode'][class*='active']",
    # 標籤頁文字匹配
    "[class*='active']:text('图片生成')",
    "[class*='active']:text('圖片生成')",
    "[class*='tabActive']:text('图片')",
]

# ── URL 模式 ──────────────────────────────────────────────────────────────────

# 登入完成後的回調 URL 特徵
LOGIN_CALLBACK_URL_PATTERN = "jimeng.jianying.com/ai-tool/third-party-callback"

# 登入頁 URL 特徵（用於偵測 session 過期跳轉）
LOGIN_PAGE_URL_PATTERNS: list[str] = [
    "open.douyin.com/platform/oauth",
    "passport/sso/login",
    "passport/web/login",
    "accounts.douyin.com",
]

# ── 網址常數 ──────────────────────────────────────────────────────────────────

OAUTH_LOGIN_URL = (
    "https://open.douyin.com/platform/oauth/pc/auth"
    "?client_key=aw97st49sighch6k"
    "&response_type=code"
    "&scope=user_info"
    "&state=e53c3ce23gAToVCgoVPZIDJmOGFiYTUwNzFlNTgxZmRjZjc2ZWJmNWRiNjBhMGY1"
    "oU7ZOGh0dHBzOi8vamltZW5nLmppYW55aW5nLmNvbS9haS10b29sL3RoaXJkLXBhcnR5"
    "LWNhbGxiYWNroVYBoUkAoUQAoUHSAAfWn6FNAKFIs2ppbWVuZy5qaWFueWluZy5jb22h"
    "UgKiUEzROl6mQUNUSU9OoKFM2ShodHRwczovL2ppbWVuZy5qaWFueWluZy5jb20vYWkt"
    "dG9vbC9ob21loVTZIGZmYzBjNzIxMGNiMzNlZGZkOGJlMTU5M2I1YmJmY2EyoVcAoUYA"
    "olNBAKFVwqJNTMI%3D"
    "&redirect_uri=https%3A%2F%2Fjimeng.jianying.com%2Fpassport%2Fweb%2Fweb_login_success"
)

IMAGE_GENERATION_URL = (
    "https://jimeng.jianying.com/ai-tool/home?type=image&workspace=undefined"
)

LOGOUT_URL = "https://jimeng.jianying.com/passport/web/logout"
