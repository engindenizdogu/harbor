"""Ingest notes from .raw_sources/ into content/.

Each top-level folder in .raw_sources/ becomes a domain folder under content/.
Markdown notes are rewritten with vault-conventional front matter, added to the
domain's MOC, and the domain is registered in content/toc.md if it is new.

Scaffold: customize the mapping logic (tags, destination, MOC layout) for each
batch before running. Conventions live in CLAUDE.md.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / ".raw_sources"
CONTENT_DIR = ROOT / "content"
TOC_PATH = CONTENT_DIR / "toc.md"

FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n?", re.DOTALL)
TITLE_LINE = re.compile(r"^title:\s*[\"']?(.*?)[\"']?\s*$", re.MULTILINE)


def clean_summary(body):
    text = re.sub(r"^#+ .*$", "", body, flags=re.MULTILINE)
    text = re.sub(r"\|.*?\|", "", text, flags=re.DOTALL)
    text = re.sub(r"[*_`]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return "Stub."
    return text[:100] + "..." if len(text) > 100 else text


def split_note(content, filename):
    """Return (title, body) with any existing front matter and duplicate H1 removed."""
    title = filename[:-3]
    body = content
    match = FRONT_MATTER.match(content)
    if match:
        body = content[match.end():]
        title_match = TITLE_LINE.search(match.group(1))
        if title_match and title_match.group(1):
            title = title_match.group(1)
    body = re.sub(r"\A\s*# " + re.escape(title) + r"\s*\n", "", body).lstrip("\n")
    return title, body


def register_domain(domain, moc_name):
    """Add a row for a new domain to the table in content/toc.md."""
    lines = TOC_PATH.read_text().split("\n")
    if any(line.startswith(f"| `/{domain}/`") for line in lines):
        return
    rows = [i for i, line in enumerate(lines) if line.startswith("| `/")]
    if not rows:
        print(f"WARNING: no domain table found in {TOC_PATH}; add '{domain}' manually.")
        return
    summary = "TODO: describe this domain."
    lines.insert(rows[-1] + 1, f"| `/{domain}/` | {domain} | [[{moc_name}]] | {summary} |")
    TOC_PATH.write_text("\n".join(lines))


def update_moc(moc_path, domain, tag, moc_lines):
    if moc_path.exists():
        content = moc_path.read_text()
    else:
        content = (
            f"---\ntitle: {domain} MOC\ntags: [{tag}, moc]\ndraft: false\n---\n"
            "Map of Contents\n\n## Notes\n"
        )
    block = "\n".join(moc_lines) + "\n"
    if "## To Research" in content:
        head, tail = content.split("## To Research", 1)
        content = head.rstrip("\n") + "\n" + block + "\n## To Research" + tail
    else:
        content = content.rstrip("\n") + "\n" + block
    moc_path.write_text(content)


def ingest_domain(domain_dir):
    domain = domain_dir.name
    dest_folder = CONTENT_DIR / domain
    dest_folder.mkdir(parents=True, exist_ok=True)
    tag = domain.lower().replace(" ", "-")
    moc_name = f"{domain} MOC"
    moc_lines = []

    for src in sorted(domain_dir.iterdir()):
        if src.name.startswith("."):
            continue
        if src.suffix != ".md":
            print(f"SKIPPED (not markdown, left in place): {src.relative_to(ROOT)}")
            continue
        dest = dest_folder / src.name
        if dest.exists():
            print(f"SKIPPED (already exists, left in place): {dest.relative_to(ROOT)}")
            continue

        title, body = split_note(src.read_text(), src.name)
        front_matter = f"---\ntitle: {title}\ntags: [{tag}]\ndraft: false\n---\n"
        dest.write_text(front_matter + body)
        moc_lines.append(f"- [[{src.stem}]] - {clean_summary(body)}")
        src.unlink()

    if moc_lines:
        update_moc(dest_folder / f"{moc_name}.md", domain, tag, moc_lines)
        register_domain(domain, moc_name)
        print(f"Ingested {len(moc_lines)} note(s) into {domain}/")
    if not any(domain_dir.iterdir()):
        domain_dir.rmdir()


def main():
    if not RAW_DIR.is_dir():
        print(f"No {RAW_DIR} folder; nothing to ingest.")
        return
    for item in sorted(RAW_DIR.iterdir()):
        if item.name.startswith("."):
            continue
        if item.is_dir():
            ingest_domain(item)
        else:
            print(f"SKIPPED (loose file, place it manually): {item.relative_to(ROOT)}")
    print("Ingestion complete. Review any SKIPPED items, then clear .raw_sources/.")


if __name__ == "__main__":
    main()
