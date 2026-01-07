# Story 1.3 — Управление уровнем детализации вывода

- Epic: 1 — Прозрачный синтез результатов
- Priority: Medium
- Estimate: 3 SP
- Status: done

## Краткое описание
Переключение между кратким и подробным выводом и фильтрация секций.

## Ценность
Пользователь контролирует объем информации в CLI.

## Критерии приемки
- По умолчанию используется краткий режим.
- При указании флагов отображаются только выбранные секции.
- В подробном режиме сохраняется структура и порядок секций.

## Зависимости
- Story 1.1 (базовая структура вывода).

## Ссылки
- `_bmad-output/planning-artifacts/epics-user-stories.md` (Story 1.3)

## Tasks
- [x] Добавить флаги для управления выводом секций.
- [x] Реализовать краткий режим по умолчанию.
- [x] Обеспечить сохранение структуры и порядка в подробном режиме.

## Subtasks
- [x] Добавить CLI-флаги --show-summary/--no-summary, --show-divergences/--no-divergences, --show-citations/--no-citations.
- [x] Обновить _format_output() для поддержки фильтрации секций.
- [x] Добавить флаг --verbose для подробного режима.

## Dev Agent Record
- Date: 2026-01-07
- Agent: Codex
- Notes: Реализовано управление детализацией вывода через флаги.

## File List
- src/chatterbox_lazy_opencode/synthesis.py
- src/chatterbox_lazy_opencode/cli.py

## Change Log
- 2026-01-07: Добавлены Tasks/Subtasks для Story 1.3.
- 2026-01-07: Реализованы флаги --show-summary/--show-divergences/--show-citations/--verbose.

## Status
- Выполнено
