#!/usr/bin/env python3
import re
import json
import csv
from pathlib import Path
from html import unescape

DOWNLOADS = Path(__file__).resolve().parents[0] / "downloads"


def parse_authors(raw):
    raw = raw.strip()
    # prefer splitting on " and " (covers most cases like "A and B")
    if " and " in raw:
        parts = [p.strip() for p in raw.split(" and ")]
        return parts
    # fallback: split on comma when there are multiple authors
    parts = [p.strip() for p in re.split(r'\s*,\s*(?=[A-Z0-9])', raw) if p.strip()]
    return parts


def extract_from_html(path: Path):
    text = unescape(path.read_text(encoding="utf-8", errors="ignore"))
    entries = []

    # Find occurrences like:
    # "Karol Borsuk, On a new shape invariant, \nTop. Proc. 1 (1976) pp. 1-9."
    pattern = re.compile(
        r'(?P<authors>[^<>\n]{2,}?)\s*,\s*(?P<title>[^<>\n]{5,}?)\s*,\s*Top\. Proc\.'
        r'\s*(?P<volume>\d+)\s*\(\s*(?P<year>\d{4})\s*\)\s*pp\.\s*(?P<pages>[\d\-–]+)\.',
        re.IGNORECASE | re.DOTALL,
    )

    for m in pattern.finditer(text):
        _, end = m.span()
        # look ahead for nearby href with id (tpxxxxx.pdf)
        tail = text[end:end + 400]
        id_match = re.search(r'(tp\d{5})\.pdf', tail)
        item_id = id_match.group(1) if id_match else None

        authors = parse_authors(m.group("authors"))
        title = m.group("title").strip().strip(',')
        volume = int(m.group("volume"))
        year = int(m.group("year"))
        pages = m.group("pages").strip()

        entries.append({
            "authors": authors,
            "title": title,
            "volume": volume,
            "year": year,
            "pages": pages,
            "id": item_id
        })

    return entries


def main():
    out = {}
    for f in sorted(DOWNLOADS.glob("v*_r2.html")):
        entries = extract_from_html(f)
        out[f.name] = entries
        # also write per-file JSON
        (f.parent / (f.stem + "_citations.json")).write_text(json.dumps(entries, indent=2), encoding="utf-8")
    # flatten
    out = [item for sublist in out.values() for item in sublist]
    # write combined file
    (DOWNLOADS / "all_citations.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    # write csv output
    csv_path = DOWNLOADS / "all_citations.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["authors", "title", "volume", "year", "pages", "id"])
        for item in out:
            authors = ", ".join(item.get("authors", []))
            writer.writerow([
                authors,
                item.get("title", ""),
                str(item.get("volume", "")),
                str(item.get("year", "")),
                item.get("pages", ""),
                item.get("id", ""),
            ])
    print("Wrote per-file *_citations.json, downloads/all_citations.json, and downloads/all_citations.csv")
    print (f"Extracted total {len(out)} citations.")


if __name__ == "__main__":
    main()