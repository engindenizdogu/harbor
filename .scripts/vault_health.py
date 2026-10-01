#!/usr/bin/env python3
"""Zero-token vault health checks for Harbor.

python3 .scripts/vault_health.py            full report
python3 .scripts/vault_health.py --session  SessionStart hook: pending sources/inbox,
                                            plus a lint summary at most every 30 days
"""
import difflib
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
RAW = ROOT / ".raw_sources"
INBOX = CONTENT / "_Private" / "Inbox"
STAMP = ROOT / ".quartz-cache" / "vault_health_stamp"
LINT_EVERY_DAYS = 30
SKIP_DIRS = {"_Private", "Templates", "Assets"}
EXEMPT_ORPHAN = {"index", "toc", "Vault To Dos"}
FM_KEYS = {"title", "tags", "draft"}
WIKILINK = re.compile(r"\[\[([^\]|#]+)")


def notes():
    for p in CONTENT.rglob("*.md"):
        if not SKIP_DIRS & set(p.relative_to(CONTENT).parts):
            yield p


def split_front_matter(text):
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    return text[3:end], text[end + 4 :]


def lint():
    files = list(notes())
    inbound, issues = set(), {"front matter": [], "H1 with title": [], "orphans": [],
                              "missing from folder MOC": [], "near-duplicate titles": []}
    mocs = {}
    for p in files:
        for m in WIKILINK.finditer(p.read_text(errors="ignore")):
            inbound.add(m.group(1).strip().lower())
        if p.stem.endswith("MOC"):
            mocs.setdefault(p.parent, p)

    titles = []
    for p in files:
        rel = str(p.relative_to(CONTENT))
        fm, body = split_front_matter(p.read_text(errors="ignore"))
        if fm is None:
            issues["front matter"].append(f"{rel}: no front matter")
        else:
            keys = set(re.findall(r"^([A-Za-z_]+):", fm, re.M))
            if keys != FM_KEYS:
                issues["front matter"].append(f"{rel}: keys {sorted(keys)}")
            if body.lstrip().startswith("# "):
                issues["H1 with title"].append(rel)
        if not p.stem.endswith("MOC"):
            titles.append((p.stem, rel))

        is_moc = p.stem.endswith("MOC")
        if p.stem not in EXEMPT_ORPHAN and not is_moc and p.stem.lower() not in inbound:
            issues["orphans"].append(rel)
        moc = mocs.get(p.parent)
        if moc and not is_moc and p != moc:
            if p.stem.lower() not in {m.group(1).strip().lower()
                                      for m in WIKILINK.finditer(moc.read_text(errors="ignore"))}:
                issues["missing from folder MOC"].append(rel)

    for i, (a, ra) in enumerate(titles):
        for b, rb in titles[i + 1 :]:
            if difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio() > 0.85:
                issues["near-duplicate titles"].append(f"{ra} <-> {rb}")
    return len(files), {k: v for k, v in issues.items() if v}


def pending():
    raw = [p for p in RAW.rglob("*") if p.is_file() and p.name != ".DS_Store"] if RAW.exists() else []
    inbox = list(INBOX.glob("*.md")) if INBOX.exists() else []
    return len(raw), len(inbox)


def report(limit=8):
    total, issues = lint()
    print(f"Vault lint: {total} notes checked, {sum(map(len, issues.values()))} issue(s)")
    for name, items in issues.items():
        print(f"- {name} ({len(items)}):")
        for item in items[:limit]:
            print(f"    {item}")
        if len(items) > limit:
            print(f"    ... {len(items) - limit} more")


def session():
    raw, inbox = pending()
    if raw:
        print(f"[harbor] {raw} file(s) waiting in .raw_sources/: ingest them (see CLAUDE.md).")
    if inbox:
        print(f"[harbor] {inbox} unverified note(s) in content/_Private/Inbox/ awaiting your review.")
    due = not STAMP.exists() or time.time() - STAMP.stat().st_mtime > LINT_EVERY_DAYS * 86400
    if due:
        report(limit=5)
        STAMP.parent.mkdir(exist_ok=True)
        STAMP.touch()


if __name__ == "__main__":
    session() if "--session" in sys.argv else report(limit=50)
