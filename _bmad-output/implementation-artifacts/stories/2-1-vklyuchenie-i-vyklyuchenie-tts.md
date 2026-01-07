# Story 2.1 — Включение и выключение TTS

- Epic: 2 — Озвучка и управление TTS
- Priority: High
- Estimate: 3 SP
- Status: done

## Краткое описание
Управление TTS через конфиг или командный флаг.

## Ценность
Пользователь выбирает, нужен ли аудиослой.

## Критерии приемки
- При включении TTS итоговые ответы озвучиваются.
- При выключении TTS озвучка не запускается.
- Состояние TTS сохраняется в конфиге.
- Поддерживаются базовые параметры `tts.enabled` и `tts.engine`.

## Конфигурация TTS (база)
```yaml
tts:
  enabled: false
  engine: "chatterbox"
```

## Зависимости
- Базовая конфигурация CLI.

## Ссылки
- `_bmad-output/implementation-artifacts/sprint-1-checklists.md` (Story 2.1)

## Tasks
- [x] Реализовать базовую конфигурацию TTS с enabled/engine.
- [x] Добавить CLI-флаги --tts/--no-tts.
- [x] Реализовать проверку включенности перед запуском TTS.

## Subtasks
- [x] Создать TtsConfig с enabled/engine.
- [x] Добавить парсинг флагов TTS в CLI.
- [x] Интегрировать проверку enabled в _maybe_speak().

## Dev Agent Record
- Date: 2026-01-07
- Agent: Codex
- Notes: Story 2.1 реализована в рамках Stories 2.3 и 2.5.

## File List
- src/chatterbox_lazy_opencode/config.py
- src/chatterbox_lazy_opencode/cli.py

## Change Log
- 2026-01-07: Story 2.1 закрыта как done (реализована в составе 2.3/2.5).

## Status
- Выполнено
