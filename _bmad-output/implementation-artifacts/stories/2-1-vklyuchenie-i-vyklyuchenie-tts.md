# Story 2.1 — Включение и выключение TTS

- Epic: 2 — Озвучка и управление TTS
- Priority: High
- Estimate: 3 SP
- Status: review

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
