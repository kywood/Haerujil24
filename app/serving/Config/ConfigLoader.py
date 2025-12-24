import os
import configparser
from typing import Optional


class ConfigLoader:
    def __init__(self, path: str = "config.ini"):
        self.path = path
        self._config = configparser.ConfigParser()

    def load(self) :
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"Config file not found: {self.path}")

        self._config.read(self.path, encoding="utf-8")
        return self

    # ----------------------------
    # Getter APIs
    # ----------------------------
    def get(self, section: str, key: str, default: Optional[str] = None) -> str:
        if self._config.has_option(section, key):
            return self._config.get(section, key)
        if default is not None:
            return default
        raise KeyError(f"Config not found: [{section}] {key}")

    def get_int(self, section: str, key: str, default: Optional[int] = None) -> int:
        if self._config.has_option(section, key):
            return self._config.getint(section, key)
        if default is not None:
            return default
        raise KeyError(f"Config not found: [{section}] {key}")

    def get_bool(self, section: str, key: str, default: Optional[bool] = None) -> bool:
        if self._config.has_option(section, key):
            return self._config.getboolean(section, key)
        if default is not None:
            return default
        raise KeyError(f"Config not found: [{section}] {key}")

    def has(self, section: str, key: str) -> bool:
        return self._config.has_option(section, key)
