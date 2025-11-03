# topproc-scrape

A Python script to download HTML files from topology.nipissingu.ca.

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the script to download HTML files for volumes 01-67:

```bash
python3 download_html.py
```

By default, files are saved to the `downloads/` directory. You can specify a custom output directory:

```bash
python3 download_html.py /path/to/output
```

## What it does

The script downloads HTML files from:
- `https://topology.nipissingu.ca/tp/reprints/v01/r2.htm`
- `https://topology.nipissingu.ca/tp/reprints/v02/r2.htm`
- ...
- `https://topology.nipissingu.ca/tp/reprints/v67/r2.htm`

Files are saved with names like `v01_r2.html`, `v02_r2.html`, etc.