# Story 2.2 — Выбор голоса и скорости

- Epic: 2 — Озвучка и управление TTS
- Priority: Medium
- Estimate: 3 SP
- Status: ready-for-dev

## Краткое описание
Настройка голоса и темпа озвучки.

## Ценность
Комфортное восприятие аудио пользователем.

## Критерии приемки
- При активном TTS озвучка использует выбранные голос и скорость.
- Настройки сохраняются локально и применяются по умолчанию.
- Некорректные значения не ломают вывод и приводят к безопасному дефолту.
- Параметры `tts.voice` и `tts.speed` доступны через конфиг и/или флаги.

## Конфигурация TTS (chatterbox)
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
```

## Зависимости
- Story 2.1 (включение/выключение TTS).

## Ссылки
- `_bmad-output/planning-artifacts/epics-user-stories.md` (Story 2.2)
