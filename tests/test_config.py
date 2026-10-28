from pathlib import Path

import pytest
from pydantic import ValidationError

from fpa.config import load_config


def write_toml(tmp_path: Path, text: str) -> Path:
    path = tmp_path / "fpa.toml"
    path.write_text(text, encoding="utf-8")
    return path


def test_defaults_when_no_config_file(monkeypatch, tmp_path):
    monkeypatch.delenv("FPA_CONFIG", raising=False)
    monkeypatch.setattr("fpa.config.user_config_path", lambda: tmp_path / "missing.toml")
    cfg = load_config()
    assert cfg.llm.model == "qwen3:4b"


def test_unknown_key_is_rejected(tmp_path):
    path = write_toml(tmp_path, '[llm]\nmodle = "qwen3:4b"\n')
    with pytest.raises(ValidationError):
        load_config(path)


def test_file_overrides_only_what_it_sets(tmp_path):
    path = write_toml(tmp_path, "[llm]\nenabled = false\n")
    cfg = load_config(path)
    assert cfg.llm.enabled is False
    assert cfg.llm.model == "qwen3:4b"  # untouched → still the default


def test_tilde_expansion_in_paths(tmp_path):
    path = write_toml(tmp_path, '[paths]\ndata_dir = "~/somewhere"\n')
    cfg = load_config(path)
    assert cfg.data_dir == Path.home() / "somewhere"


def test_env_var_points_to_config(monkeypatch, tmp_path):
    path = write_toml(tmp_path, '[llm]\nmodel = "llama3.2:3b"\n')
    monkeypatch.setenv("FPA_CONFIG", str(path))
    cfg = load_config()  # no argument → must find it via the env var
    assert cfg.llm.model == "llama3.2:3b"
