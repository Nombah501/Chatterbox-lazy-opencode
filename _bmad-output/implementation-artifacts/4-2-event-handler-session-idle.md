# Story 4.2: Event handler session.idle

Status: review

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a пользователь OpenCode,
I want чтобы плагин реагировал на событие `session.idle`,
so that озвучка запускалась автоматически после завершения ответа агента.

## Acceptance Criteria

1. **Given** плагин установлен и OpenCode запущен
   **When** агент завершает ответ (`session.idle`)
   **Then** плагин получает событие с `sessionID`.
2. **Given** получен `sessionID`
   **When** плагин читает сообщения сессии
   **Then** извлекается последний message с ролью `assistant`.
3. **Given** найден последний assistant message
   **When** сообщение содержит несколько текстовых частей
   **Then** все части типа `text` объединяются в одну строку для последующей озвучки.

## Tasks / Subtasks

- [x] Task 1: Добавить обработчик события `session.idle` (AC: 1)
  - [x] Subtask 1.1: Проверить `event.type === "session.idle"` и наличие `event.properties.sessionID`
  - [x] Subtask 1.2: Извлечь `sessionID` как строку и сразу выйти при отсутствии
- [x] Task 2: Получить сообщения сессии и найти последний assistant (AC: 2)
  - [x] Subtask 2.1: Вызвать `client.session.messages({ path: { id: sessionID } })`
  - [x] Subtask 2.2: Отфильтровать сообщения по `info.role === "assistant"` и взять последний
- [x] Task 3: Сформировать строку для озвучки (AC: 3)
  - [x] Subtask 3.1: Собрать `parts` с `type === "text"` и объединить через `\n`
  - [x] Subtask 3.2: Пропустить обработку, если текст пустой
- [x] Task 4: Добавить минимальный тестовый скрипт (запрос пользователя)
  - [x] Subtask 4.1: Создать `scripts/test_opencode_plugin.py`
  - [x] Subtask 4.2: Запустить скрипт и проверить отсутствие ошибок

## Dev Notes

### Developer Context

- Scope: только обработчик `session.idle` и извлечение текста; без вызова `cbx` (Story 4.3) и без конфигурации (Story 4.4).
- Событие: использовать `event.type === "session.idle"`; session id приходит в `event.properties.sessionID`.
- Источник сообщений: `client.session.messages({ path: { id: sessionID } })`.
- Извлекать последний `assistant` из массива сообщений и объединять все `parts` типа `text` через `\n`.
- Если нет `sessionID`, нет assistant message или текст пустой — завершать без ошибок и без логирования критичного уровня.

### Technical Requirements

- Язык/рантайм: TypeScript plugin для OpenCode.
- Типизация: `import type { Plugin } from "@opencode-ai/plugin"`.
- Работать в глобальном плагине `~/.config/opencode/plugin/cbx-speak.ts` (создан в 4.1).
- Никаких новых зависимостей, конфигов и файлов в рамках этой истории.

### Architecture Compliance

- Следовать OpenCode Plugin API (event hook).
- Сохранять неблокирующий UX: все операции async, без тяжелых синхронных операций.

### Testing Requirements

- Для этой истории — smoke-проверка в OpenCode: убедиться, что обработчик не вызывает ошибок при `session.idle`.

### Previous Story Intelligence

- Story 4.1 уже создала глобальный плагин `~/.config/opencode/plugin/cbx-speak.ts` и лог инициализации `cbx-speak initialized`.
- Не создавать дубликаты плагина в репозитории; все изменения только в глобальном файле.
- Не добавлять shell вызовы `cbx` и конфиг — это отдельно в 4.3 и 4.4.

### Git Intelligence Summary

- Последние коммиты в репозитории — документация/планирование, без изменений плагина.
- Изменения этой истории ожидаются только в `~/.config/opencode/plugin/cbx-speak.ts`.

### Latest Tech Information

- OpenCode Plugins: `session.idle` доступен как событие в общем `event` hook.
- SDK `client.session.messages({ path: { id } })` возвращает массив объектов с `info` и `parts`, где `info.role` — роль сообщения, а `parts` — массив частей.

### Project Context Reference

- `project-context.md` не найден; использовать контекст из Epic 4 и исследований.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 4.2]
- [Source: _bmad-output/planning-artifacts/opencode-integration-plan.md#Рекомендуемый подход: OpenCode Plugin]
- [Source: _bmad-output/planning-artifacts/research-opencode-plugin-integration.md#2.1 Plugin System (Рекомендуется)]
- [Source: https://opencode.ai/docs/plugins/#events]
- [Source: https://opencode.ai/docs/sdk/#sessions]

## Dev Agent Record

### Agent Model Used

GPT-5

### Debug Log References

### Completion Notes List

- Реализован обработчик `session.idle` с извлечением sessionID и сообщений.
- Добавлено извлечение последнего assistant message и сбор текстовых частей.
- Создан минимальный тестовый скрипт по запросу пользователя; проверка пройдена.
- Story переведена в review для последующего code review.

### File List

- `_bmad-output/implementation-artifacts/4-2-event-handler-session-idle.md`
- `~/.config/opencode/plugin/cbx-speak.ts`
- `scripts/test_opencode_plugin.py`

## Change Log

- 2026-01-07: Создана story 4.2 с контекстом и требованиями.
- 2026-01-07: Реализован обработчик session.idle и извлечение текста.
- 2026-01-07: Добавлен минимальный тестовый скрипт по запросу пользователя.
- 2026-01-07: Статус переведен в review.

## Status

review
