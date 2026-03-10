#!/usr/bin/env python3
import argparse
import re
from datetime import datetime, timezone

ACTION_PAT = re.compile(r"(todo|to do|action|follow up|need to|should|must|please|let's|deadline|owner|需要|请|跟进|最晚|之前|今晚|明天|本周|负责人)", re.I)
DECISION_PAT = re.compile(r"(decide|decision|agreed|we will|approved|choose|chosen|决定|确定|采用|优先|延期)", re.I)
RISK_PAT = re.compile(r"(blocker|risk|issue|problem|delay|stuck|风险|问题|阻塞|卡住|延期)", re.I)


def clean(line: str) -> str:
    return re.sub(r"\s+", " ", line.strip())


def split_lines(text: str):
    parts = re.split(r"[\n\r]+", text)
    return [clean(p) for p in parts if clean(p)]


def pick(lines, pat, limit=5):
    out = []
    for ln in lines:
        if pat.search(ln):
            out.append(ln)
        if len(out) >= limit:
            break
    return out


def to_markdown(lines):
    actions = pick(lines, ACTION_PAT, 5)
    decisions = pick(lines, DECISION_PAT, 3)
    risks = pick(lines, RISK_PAT, 3)

    summary = lines[:3] if len(lines) >= 3 else lines

    md = []
    md.append(f"# Meeting QuickCut\n")
    md.append(f"- Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    md.append(f"- Input lines: {len(lines)}\n")

    md.append("## 3-line Summary")
    for s in summary:
        md.append(f"- {s}")

    md.append("\n## 5 Action Items")
    if actions:
        for a in actions:
            md.append(f"- [ ] {a}")
    else:
        md.append("- [ ] No explicit actions detected (please add manually)")

    md.append("\n## Decisions")
    if decisions:
        for d in decisions:
            md.append(f"- {d}")
    else:
        md.append("- No clear decision statements detected")

    md.append("\n## Risks / Blockers")
    if risks:
        for r in risks:
            md.append(f"- {r}")
    else:
        md.append("- No obvious blockers detected")

    return "\n".join(md) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Convert raw meeting transcript text into summary + actions markdown")
    ap.add_argument("input", help="Path to transcript text file")
    ap.add_argument("-o", "--output", default="meeting_brief.md", help="Output markdown path")
    args = ap.parse_args()

    text = open(args.input, "r", encoding="utf-8").read()
    lines = split_lines(text)
    md = to_markdown(lines)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"Written {args.output}")


if __name__ == "__main__":
    main()
