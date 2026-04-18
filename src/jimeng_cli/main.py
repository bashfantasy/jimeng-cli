"""
即夢 CLI 主程式入口

NOTE: 依「選擇 Typer 作為 CLI 框架」設計決策，
      使用 Typer 建立子命令結構（login / generate / logout）。
"""

import sys
from pathlib import Path

# NOTE: 圖片存檔預設路徑，對應 openclaw 的 media 目錄
_DEFAULT_OUTPUT_DIR = Path.home() / ".openclaw" / "media" / "browser"
from typing import Annotated

import typer
from loguru import logger

from jimeng_cli.commands import generate, login, logout

# NOTE: 建立 Typer app 實例，no_args_is_help=True 確保無參數時顯示說明
app = typer.Typer(
    name="jimeng",
    help="即夢 AI 圖片生成 CLI 工具\n\n"
    "支援 headless 瀏覽器自動化登入、生圖與登出。",
    no_args_is_help=True,
    add_completion=False,
)

# ── 共用選項型別別名 ──────────────────────────────────────────────────────────

OutputDirOption = Annotated[
    Path,
    typer.Option(
        "--output-dir",
        "-o",
        help="圖片存檔目錄（不存在時自動建立）",
        envvar="JIMENG_OUTPUT_DIR",
    ),
]

VerboseOption = Annotated[
    bool,
    typer.Option(
        "--verbose",
        "-v",
        help="啟用 DEBUG 層級日誌輸出",
    ),
]


def _configure_logging(verbose: bool) -> None:
    """
    設定 loguru 日誌層級

    NOTE: INFO 以上輸出至 stdout；WARNING/ERROR 輸出至 stderr。
          --verbose 時啟用 DEBUG 層級。
    """
    logger.remove()

    level = "DEBUG" if verbose else "INFO"

    # INFO / DEBUG 輸出至 stdout
    logger.add(
        sys.stdout,
        level=level,
        filter=lambda record: record["level"].no < 30,  # < WARNING
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | {message}",
        colorize=True,
    )

    # WARNING 以上輸出至 stderr
    logger.add(
        sys.stderr,
        level="WARNING",
        format="<red>{time:HH:mm:ss}</red> | <level>{level: <8}</level> | {message}",
        colorize=True,
    )


# ── 子命令 ────────────────────────────────────────────────────────────────────

@app.command("login")
def login_cmd(
    output_dir: OutputDirOption = _DEFAULT_OUTPUT_DIR,
    verbose: VerboseOption = False,
    timeout: Annotated[
        int,
        typer.Option("--timeout", help="等待掃碼完成的秒數（預設 120）"),
    ] = 120,
) -> None:
    """開啟即夢 QR Code 登入頁，存檔 QR Code 並等待掃碼完成。"""
    _configure_logging(verbose)
    login.run(output_dir=output_dir, login_timeout=timeout)


@app.command("generate")
def generate_cmd(
    prompt: Annotated[str, typer.Argument(help="圖片生成提示詞")],
    output_dir: OutputDirOption = _DEFAULT_OUTPUT_DIR,
    verbose: VerboseOption = False,
    timeout: Annotated[
        int,
        typer.Option("--timeout", help="等待圖片生成完成的秒數（預設 180）"),
    ] = 180,
) -> None:
    """輸入提示詞，生成 4 張圖片並存檔。"""
    _configure_logging(verbose)
    generate.run(prompt=prompt, output_dir=output_dir, generation_timeout=timeout)


@app.command("logout")
def logout_cmd(
    verbose: VerboseOption = False,
) -> None:
    """登出即夢並清除本機 Session。"""
    _configure_logging(verbose)
    logout.run()


def main() -> None:
    """程式入口點"""
    app()


if __name__ == "__main__":
    main()
