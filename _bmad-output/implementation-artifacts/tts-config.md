# Конфигурация TTS

## Базовые параметры
```yaml
tts:
  enabled: false
  engine: "chatterbox"
```

## Параметры chatterbox
```yaml
tts:
  enabled: false
  engine: "chatterbox"
  model: "turbo" # turbo | multilingual
  device: "auto" # auto | cuda | cpu
  voice_prompt_path: ""
  voice: "default"
  speed: 1.0
  tags_enabled: true
  hf_token: ""
```

## Примечания
- `hf_token` можно задать в конфиге или через переменную окружения `HF_TOKEN`.
- `device: auto` выбирает GPU при доступности, иначе CPU.
- `voice_prompt_path` используется для голос-клона; пустое значение отключает его.
- `tags_enabled` позволяет пропускать парлингвистические теги в текст.
- Некорректные значения приводятся к безопасным дефолтам без падения.
