import pytest

from fpa.config import Config, PathsConfig
from fpa.ingest import find_pdfs, ingest_inbox, sha256_of


@pytest.fixture
def cfg(tmp_path):
    cfg = Config(paths=PathsConfig(data_dir=str(tmp_path)))
    inbox = cfg.inbox_dir
    (inbox / "old").mkdir(parents=True)
    (inbox / "visa march.pdf").write_bytes(b"statement A")
    (inbox / "copy of visa.pdf").write_bytes(b"statement A")
    (inbox / "Statement(2).PDF").write_bytes(b"statement B")
    (inbox / "old" / "jan.pdf").write_bytes(b"statement C")
    (inbox / "notes.txt").write_bytes(b"not a pdf")
    return cfg


def test_same_bytes_different_names_same_hash(tmp_path):
    a = tmp_path / "april.pdf"
    b = tmp_path / "june.pdf"
    a.write_bytes(b"fake pdf content")
    b.write_bytes(b"fake pdf content")
    assert sha256_of(a) == sha256_of(b)


def test_one_changed_byte_changes_hash(tmp_path):
    a = tmp_path / "april.pdf"
    b = tmp_path / "june.pdf"
    a.write_bytes(b"fake pdf content")
    b.write_bytes(b"fake pdf contenT")
    assert sha256_of(a) != sha256_of(b)


def test_known_vector(tmp_path):
    a = tmp_path / "april.pdf"
    a.write_bytes(b"abc")
    assert sha256_of(a) == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"


def test_find_pdfs_recursive_and_case_sensitive(cfg):
    found = find_pdfs(cfg.inbox_dir)
    assert len(found) == 4
    assert all(p.suffix.lower() == ".pdf" for p in found)


def test_ingest_copies_unique_and_skips_duplicates(cfg):
    result = ingest_inbox(cfg)
    assert result.copied == 3
    assert result.duplicates == 1
    raw_files = sorted(cfg.raw_dir.iterdir())
    assert len(raw_files) == 3
    for f in raw_files:
        assert f.name == f"{sha256_of(f)}.pdf"


def test_ingest_twice_is_noop(cfg):
    ingest_inbox(cfg)
    second = ingest_inbox(cfg)
    assert second.copied == 0
    assert second.duplicates == 4
    assert len(list(cfg.raw_dir.iterdir())) == 3


def test_ingest_leaves_inbox_untouched(cfg):
    before = {p: sha256_of(p) for p in find_pdfs(cfg.inbox_dir)}
    ingest_inbox(cfg)
    after = {p: sha256_of(p) for p in find_pdfs(cfg.inbox_dir)}
    assert before == after
