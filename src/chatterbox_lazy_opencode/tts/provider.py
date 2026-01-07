from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
from typing import Any

from chatterbox_lazy_opencode.config import TtsConfig


@dataclass
class TtsResult:
    success: bool
    warnings: list[str]
    audio_path: str | None = None


class ChatterboxProvider:
    def __init__(self) -> None:
        self._models: dict[str, Any] = {}

    def is_available(self) -> bool:
        try:
            import chatterbox  # noqa: F401
        except Exception:
            return False
        return True

    def synthesize(self, text: str, config: TtsConfig, output_path: str) -> TtsResult:
        warnings: list[str] = []

        if not config.enabled:
            return TtsResult(success=False, warnings=["TTS выключен"], audio_path=None)

        if not self.is_available():
            return TtsResult(
                success=False, warnings=["chatterbox недоступен"], audio_path=None
            )

        device = _resolve_device(config.device)
        if device == "cpu" and config.device == "auto":
            warnings.append("GPU не найден, используется CPU")

        _configure_hf_token(config.hf_token)
        model = self._get_model(config.model, device)
        audio = _generate_audio(model, text, config, warnings)
        if audio is None:
            return TtsResult(success=False, warnings=warnings, audio_path=None)

        audio_path = Path(output_path)
        _save_audio(audio_path, audio, getattr(model, "sr", 24000))
        return TtsResult(success=True, warnings=warnings, audio_path=str(audio_path))

    def _get_model(self, model_name: str, device: str) -> Any:
        if model_name not in {"turbo", "multilingual"}:
            model_name = "turbo"
        cache_key = f"{model_name}:{device}"
        if cache_key in self._models:
            return self._models[cache_key]

        device_arg: Any = device
        if model_name == "turbo":
            from chatterbox.tts_turbo import ChatterboxTurboTTS

            model = ChatterboxTurboTTS.from_pretrained(device=device_arg)  # type: ignore[arg-type]
        else:
            from chatterbox.mtl_tts import ChatterboxMultilingualTTS

            model = ChatterboxMultilingualTTS.from_pretrained(device=device_arg)  # type: ignore[arg-type]

        self._models[cache_key] = model
        return model


def _configure_hf_token(token: str) -> None:
    if not token:
        return
    os.environ.setdefault("HF_TOKEN", token)
    os.environ.setdefault("HUGGINGFACE_HUB_TOKEN", token)


def _resolve_device(requested: str) -> str:
    if requested in {"cuda", "cpu"}:
        return requested
    try:
        import torch

        return "cuda" if torch.cuda.is_available() else "cpu"
    except Exception:
        return "cpu"


def _generate_audio(model: Any, text: str, config: TtsConfig, warnings: list[str]):
    if config.voice_prompt_path:
        prompt_path = Path(config.voice_prompt_path)
        if not prompt_path.exists():
            warnings.append("voice prompt не найден, голос-клон отключен")
            return model.generate(text)
        return model.generate(text, audio_prompt_path=str(prompt_path))
    return model.generate(text)


def _save_audio(path: Path, audio: Any, sample_rate: int) -> None:
    try:
        import torchaudio as ta
    except Exception as exc:
        raise RuntimeError("torchaudio недоступен") from exc

    path.parent.mkdir(parents=True, exist_ok=True)
    ta.save(str(path), audio, sample_rate)
