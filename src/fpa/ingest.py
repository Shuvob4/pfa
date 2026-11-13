"""Ingest: fingerprint files and copy new ones into the immutable raw store"""

import hashlib
import shutil
from dataclasses import dataclass
from pathlib import Path

from fpa.config import Config


@dataclass(frozen=True)
class IngestResult:
    copied: int
    duplicates: int


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def find_pdfs(inbox: Path) -> list[Path]:
    return sorted(p for p in inbox.rglob("*") if p.is_file() and p.suffix.lower() == ".pdf")


def ingest_inbox(cfg: Config) -> IngestResult:
    cfg.raw_dir.mkdir(parents=True, exist_ok=True)
    copied = 0
    duplicates = 0
    for src in find_pdfs(cfg.inbox_dir):
        dest = cfg.raw_dir / f"{sha256_of(src)}.pdf"
        if dest.exists():
            duplicates += 1
            continue
        tmp = dest.with_suffix(".tmp")
        shutil.copyfile(src, tmp)
        tmp.replace(dest)
        copied += 1
    return IngestResult(copied=copied, duplicates=duplicates)
