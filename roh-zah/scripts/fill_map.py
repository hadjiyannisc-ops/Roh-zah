#!/usr/bin/env python3
"""Fill the Roh-zah course map template with data.

Usage:
    python3 fill_map.py map.json out.html            # fragment for an inline visual widget
    python3 fill_map.py map.json out.html --page     # standalone page (artifact or file)
"""
import html as _html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "..", "assets", "course-map.html")


def fill(data, page=False):
    with open(TEMPLATE, encoding="utf-8") as fh:
        html = fh.read()
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    html = html.replace("__ROHZAH_DATA__", payload)
    if page:
        title = _html.escape((data.get("course") or "Course") + " · Course map")
        html = ("<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"utf-8\">"
                "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
                f"<title>{title}</title></head>"
                "<body style=\"margin:0;padding:24px 16px;background:#FAF9F7\">"
                "<main style=\"max-width:720px;margin:0 auto\">"
                f"<h1 style=\"font:500 22px system-ui,sans-serif;margin:0 0 12px\">{title}</h1>"
                + html + "</main></body></html>")
    return html


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as fh:
        d = json.load(fh)
    with open(sys.argv[2], "w", encoding="utf-8") as fh:
        fh.write(fill(d, page="--page" in sys.argv))
    print(sys.argv[2])
