"""Load fpa settings: built-in defaults, optionally overridden by a TOML file."""

import os
import tomllib
from pathlib import Path

import platformdirs
from pydantic import BaseModel, ConfigDict, Field

APP_NAME = "fpa"
CONFIG_FILENAME = "fpa.toml"
ENV_VAR = "FPA_CONFIG"


class PathsConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    data_dir: str = ""  # "" means "use the OS default"


class LLMConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    enabled: bool = True
    base_url: str = "http://localhost:11434"
    model: str = "qwen3:4b"


class Config(BaseModel):
    model_config = ConfigDict(extra="forbid")
    paths: PathsConfig = Field(default_factory=PathsConfig)
    llm: LLMConfig = Field(default_factory=LLMConfig)

    @property
    def data_dir(self) -> Path:
        if self.paths.data_dir:  # user typed a folder
            return Path(self.paths.data_dir).expanduser().resolve()
        return Path(platformdirs.user_data_dir(APP_NAME))  # empty → macOS default

    @property
    def inbox_dir(self) -> Path:
        return self.data_dir / "inbox"

    @property
    def raw_dir(self) -> Path:
        return self.data_dir / "raw"

    @property
    def db_path(self) -> Path:
        return self.data_dir / "fpa.duckdb"

    @property
    def overrides_path(self) -> Path:
        return self.data_dir / "overrides.csv"


def user_config_path() -> Path:
    return Path(platformdirs.user_config_dir(APP_NAME)) / CONFIG_FILENAME


def find_config_file() -> Path | None:
    env_value = os.environ.get(ENV_VAR)  # 1. FPA_CONFIG set? use it
    if env_value:
        return Path(env_value).expanduser()
    default = user_config_path()  # 2. file in the OS config folder?
    return default if default.exists() else None  # 3. nothing → None


def load_config(path: Path | None = None) -> Config:
    path = path or find_config_file()
    if path is None:
        return Config()  # no file → defaults
    with path.open("rb") as f:  # tomllib needs binary mode
        data = tomllib.load(f)  # TOML text → dict
    return Config.model_validate(data)  # dict → checked Config
