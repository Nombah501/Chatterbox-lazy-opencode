# Story 2.3 — Озвучка итогов с fallback

- Epic: 2 — Озвучка и управление TTS
- Priority: High
- Estimate: 3 SP
- Status: done

## Краткое описание
Озвучка итогов не должна блокировать текстовый поток и должна иметь fallback при сбоях.

## Ценность
Результат остается доступным даже при проблемах с TTS.

## Критерии приемки
- При недоступном TTS-воркере текстовый вывод остается полным.
- Показывается предупреждение о сбое TTS.
- Озвучка не блокирует завершение команды синтеза.

## Зависимости
- Story 2.1 (включение/выключение TTS).

## Ссылки
- `_bmad-output/implementation-artifacts/sprint-1-checklists.md` (Story 2.3)

## Tasks
- [x] Обеспечить неблокирующий запуск TTS в CLI.
- [x] Добавить безопасный fallback и предупреждения при сбое TTS.
- [x] Проверить вывод текста при ошибках/медленном TTS.

## Subtasks
- [x] Запускать озвучку в фоновом потоке без ожидания.
- [x] Обработать исключения провайдера и вернуть предупреждения.
- [x] Печатать предупреждения в stderr без падения CLI.

## Dev Agent Record
- Date: 2026-01-07
- Agent: Codex
- Notes: Реализована неблокирующая озвучка и fallback.
- Date: 2026-01-07
- Agent: Codex
- Notes: Code-review завершен, все критерии приемки выполнены, MEDIUM/LOW issues исправлены.

## File List
- src/chatterbox_lazy_opencode/cli.py
- src/chatterbox_lazy_opencode/tts/provider.py

## Change Log
- 2026-01-07: Добавлены Tasks/Subtasks для Story 2.3.
- 2026-01-07: Неблокирующий TTS и безопасный fallback в CLI/провайдере.
- 2026-01-07: Code-review прошел без HIGH/CRITICAL issues.
- 2026-01-07: Исправлены MEDIUM/LOW issues (HF_TOKEN, voice/speed/tags, mkdir, логирование цитат).
- 2026-01-07: Story 2.3 закрыта как done.

## Status
- Выполнено
