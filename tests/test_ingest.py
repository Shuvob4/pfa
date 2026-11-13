from fpa.ingest import sha256_of


def test_same_bytes_different_names_same_hash(tmp_path):
    a = tmp_path / "march.pdf"
    b = tmp_path / "stmt (1) copy.pdf"
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
