# dl_impress

`dl_impress` is a Python tool to download page images distributed as `data:image`
from the Impress Viewer and convert them into a **lossless PDF**.

The purpose of this program is to convert legally purchased Impress e-book data
into PDF format for offline viewing in network-restricted environments.

---

## Overview

- Extracts `data:image` content directly from Impress Viewer
- Saves pages as JPEG files
- Converts JPEGs into a **lossless PDF**
- Prevents file conflicts using timestamps
- Separates output per execution to avoid mixing files

This repository is intended to be used as a **command-line utility**.

---

## Features

- DOM-based image extraction (no screenshots)
- Automatic duplicate detection using SHA1
- JPEG → PDF conversion without recompression
- Timestamped filenames to avoid overwriting
- Per-run output directories (`run_YYYYmmdd_HHMMSS`)
- Windows-safe PDF generation (no `PermissionError`)

---

## Requirements

- Python 3.9 or later (3.10 / 3.11 recommended)
- Microsoft Edge (Chromium-based)

### Python packages

```text
playwright
img2pdf
```

Install dependencies:

```bash
pip install -r requirements.txt
```

> Note  
> This script launches the existing `msedge.exe` directly.  
> `playwright install chromium` is **not required**.

---

## Project Structure

```
dl_impress/
├─ main.py
├─ requirements.txt
├─ README.md
└─ modules/
   ├─ __init__.py
   ├─ jpeg_downloader.py
   └─ pdf_maker.py
```

`__init__.py` is intentionally empty and only marks the directory as a Python package.

---

## Usage

### Basic usage (recommended)

```bash
python main.py
```

This will:

1. Launch Microsoft Edge
2. Download page images from the Impress Viewer
3. Save JPEG files into a run-specific directory
4. Generate a lossless PDF from those images

### Example output

```
C:\jpegs
└─ run_20260409_153012
   ├─ page_001_20260409_153012.jpg
   ├─ page_002_20260409_153012.jpg
   └─ ...
C:\jpegsbook_20260409_153012.pdf
```

---

## Command-line Options

| Option | Description |
|------|-------------|
| `--headed` | Launch Edge with visible UI |
| `--clean-outdir` | Clean output directory before execution |
| `--skip-download` | Skip JPEG download |
| `--skip-pdf` | Skip PDF generation |
| `--no-timestamp` | Do not add timestamps to JPEG filenames |
| `--no-run-subdir` | Disable per-run output directory |

---

## Notes

- The output directory (`C:\jpegs`) is created automatically
- PDF filenames are always unique
- Files from different runs are not mixed by default
- Safe to re-run even if previous PDFs are open

---

## Disclaimer

This tool is intended for **personal or investigative use**.

Please ensure your usage complies with:

- the terms of service of the target website
- applicable copyright and content usage policies

The author assumes no responsibility for misuse.
