#!/usr/bin/env python3
"""Zero-token vault health checks for Harbor.

python3 .scripts/vault_health.py            full report
python3 .scripts/vault_health.py --queue --session-id ID  append takeaway entries from stdin
                                            (separate entries with a line of `---`)
python3 .scripts/vault_health.py --drain --session-id ID  print and claim that session's queue
python3 .scripts/vault_health.py --drain --all  print and claim every session's queue
python3 .scripts/vault_health.py --drain --stale  print and claim queues untouched for 12h+
python3 .scripts/vault_health.py --status --session-id ID  list queued entries per session (read-only)
python3 .scripts/vault_health.py --drain-done  delete claimed queue files after processing
python3 .scripts/vault_health.py --session  SessionStart hook: session id, queue status,
                                            pending sources/inbox, plus a
                                            lint summary at most every 30 days
"""
import difflib
import json
import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
RAW = ROOT / ".raw_sources"
INBOX = CONTENT / "_Private" / "Inbox"
STAMP = ROOT / ".quartz-cache" / "vault_health_stamp"
QUEUE = ROOT / ".scripts" / "queue"
DRAINING = QUEUE / "draining"
LINT_EVERY_DAYS = 30
AUTO_FLUSH_HOURS = 12
STALE_DRAIN_MINUTES = 10
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


def hook_input():
    if sys.stdin.isatty():
        return {}
    try:
        return json.load(sys.stdin)
    except ValueError:
        return {}


def safe_id(sid):
    return re.sub(r"[^\w.-]", "_", sid or "") or "manual"


def arg_value(name):
    argv = sys.argv
    return argv[argv.index(name) + 1] if name in argv and argv.index(name) + 1 < len(argv) else None


def queue_files():
    return sorted(QUEUE.glob("*.md")) if QUEUE.exists() else []


def entry_count(path):
    return len(re.findall(r"^## ", path.read_text(errors="ignore"), re.M))


def age_hours(path):
    return (time.time() - path.stat().st_mtime) / 3600


def enqueue(sid):
    entries = [e.strip() for e in re.split(r"^---$", sys.stdin.read(), flags=re.M) if e.strip()]
    if not entries:
        sys.exit("No entries on stdin.")
    QUEUE.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y-%m-%d %H:%M")
    with open(QUEUE / f"{sid}.md", "a") as f:
        for e in entries:
            f.write(f"## {stamp} | {e}\n\n")
    print(f"Queued {len(entries)} entry(ies).")


def drain(sid, mode):
    """Claim queue files by moving them into draining/ (atomic), then print them.
    Files stranded in draining/ by an interrupted flush are picked up after a delay."""
    DRAINING.mkdir(parents=True, exist_ok=True)
    claimed = [p for p in DRAINING.glob("*.md") if time.time() - p.stat().st_mtime > STALE_DRAIN_MINUTES * 60]
    candidates = {"all": queue_files(),
                  "stale": [p for p in queue_files() if age_hours(p) > AUTO_FLUSH_HOURS],
                  "own": [QUEUE / f"{sid}.md"]}[mode]
    for p in candidates:
        dest = DRAINING / f"{int(time.time() * 1000)}-{p.name}"
        try:
            os.rename(p, dest)
        except FileNotFoundError:
            continue
        os.utime(dest)
        claimed.append(dest)
    if not claimed:
        print("Queue empty.")
        return
    for p in claimed:
        print(f"=== session {p.stem.split('-', 1)[1]} ===")
        print(p.read_text().rstrip() + "\n")
    print(f"Drained {len(claimed)} file(s). After writing the notes, run --drain-done.")


def status(sid):
    files = queue_files()
    total = sum(map(entry_count, files))
    print(f"Queue: {total} entry(ies) in {len(files)} session(s); files older than {AUTO_FLUSH_HOURS}h flush at the next session start.")
    for p in files:
        hours = age_hours(p)
        age = f"{hours:.0f}h" if hours >= 1 else f"{hours * 60:.0f}m"
        flag = ", flushes next session start" if hours > AUTO_FLUSH_HOURS else ""
        print(f"- {p.stem}{' (this session)' if p.stem == sid else ''}: {entry_count(p)} entry(ies), last added {age} ago{flag}")
        for m in re.finditer(r"^## \S+ \S+ \| (.*)$", p.read_text(errors="ignore"), re.M):
            print(f"    {m.group(1)}")
    stuck = list(DRAINING.glob("*.md")) if DRAINING.exists() else []
    if stuck:
        print(f"Draining: {len(stuck)} file(s) claimed by a flush in progress or interrupted (picked up after {STALE_DRAIN_MINUTES}m).")


def drain_done():
    for p in DRAINING.glob("*.md") if DRAINING.exists() else []:
        p.unlink()
    print("Cleared drained queue files.")


def queue_status(sid):
    print(f"[harbor] Session id: {sid}. Queue takeaways with --queue --session-id {sid} (see CLAUDE.md).")
    files = queue_files()
    own = QUEUE / f"{sid}.md"
    stale = [p for p in files if age_hours(p) > AUTO_FLUSH_HOURS]
    if own in files and own not in stale:
        print(f"[harbor] This session has {entry_count(own)} queued entry(ies) not yet flushed.")
    fresh = [p for p in files if p != own and p not in stale]
    if fresh:
        print(f"[harbor] {sum(map(entry_count, fresh))} entry(ies) queued by {len(fresh)} other session(s) in the last {AUTO_FLUSH_HOURS}h: they flush automatically once older, or on `/fin`.")
    if stale:
        print(f"[harbor] {sum(map(entry_count, stale))} queued entry(ies) from {len(stale)} session(s) are over {AUTO_FLUSH_HOURS}h old: flush them now, before the first reply "
              f"(`--drain --stale --session-id {sid}`, then notes per CLAUDE.md steps 3-6, then `--drain-done`) and mention it in one line.")
    stranded = [p for p in DRAINING.glob("*.md") if time.time() - p.stat().st_mtime > STALE_DRAIN_MINUTES * 60] if DRAINING.exists() else []
    if stranded:
        print(f"[harbor] {len(stranded)} queue file(s) stuck in .scripts/queue/draining/ from an interrupted flush: the next flush picks them up.")


def session(sid):
    raw, inbox = pending()
    queue_status(sid)
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
    flags = set(sys.argv)
    sid = safe_id(arg_value("--session-id"))
    if "--session" in flags:
        session(safe_id(hook_input().get("session_id")))
    elif "--queue" in flags:
        enqueue(sid)
    elif "--drain" in flags:
        drain(sid, "all" if "--all" in flags else "stale" if "--stale" in flags else "own")
    elif "--status" in flags:
        status(sid)
    elif "--drain-done" in flags:
        drain_done()
    else:
        report(limit=50)
