import argparse
import os
import shutil
from datetime import datetime

from modules.jpeg_downloader import download_jpegs_from_data_image
from modules.pdf_maker import make_pdf_from_jpegs

"""
引数を設定していないときは以下の値をデフォルト値として使用します。
- DEFAULT_BASE_URL: 画像を取得したいURLのデフォルト値
- DEFAULT_OUTDIR: JPEGを保存するディレクトリのデフォルト値
- DEFAULT_EDGE_EXE: Edgeブラウザの実行ファイルパス
- DEFAULT_INPUT_DIR: JPGファイルを読み込むディレクトリのデフォルト値
- DEFAULT_OUTPUT_PDF: PDFを保存するパスのデフォルト値
"""
DEFAULT_BASE_URL = (
    "https://viewer.impress.co.jp/viewer.html"
    "?group_name=155d3206_69cce13a80ab5&pdf=p502340all"
)
DEFAULT_OUTDIR = r"C:\jpegs"
DEFAULT_EDGE_EXE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
DEFAULT_OUTPUT_PDF = r"C:\jpegs\book.pdf"


def make_run_id():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Download JPEGs (data:image) and make a PDF."
    )

    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--outdir", default=DEFAULT_OUTDIR)
    parser.add_argument("--edge-exe", default=DEFAULT_EDGE_EXE)
    parser.add_argument("--output-pdf", default=DEFAULT_OUTPUT_PDF)

    parser.add_argument("--no-new-limit", type=int, default=20)
    parser.add_argument("--wait-after-move", type=float, default=0.4)
    parser.add_argument("--headed", action="store_true")

    parser.add_argument("--skip-download", action="store_true")
    parser.add_argument("--skip-pdf", action="store_true")
    parser.add_argument("--clean-outdir", action="store_true")

    # ★ デフォルトONのフラグたち
    parser.add_argument(
        "--no-timestamp",
        action="store_true",
        help="Do not add timestamp to JPEG filenames (default: add timestamp)"
    )

    parser.add_argument(
        "--no-run-subdir",
        action="store_true",
        help="Do not create run_YYYYmmdd_HHMMSS subdir (default: create)"
    )

    return parser.parse_args()


def clean_directory(path: str):
    if os.path.isdir(path):
        for name in os.listdir(path):
            p = os.path.join(path, name)
            if os.path.isdir(p):
                shutil.rmtree(p)
            else:
                os.remove(p)
    else:
        os.makedirs(path, exist_ok=True)


def main():
    args = parse_args()

    run_id = make_run_id()

    # ✅ デフォルトは run_subdir ON
    use_run_subdir = not args.no_run_subdir
    run_subdir = f"run_{run_id}" if use_run_subdir else None

    outdir = args.outdir

    if args.clean_outdir and not args.skip_download:
        clean_directory(outdir)
        print(f"Cleaned outdir: {outdir}")
    else:
        os.makedirs(outdir, exist_ok=True)

    # ✅ デフォルトは timestamp ON
    add_timestamp = not args.no_timestamp

    actual_jpeg_dir = outdir

    if not args.skip_download:
        pages, actual_jpeg_dir = download_jpegs_from_data_image(
            base_url=args.base_url,
            outdir=outdir,
            edge_exe=args.edge_exe,
            wait_after_move=args.wait_after_move,
            no_new_limit=args.no_new_limit,
            headless=(not args.headed),
            add_timestamp_to_filename=add_timestamp,
            run_subdir=run_subdir
        )
        print(f"Downloaded unique pages: {pages}")
        print(f"JPEG directory: {actual_jpeg_dir}")

    if not args.skip_pdf:
        pages_pdf, final_pdf = make_pdf_from_jpegs(
            input_dir=actual_jpeg_dir,   # ★ 必ず今回の run フォルダのみ
            output_pdf=args.output_pdf,
            add_timestamp=True           # PDFは常にユニーク
        )
        print(f"PDF pages: {pages_pdf}")
        print(f"PDF path : {final_pdf}")


if __name__ == "__main__":
    main()
