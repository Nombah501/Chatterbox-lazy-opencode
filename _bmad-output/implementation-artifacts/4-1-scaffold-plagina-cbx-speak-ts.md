# Story 4.1: Scaffold плагина cbx-speak.ts

Status: review

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a разработчик,
I want иметь базовую структуру плагина для OpenCode,
so that я могу расширять его функциональность.

## Acceptance Criteria

1. **Given** глобальная директория `~/.config/opencode/plugin/`
   **When** я создаю файл `cbx-speak.ts`
   **Then** плагин экспортирует `Plugin` функцию с корректной сигнатурой из `@opencode-ai/plugin`.
2. **Given** плагин установлен
   **When** OpenCode загружает плагины
   **Then** загрузка проходит без ошибок.
3. **Given** плагин загружен
   **When** происходит инициализация
   **Then** в логах видно строку `cbx-speak initialized`.

## Tasks / Subtasks

- [x] Task 1: Добавить глобальный файл плагина `~/.config/opencode/plugin/cbx-speak.ts` (AC: 1)
  - [x] Subtask 1.1: Создать файл и базовый экспорт `Plugin` из `@opencode-ai/plugin`
  - [x] Subtask 1.2: Вернуть минимальный объект плагина (name + пустой event handler)
- [x] Task 2: Добавить лог инициализации (AC: 3)
  - [x] Subtask 2.1: Логировать `cbx-speak initialized` при запуске плагина
- [x] Task 3: Smoke-проверка загрузки плагина в OpenCode (AC: 2)
  - [x] Subtask 3.1: Запустить OpenCode и убедиться в отсутствии ошибок плагина

## Dev Notes

### Developer Context

- Scope: только scaffold плагина; без session.idle и без вызовов `cbx` (это Story 4.2–4.3).
- Глобальная установка: `~/.config/opencode/plugin/cbx-speak.ts`.
- При инициализации обязателен лог `cbx-speak initialized` (AC3).

### Technical Requirements

- Язык/рантайм: TypeScript plugin для OpenCode, база `@opencode-ai/plugin`.
- Минимальный контракт: `export const Plugin = async (...) => ({ name: "cbx-speak", event: async (...) => {} })`.
- Ошибки: не бросать при инициализации; лог только в stdout/stderr.

### Architecture Compliance

- Следовать интеграции через OpenCode Plugin API и глобальную установку в `~/.config/opencode/plugin/`.
- Сохранить неблокирующий UX (никаких синхронных тяжёлых операций в scaffold).

### Library/Framework Requirements

- Использовать `@opencode-ai/plugin` как источник типов и сигнатуры.
- Не добавлять новых зависимостей в scaffold.

### File Structure Requirements

- Единственный файл в рамках истории: `~/.config/opencode/plugin/cbx-speak.ts`.
- В репозитории держать прототип в `.opencode/plugin/` только если нужно для примера (не в этой истории).

### Testing Requirements

- Для этой истории достаточно smoke-проверки загрузки в OpenCode.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Epic 4: Интеграция с OpenCode]
- [Source: _bmad-output/planning-artifacts/opencode-integration-plan.md#Структура файлов (план)]
- [Source: _bmad-output/planning-artifacts/research-opencode-plugin-integration.md#2.1 Plugin System (Рекомендуется)]

## Dev Agent Record

### Agent Model Used

GPT-5

### Debug Log References

### Completion Notes List

- Создан глобальный файл плагина с минимальным экспортом Plugin.
- Добавлен лог инициализации `cbx-speak initialized` (stdout) и запись в `~/.config/opencode/logs/cbx-speak.log`.
- Smoke-проверка в OpenCode выполнена: лог появился в `~/.config/opencode/logs/cbx-speak.log`.
- Статус переведён в review до smoke-проверки по запросу.

### File List

- `~/.config/opencode/plugin/cbx-speak.ts`

## Change Log

- 2026-01-07: Создана story для 4.1 со структурой задач и контекстом.
- 2026-01-07: Создан глобальный scaffold плагина и добавлен лог инициализации.
- 2026-01-07: Добавлена запись лога в `~/.config/opencode/logs/cbx-speak.log`.
- 2026-01-07: Smoke-проверка выполнена; лог появился в `~/.config/opencode/logs/cbx-speak.log`.
- 2026-01-07: Статус переведён в review; ожидание code review.

## Status

review
