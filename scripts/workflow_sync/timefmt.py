from __future__ import annotations

import re
from datetime import datetime
from zoneinfo import ZoneInfo

from .collect import parse_frontmatter

DATE_ONLY_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DATETIME_RE = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")


def now_shanghai() -> str:
    return datetime.now(ZoneInfo("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:%S")


def normalize_datetime(value: str | None, *, default_time: str = "00:00:00") -> str | None:
    """Normalize trace/archive timestamps to YYYY-MM-DD HH:mm:ss."""

    if value is None:
        return None
    raw = str(value).strip()
    if not raw or raw.lower() in {"null", "none"}:
        return None
    if DATETIME_RE.match(raw):
        return raw
    if DATE_ONLY_RE.match(raw):
        return f"{raw} {default_time}"
    match = re.match(r"^(\d{4}-\d{2}-\d{2})[ T](\d{2}:\d{2}:\d{2})", raw)
    if match:
        return f"{match.group(1)} {match.group(2)}"
    return None


def touch_frontmatter(text: str, *, force_created: bool = False) -> tuple[str, bool]:
    """Ensure created_at / updated_at exist and bump updated_at."""

    now = now_shanghai()
    if not text.startswith("---"):
        wrapped = (
            "---\n"
            f"created_at: {now}\n"
            f"updated_at: {now}\n"
            "---\n\n"
            f"{text.lstrip()}"
        )
        return wrapped, True

    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return text, False

    body = text[match.end() :]
    fm_text = match.group(1)
    fm = parse_frontmatter(text)
    lines = fm_text.splitlines()
    out: list[str] = []
    has_created = "created_at" in fm
    has_updated = "updated_at" in fm

    for line in lines:
        if line.startswith("created_at:"):
            if not force_created:
                out.append(line)
            else:
                out.append(f"created_at: {now}")
            has_created = True
            continue
        if line.startswith("updated_at:"):
            out.append(f"updated_at: {now}")
            has_updated = True
            continue
        out.append(line)

    if not has_created:
        out.append(f"created_at: {now}")
    if not has_updated:
        out.append(f"updated_at: {now}")

    new_fm = "\n".join(out)
    if new_fm == fm_text:
        return text, False
    return f"---\n{new_fm}\n---{body}", True
