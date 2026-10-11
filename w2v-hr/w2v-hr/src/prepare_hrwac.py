from __future__ import annotations

import gzip
import re
import sys
from pathlib import Path
from collections import Counter

URL_RE = re.compile(r"https?://\S+|www\.\S+")
NONWORD_RE = re.compile(r"[^0-9a-zA-ZčćđšžČĆĐŠŽ\-]+")

TAG_LINE_RE = re.compile(r"^\s*<[^>]+>\s*$")   
S_OPEN_RE = re.compile(r"<s[^>]*>")
S_CLOSE_RE = re.compile(r"</s>")

def norm_token(t: str) -> str | None:
    t = t.strip()
    if not t:
        return None
    t = URL_RE.sub("", t)
    t = t.lower()
    t = NONWORD_RE.sub("", t)
    if len(t) < 2:
        return None
    return t

def extract_hrwac_table(xml_gz_path: Path, out_path: Path, token_limit: int = 5_000_000, log_every: int = 500_000):
    out_path.parent.mkdir(parents=True, exist_ok=True)

    in_sent = False
    sent_tokens: list[str] = []

    total_tokens = 0
    sent_count = 0
    line_count = 0
    freq = Counter()

    with gzip.open(xml_gz_path, "rt", encoding="utf-8", errors="ignore") as fin, \
         out_path.open("w", encoding="utf-8") as fout:

        for line in fin:
            line_count += 1

            if line_count % log_every == 0:
                print(f"[progress] lines={line_count:,} sentences={sent_count:,} tokens={total_tokens:,}")

            line = line.rstrip("\n")

            if S_OPEN_RE.search(line):
                in_sent = True
                sent_tokens.clear()
                continue

            if in_sent and S_CLOSE_RE.search(line):
                if sent_tokens:
                    fout.write(" ".join(sent_tokens) + "\n")
                    sent_count += 1
                in_sent = False
                sent_tokens.clear()
                if total_tokens >= token_limit:
                    break
                continue

            if not in_sent:
                continue

            # ignore pure tag lines like <g/>
            if TAG_LINE_RE.match(line):
                continue

            # token rows: "Adam    Adam    Adam    Npmsn" (tabs/spaces)
            parts = line.split()
            if not parts:
                continue

            tok = norm_token(parts[0])
            if tok:
                sent_tokens.append(tok)
                total_tokens += 1
                freq[tok] += 1

                if total_tokens >= token_limit:
                    if sent_tokens:
                        fout.write(" ".join(sent_tokens) + "\n")
                        sent_count += 1
                    break

    return {
        "out_path": str(out_path),
        "lines": line_count,
        "sentences": sent_count,
        "tokens": total_tokens,
        "top_20": freq.most_common(20),
    }

def main():
    xml_gz = Path("data/raw/hrWaC2.1.01.xml.gz")
    if not xml_gz.exists():
        print(f"ERROR: file not found: {xml_gz}", file=sys.stderr)
        sys.exit(1)

    out = Path("data/work/hrwac_work.txt")

    stats = extract_hrwac_table(xml_gz, out, token_limit=100_000_000)

    print("\nDONE")
    print("Output:", stats["out_path"])
    print("Lines read:", f"{stats['lines']:,}")
    print("Sentences:", f"{stats['sentences']:,}")
    print("Tokens:", f"{stats['tokens']:,}")
    print("Top-20 tokens:")
    for w, c in stats["top_20"]:
        print(f"  {w:15s} {c:,}")

if __name__ == "__main__":
    main()