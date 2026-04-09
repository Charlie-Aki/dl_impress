import os
import time
import base64
import hashlib
from datetime import datetime
from playwright.sync_api import sync_playwright

"""
引数を設定していないときは以下の値をデフォルト値として使用します。
- DEFAULT_BASE_URL: 画像を取得したいURLのデフォルト値
- DEFAULT_OUTDIR: JPEGを保存するディレクトリのデフォルト値
- DEFAULT_EDGE_EXE: Edgeブラウザの実行ファイルパス
"""
DEFAULT_BASE_URL = (
    "https://viewer.impress.co.jp/viewer.html"
    "?group_name=155d3206_69cce13a80ab5&pdf=p502340all"
) # 画像を取得したいURLのデフォルト値
DEFAULT_OUTDIR = r"C:\jpegs" # JPEGを保存するディレクトリのデフォルト値
DEFAULT_EDGE_EXE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" # Edgeブラウザの実行ファイルパス


def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def make_run_id():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def download_jpegs_from_data_image(
    base_url: str,
    outdir: str,
    edge_exe: str,
    wait_after_move: float = 0.4,
    no_new_limit: int = 10, #この回数画像が取得できなかったらこれ以上ページがないと判定する。
    headless: bool = True,
    next_button_css: str = "div.viewer_next.slick-arrow",
    viewer_css: str = "#ipc_viewer_wrap",
    add_timestamp_to_filename: bool = True,   # ★ デフォルトONに変更
    run_subdir: str | None = None,
):
    """
    data:image を取得してページ画像を保存（重複は画像SHA1で排除）。
    - add_timestamp_to_filename=True の場合、page_001_yyyymmdd_hhmmss.jpg のように秒まで付与
    - run_subdir を指定すると outdir/run_subdir/ 配下に保存（混在回避）
    """

    if run_subdir:
        outdir = os.path.join(outdir, run_subdir)

    ensure_dir(outdir)

    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=edge_exe, headless=headless)
        page = browser.new_page()

        page.goto(base_url, wait_until="load")
        time.sleep(1.0)

        seen_hashes = set()
        page_index = 0
        no_new_count = 0

        # ファイル名に付ける時刻（実行中は固定）
        run_id = make_run_id()

        while True:
            new_this_turn = 0

            data_images = page.evaluate(
                """(viewerSel) => {
                    const viewer = document.querySelector(viewerSel);
                    if (!viewer) return [];
                    return Array.from(viewer.querySelectorAll('img[src^="data:image"]'))
                        .filter(img => img.offsetParent !== null)
                        .map(img => img.src);
                }""",
                viewer_css
            )

            for src in data_images:
                try:
                    _, b64 = src.split(",", 1)
                except ValueError:
                    continue

                binary = base64.b64decode(b64)
                h = hashlib.sha1(binary).hexdigest()

                if h in seen_hashes:
                    continue

                seen_hashes.add(h)
                page_index += 1
                new_this_turn += 1

                if add_timestamp_to_filename:
                    name = f"page_{page_index:03d}_{run_id}.jpg"
                else:
                    name = f"page_{page_index:03d}.jpg"

                out_path = os.path.join(outdir, name)

                with open(out_path, "wb") as f:
                    f.write(binary)

                print(f"page {page_index:03d} saved -> {out_path}")

            if new_this_turn == 0:
                no_new_count += 1
                # print(f"no new page ({no_new_count}/{no_new_limit})")
            else:
                no_new_count = 0

            if no_new_count >= no_new_limit:
                print("No new pages detected. Stop.")
                break

            btn = page.locator(next_button_css)
            if btn.count() == 0:
                print("No next button. Stop.")
                break

            btn.first.click()
            time.sleep(wait_after_move)

        browser.close()

    return page_index, outdir


if __name__ == "__main__":
    # テスト実行用（JPEG名はデフォルトで時刻付き）
    download_jpegs_from_data_image(
        base_url=DEFAULT_BASE_URL,
        outdir=DEFAULT_OUTDIR,
        edge_exe=DEFAULT_EDGE_EXE,
        headless=False,
        add_timestamp_to_filename=True,
        run_subdir=f"run_{make_run_id()}",
    )
