import os
from datetime import datetime
import img2pdf

"""
引数を設定していないときは以下の値をデフォルト値として使用します。
- DEFAULT_INPUT_DIR: JPGファイルを読み込むディレクトリのデフォルト値
- DEFAULT_OUTPUT_PDF: PDFを保存するパスのデフォルト値
"""
DEFAULT_INPUT_DIR = r"C:\jpegs" # JPGファイルを読み込むディレクトリのデフォルト値
DEFAULT_OUTPUT_PDF = r"C:\jpegs\book.pdf" # PDFを保存するパスのデフォルト値


def make_run_id():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def make_pdf_from_jpegs(input_dir: str, output_pdf: str, add_timestamp: bool = True):
    """
    input_dir内の JPG を名前順でPDF化。
    add_timestamp=True の場合、出力PDF名末尾に _yyyymmdd_hhmmss を付与して衝突を回避。
    """
    images = [
        os.path.join(input_dir, f)
        for f in sorted(os.listdir(input_dir))
        if f.lower().endswith(".jpg")
    ]

    if not images:
        raise RuntimeError(f"No JPG files found in: {input_dir}")

    out_parent = os.path.dirname(output_pdf)
    if out_parent:
        os.makedirs(out_parent, exist_ok=True)

    final_pdf = output_pdf
    if add_timestamp:
        base, ext = os.path.splitext(output_pdf)
        final_pdf = f"{base}_{make_run_id()}{ext if ext else '.pdf'}"

    with open(final_pdf, "wb") as f:
        f.write(img2pdf.convert(images))

    print(f"PDF created: {final_pdf}")
    print(f"Total pages: {len(images)}")
    return len(images), final_pdf


if __name__ == "__main__":
    # テスト実行用（PDF名はデフォルトで時刻付き）
    make_pdf_from_jpegs(
        input_dir=DEFAULT_INPUT_DIR,
        output_pdf=DEFAULT_OUTPUT_PDF,
        add_timestamp=True
    )
