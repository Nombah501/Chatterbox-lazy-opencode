from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python < 3.11
    tomllib = None


@dataclass
class TtsConfig:
    enabled: bool = False
    engine: str = "chatterbox"
    model: str = "turbo"  # turbo | multilingual
    device: str = "auto"  # auto | cuda | cpu
    voice_prompt_path: str = ""
    voice: str = "default"
    speed: float = 1.0
    tags_enabled: bool = True
    hf_token: str = ""


@dataclass
class AppConfig:
    tts: TtsConfig = field(default_factory=TtsConfig)


def load_config(path: str | None) -> AppConfig:
    if not path:
        return AppConfig()

    config_path = Path(path)
    if not config_path.exists():
        return AppConfig()

    data = _load_data(config_path)
    return _parse_config(data)


def apply_overrides(config: AppConfig, overrides: dict[str, Any]) -> AppConfig:
    tts_overrides = overrides.get("tts", {})
    config.tts.enabled = _coerce_bool(tts_overrides.get("enabled", config.tts.enabled))
    config.tts.engine = str(tts_overrides.get("engine", config.tts.engine))
    config.tts.model = str(tts_overrides.get("model", config.tts.model))
    config.tts.device = str(tts_overrides.get("device", config.tts.device))
    config.tts.voice_prompt_path = str(
        tts_overrides.get("voice_prompt_path", config.tts.voice_prompt_path)
    )
    config.tts.voice = str(tts_overrides.get("voice", config.tts.voice))
    config.tts.speed = _coerce_float(tts_overrides.get("speed", config.tts.speed))
    config.tts.tags_enabled = _coerce_bool(
        tts_overrides.get("tags_enabled", config.tts.tags_enabled)
    )
    config.tts.hf_token = str(tts_overrides.get("hf_token", config.tts.hf_token))
    return config


def _load_data(path: Path) -> dict[str, Any]:
    if path.suffix.lower() == ".json":
        return json.loads(path.read_text(encoding="utf-8"))
    if path.suffix.lower() == ".toml":
        if tomllib is None:
            return {}
        return tomllib.loads(path.read_text(encoding="utf-8"))
    return {}


def _parse_config(data: dict[str, Any]) -> AppConfig:
    tts_data = data.get("tts", {}) if isinstance(data, dict) else {}
    config = AppConfig()
    return apply_overrides(config, {"tts": tts_data})


def _coerce_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "on"}
    return bool(value)


def _coerce_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 1.0
