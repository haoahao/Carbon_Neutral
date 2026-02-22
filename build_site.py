#!/usr/bin/env python3
from __future__ import annotations

import csv
import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
INPUT_FILE = ROOT / "review_responses.tsv"
OUTPUT_DIR = ROOT / "docs"
OUTPUT_FILE = OUTPUT_DIR / "index.html"
ROOT_INDEX = ROOT / "index.html"


def split_response_and_page(text: str) -> tuple[str, str]:
    marker = "頁碼："
    if marker not in text:
        return text.strip(), "第＿＿＿頁至第＿＿＿頁"
    left, right = text.rsplit(marker, 1)
    response = left.strip().rstrip("。")
    page = right.strip().rstrip("。")
    if not page:
        page = "第＿＿＿頁至第＿＿＿頁"
    return response, page


def parse_rows(path: Path) -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f, delimiter="\t")
        header_seen = False
        for row in reader:
            if not row:
                continue
            if not header_seen:
                header_seen = True
                continue
            if len(row) < 2:
                continue
            opinion = row[0].strip()
            response_full = row[1].strip()
            if opinion and response_full:
                response, page = split_response_and_page(response_full)
                rows.append((opinion, response, page))
    return rows


def linebreak_to_html(text: str) -> str:
    escaped = html.escape(text)
    return escaped.replace("\n", "<br>")


def to_bullets(text: str) -> list[str]:
    text = text.strip()
    if not text:
        return []
    numbered = re.findall(r"((?<!\d)\d+\.\s+.*?)(?=(?:(?<!\d)\d+\.\s+)|$)", text)
    if numbered:
        return [item.strip() for item in numbered if item.strip()]
    lines = [seg.strip() for seg in text.split("\n") if seg.strip()]
    if len(lines) > 1:
        return lines
    return [text]


def list_html(text: str) -> str:
    items = to_bullets(text)
    rendered = "".join(f"<li>{linebreak_to_html(item)}</li>" for item in items)
    return f'<ul class="cell-list">{rendered}</ul>'


def build_html(rows: list[tuple[str, str, str]]) -> str:
    table_rows = []
    for opinion, response, page in rows:
        table_rows.append(
            "      <tr>\n"
            f"        <td>{list_html(opinion)}</td>\n"
            f"        <td>{list_html(response)}</td>\n"
            f"        <td>{list_html(page)}</td>\n"
            "      </tr>"
        )

    return f"""<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; img-src 'self' data:; font-src 'self'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'; upgrade-insecure-requests">
  <meta name="referrer" content="no-referrer">
  <meta name="robots" content="index,follow,max-image-preview:none">
  <meta name="description" content="114年度碳中和中程計畫審查意見修正對照表，提供教育局報送使用。">
  <meta name="color-scheme" content="light">
  <link rel="canonical" href="https://haoahao.github.io/Carbon_Neutral/">
  <title>114年度碳中和中程計畫 審查意見修正對照表</title>
  <style>
    :root {{
      --bg: #f4f7f2;
      --card: #ffffff;
      --line: #d7dfd4;
      --head: #2a4f35;
      --headText: #f7fbf8;
      --text: #1f2a22;
      --muted: #5d6e62;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "Noto Sans TC", "Microsoft JhengHei", sans-serif;
      color: var(--text);
      background:
        radial-gradient(1000px 300px at 10% -20%, #dfeadb 0%, transparent 60%),
        radial-gradient(700px 240px at 100% 0%, #e9efe4 0%, transparent 55%),
        var(--bg);
    }}
    .wrap {{
      max-width: 1180px;
      margin: 32px auto;
      padding: 0 16px 24px;
    }}
    .hero {{
      background: linear-gradient(135deg, #2f5f41 0%, #244832 100%);
      color: #fff;
      border-radius: 14px;
      padding: 22px 20px;
      margin-bottom: 18px;
      box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
    }}
    .hero h1 {{
      margin: 0 0 8px;
      font-size: 1.28rem;
      line-height: 1.4;
    }}
    .hero p {{
      margin: 0;
      color: #e4efe8;
      font-size: .95rem;
    }}
    .card {{
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 14px;
      overflow: hidden;
      box-shadow: 0 10px 24px rgba(10, 30, 10, .06);
    }}
    .scroll {{
      overflow-x: auto;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      min-width: 980px;
    }}
    th, td {{
      vertical-align: top;
      border: 1px solid var(--line);
      padding: 12px;
      line-height: 1.6;
      font-size: 0.95rem;
    }}
    th {{
      background: var(--head);
      color: var(--headText);
      text-align: left;
      position: sticky;
      top: 0;
      z-index: 1;
    }}
    td:first-child {{
      width: 26%;
      background: #f8fcf7;
      font-weight: 700;
    }}
    td:nth-child(2) {{
      width: 56%;
    }}
    td:nth-child(3) {{
      width: 18%;
      white-space: nowrap;
    }}
    .cell-list {{
      margin: 0;
      padding-left: 1.1rem;
    }}
    .cell-list li {{
      margin: 0 0 .3rem 0;
    }}
    .cell-list li:last-child {{
      margin-bottom: 0;
    }}
    .footer {{
      margin-top: 14px;
      color: var(--muted);
      font-size: .86rem;
    }}
    @media (max-width: 768px) {{
      .wrap {{ margin: 18px auto; }}
      .hero h1 {{ font-size: 1.1rem; }}
      th, td {{ padding: 10px; font-size: .9rem; }}
    }}
  </style>
</head>
<body>
  <main class="wrap">
    <section class="hero">
      <h1>114年度「碳中和中程計畫」審查意見修正對照表</h1>
      <p>三欄格式：審查意見 / 修正情形 / 頁碼（可直接列印或作為附件）</p>
    </section>
    <section class="card">
      <div class="scroll">
        <table>
          <thead>
            <tr>
              <th>審查意見</th>
              <th>修正情形</th>
              <th>頁碼</th>
            </tr>
          </thead>
          <tbody>
{chr(10).join(table_rows)}
          </tbody>
        </table>
      </div>
    </section>
    <p class="footer">此頁由 <code>build_site.py</code> 依 <code>review_responses.tsv</code> 自動產生。</p>
  </main>
</body>
</html>
"""


def main() -> None:
    rows = parse_rows(INPUT_FILE)
    if not rows:
        raise SystemExit("No rows found in review_responses.tsv")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    html_content = build_html(rows)
    OUTPUT_FILE.write_text(html_content, encoding="utf-8")
    ROOT_INDEX.write_text(html_content, encoding="utf-8")
    print(f"Generated: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
