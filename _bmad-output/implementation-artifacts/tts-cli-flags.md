# CLI-флаги для TTS

## Базовые
- `--tts` / `--no-tts`
- `--tts-engine chatterbox`

## Параметры chatterbox
- `--tts-model turbo|multilingual`
- `--tts-device auto|cuda|cpu`
- `--tts-voice "default"`
- `--tts-speed 1.0`
- `--tts-voice-prompt /path/to/ref.wav`
- `--tts-tags` / `--no-tts-tags`
- `--tts-hf-token <token>`

## Приоритеты
1) CLI-флаги
2) Конфиг
3) Дефолты

## Валидация
- Некорректные значения приводятся к дефолтам с предупреждением.
- При `--no-tts` остальные параметры игнорируются.
