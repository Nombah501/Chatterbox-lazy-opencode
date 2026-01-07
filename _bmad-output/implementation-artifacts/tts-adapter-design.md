# Эскиз архитектуры TTS-адаптера

## Цели
- Инкапсулировать TTS-движок (chatterbox) за стабильным интерфейсом.
- Не блокировать текстовый вывод при ошибках или долгой генерации.
- Обеспечить CPU/GPU fallback и конфигурируемость.

## Интерфейс (пример)
```python
class TtsProvider:
    def is_available(self) -> bool: ...
    def synthesize(self, text: str, config: TtsConfig) -> TtsResult: ...

class TtsConfig:
    enabled: bool
    engine: str  # "chatterbox"
    model: str   # "turbo" | "multilingual"
    device: str  # "auto" | "cuda" | "cpu"
    voice_prompt_path: str
    voice: str
    speed: float
    tags_enabled: bool

class TtsResult:
    success: bool
    warnings: list[str]
    audio_path: str | None
```

## Поток выполнения
1) CLI/конфиг -> `TtsConfig` (валидация, дефолты).
2) `TtsProvider.is_available()` -> определение доступности движка.
3) `synthesize()` вызывается неблокирующе (фон/async).
4) Ошибка TTS не влияет на текстовый вывод; предупреждение логируется/печатается.

## Точки интеграции
- Модуль синтеза вызывает TTS только после формирования секции «Итог».
- Параметры TTS берутся из конфига и CLI-флагов.
- В неинтерактиве и CI TTS принудительно отключен.

## Fallback и ошибки
- `device=auto` -> GPU при наличии, иначе CPU с предупреждением.
- Отсутствие `voice_prompt_path` -> отключение голос-клона.
- Любая ошибка движка -> `success=false`, текстовый вывод продолжается.

## Ограничения
- Первый запуск модели может быть тяжелым; рекомендуется кэширование модели в провайдере.
- Генерация аудио должна быть вынесена из основного потока CLI.
