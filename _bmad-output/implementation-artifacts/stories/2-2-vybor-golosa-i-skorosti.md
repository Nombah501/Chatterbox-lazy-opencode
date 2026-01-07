# Story 2.2 — Выбор голоса и скорости

- Epic: 2 — Озвучка и управление TTS
- Priority: Medium
- Estimate: 3 SP
- Status: done

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

## Tasks
- [x] Обеспечить использование выбранного голоса и скорости.
- [x] Сохранять настройки локально и применять по умолчанию.
- [x] Обработать некорректные значения с безопасным дефолтом.
- [x] Сделать tts.voice и tts.speed доступными через конфиг/флаги.

## Subtasks
- [x] Добавить voice и speed в TtsConfig.
- [x] Добавить CLI-флаги --tts-voice и --tts-speed.
- [x] Передавать voice/speed в model.generate() через kwargs.
- [x] Реализовать _coerce_float() для безопасного парсинга скорости.

## Dev Agent Record
- Date: 2026-01-07
- Agent: Codex
- Notes: Story 2.2 реализована в составе Story 2.5.

## File List
- src/chatterbox_lazy_opencode/config.py
- src/chatterbox_lazy_opencode/cli.py
- src/chatterbox_lazy_opencode/tts/provider.py

## Change Log
- 2026-01-07: Story 2.2 закрыта как done (реализована в составе 2.5).

## Status
- Выполнено
