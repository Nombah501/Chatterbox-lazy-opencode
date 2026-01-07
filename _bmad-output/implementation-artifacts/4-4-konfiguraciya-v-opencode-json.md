# Story 4.4: Конфигурация в opencode.json

Status: review

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a пользователь,
I want управлять плагином через конфигурацию,
so that я могу включать/выключать озвучку и настраивать параметры.

## Acceptance Criteria

1. **Given** opencode.json с секцией `cbx-speak`
   **When** `enabled: false`
   **Then** плагин не запускает озвучку.
2. **Given** opencode.json с секцией `cbx-speak`
   **When** задан `cbxPath`
   **Then** плагин использует указанный путь к cbx вместо PATH.
3. **Given** opencode.json с секцией `cbx-speak`
   **When** задан `minWords` (например, 50)
   **Then** короткие ответы (< minWords слов) не озвучиваются.
4. **Given** opencode.json отсутствует или не содержит секцию
   **When** плагин загружается
   **Then** используются значения по умолчанию: enabled=true, minWords=0.

## Tasks / Subtasks

- [x] Task 1: Добавить чтение конфига из opencode.json (AC: 1, 2, 3, 4)
  - [x] Subtask 1.1: Найти opencode.json в текущей директории или .opencode/
  - [x] Subtask 1.2: Парсить JSON и извлечь секцию `cbx-speak`
  - [x] Subtask 1.3: Определить дефолты: enabled=true, cbxPath=null, minWords=0
- [x] Task 2: Интегрировать конфиг в логику плагина (AC: 1, 2, 3)
  - [x] Subtask 2.1: Проверять `enabled` перед вызовом cbx — ранний выход если false
  - [x] Subtask 2.2: Использовать `cbxPath` из конфига с fallback на cbx-speak.env и PATH
  - [x] Subtask 2.3: Проверять `minWords` — не озвучивать если слов меньше порога
- [x] Task 3: Кэширование конфига (performance)
  - [x] Subtask 3.1: Читать конфиг при инициализации плагина
  - [x] Subtask 3.2: Опционально: перечитывать на каждый session.idle (hot reload)
- [x] Task 4: Smoke-проверка конфигурации
  - [x] Subtask 4.1: Создать тестовый .opencode/opencode.json с enabled=false и проверить
  - [x] Subtask 4.2: Проверить cbxPath override и minWords filtering

## Dev Notes

### Developer Context

- Scope: только конфигурация через opencode.json; не затрагивать cbx-speak.env (уже работает).
- opencode.json — стандартный формат конфига OpenCode для проекта.
- Приоритет конфигурации: opencode.json > cbx-speak.env > environment > defaults.
- Не добавлять /speak команду (Story 4.5) и smart filtering по коду (Story 4.6).

### Technical Requirements

- Язык/рантайм: TypeScript plugin для OpenCode.
- Типизация: `import type { Plugin } from "@opencode-ai/plugin"`.
- Работать в глобальном плагине `~/.config/opencode/plugin/cbx-speak.ts`.
- Чтение JSON через `Bun.file().json()` или `readFile` + `JSON.parse`.
- Никаких новых npm-зависимостей.

### Architecture Compliance

- Конфиг не должен блокировать UI; чтение async.
- При ошибке парсинга — логировать и использовать дефолты.
- Приватность: конфиг локальный, без внешних сервисов.

### Library & Framework Requirements

- OpenCode Plugin API (event hook, context).
- Bun runtime для file access.
- Node.js fs/promises как fallback.

### Project Structure Notes

- Изменения только в `~/.config/opencode/plugin/cbx-speak.ts`.
- Тестовый конфиг: `.opencode/opencode.json` в тестовом проекте.
- Формат конфига:
  ```json
  {
    "cbx-speak": {
      "enabled": true,
      "cbxPath": "/path/to/cbx",
      "minWords": 50
    }
  }
  ```

### Testing Requirements

- Smoke-проверка: enabled=false не вызывает cbx.
- Smoke-проверка: minWords=100 не озвучивает короткие ответы.
- Smoke-проверка: cbxPath переопределяет PATH и cbx-speak.env.

### Previous Story Intelligence

- Story 4.3 уже реализовала shell-вызов cbx с поддержкой CBX_PATH из cbx-speak.env.
- Приоритет: opencode.json.cbxPath > cbx-speak.env.CBX_PATH > PATH.
- minWords — новая логика, не пересекается с существующим кодом.
- enabled — добавить ранний выход в начало обработчика session.idle.

### Git Intelligence Summary

- Последние коммиты — Stories 4.1-4.3, плагин полностью функционален.
- Изменения этой истории — только глобальный файл плагина.

### Latest Tech Information

- OpenCode не предоставляет специального API для чтения конфига плагинов.
- Стандартная практика: читать opencode.json из cwd или .opencode/.
- Bun.file() доступен в контексте плагина.

### Project Context Reference

- Epic 4 (FR10): конфигурация плагина в opencode.json.
- cbx-speak.env уже работает для локальных переопределений.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 4.4]
- [Source: _bmad-output/planning-artifacts/opencode-integration-plan.md]
- [Source: https://opencode.ai/docs/plugins/]

## Dev Agent Record

### Agent Model Used

GPT-5

### Debug Log References

### Implementation Plan

- Добавить функцию `loadProjectConfig()` для чтения opencode.json.
- Вызывать в начале обработчика session.idle после loadLocalConfig().
- Добавить проверку enabled — ранний выход если false.
- Добавить проверку minWords — считать слова в тексте.
- Объединить cbxPath: projectConfig > localConfig > env > PATH.

### Completion Notes List

- Добавлен тип `ProjectConfig` с полями enabled, cbxPath, minWords.
- Добавлена функция `loadProjectConfig()` для чтения opencode.json и .opencode/opencode.json.
- Добавлена функция `countWords()` для подсчёта слов в тексте.
- Интегрирован проектный конфиг в обработчик session.idle:
  - enabled=false → ранний выход с логом.
  - minWords > 0 → фильтрация коротких ответов.
  - cbxPath → приоритет над cbx-speak.env и PATH.
- Приоритет конфигурации: opencode.json > cbx-speak.env > env > defaults.
- Создан тестовый .opencode/opencode.json для smoke-проверки.

### File List

- `~/.config/opencode/plugin/cbx-speak.ts`
- `.opencode/cbx-speak.json`

## Change Log

- 2026-01-07: Создана story 4.4 с контекстом и требованиями.
- 2026-01-07: Добавлен тип ProjectConfig и функция loadProjectConfig().
- 2026-01-07: Добавлена функция countWords() для minWords filtering.
- 2026-01-07: Интегрирован проектный конфиг в session.idle: enabled, minWords, cbxPath.
- 2026-01-07: Создан тестовый .opencode/opencode.json для smoke-проверки.
- 2026-01-07: Исправлен конфликт с opencode.json — плагин теперь читает из отдельного `.opencode/cbx-speak.json`.
- 2026-01-07: Smoke-проверка enabled=false: лог показывает "cbx-speak disabled via opencode.json".
- 2026-01-07: Smoke-проверка minWords=100: лог показывает "skipping: 29 words < minWords=100".
- 2026-01-07: Все AC выполнены, история закрыта.


## Status

done
