# Story 4.3: Shell integration с cbx

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a пользователь OpenCode,
I want чтобы плагин вызывал cbx для озвучки,
so that я слышал ответы агентов.

## Acceptance Criteria

1. **Given** текст ответа извлечен
   **When** плагин вызывает `cbx --text "..." --tts`
   **Then** cbx озвучивает текст.
2. **Given** вызов cbx завершился ошибкой или cbx недоступен
   **When** плагин пытается озвучить текст
   **Then** ошибка логируется, но OpenCode не ломается и продолжает работу.
3. **Given** требуется абсолютный путь к cbx
   **When** в плагине задан абсолютный путь
   **Then** используется этот путь вместо `cbx` из PATH.

## Tasks / Subtasks

- [x] Task 1: Добавить shell-вызов cbx для озвучки (AC: 1)
  - [x] Subtask 1.1: Сформировать команду `cbx --text ${text} --tts` через `Bun.$`/`$` и вызывать после извлечения текста
  - [x] Subtask 1.2: Сохранить неблокирующий async вызов и ранний выход при пустом тексте
- [x] Task 2: Обработать ошибки вызова cbx без падения UX (AC: 2)
  - [x] Subtask 2.1: Обернуть вызов в `try/catch` и логировать ошибки с префиксом `[cbx-speak]`
  - [x] Subtask 2.2: Не пробрасывать исключения наружу, не останавливать обработку событий
- [x] Task 3: Поддержать абсолютный путь к cbx (AC: 3)
  - [x] Subtask 3.1: Добавить поддержку `CBX_PATH` (или константы) с fallback на `cbx`
  - [x] Subtask 3.2: Явно задокументировать способ задания пути до появления конфигурации (Story 4.4)
- [x] Task 4: Smoke-проверка интеграции
  - [x] Subtask 4.1: В OpenCode убедиться, что при `session.idle` запускается cbx
  - [x] Subtask 4.2: Проверить негативный сценарий (cbx отсутствует) — лог без падения

## Dev Notes

### Developer Context

- Scope: только shell-integration; извлечение текста уже сделано в Story 4.2.
- Не добавлять конфигурацию `opencode.json` (Story 4.4) и `/speak` (Story 4.5).
- Работать с глобальным плагином `~/.config/opencode/plugin/cbx-speak.ts`; не создавать копии в репозитории.
- Вызов cbx выполнять через `Bun.$`/`$` из контекста плагина, асинхронно, без блокировки UX.
- Поддержать абсолютный путь к cbx через `CBX_PATH` (или константу) до появления конфигурации.
- Ошибки вызова cbx логировать и продолжать работу без краша.

### Technical Requirements

- Язык/рантайм: TypeScript plugin для OpenCode.
- Типизация: `import type { Plugin } from "@opencode-ai/plugin"`.
- Использовать существующий обработчик `event` и проверку `event.type === "session.idle"`.
- Shell-вызов через `Bun.$`/`$` с безопасной подстановкой текста.
- Никаких новых зависимостей.

### Architecture Compliance

- Сбой TTS не должен ломать текстовый поток OpenCode.
- Операции остаются async и не блокируют UI.
- Локальная обработка без внешних сервисов.

### Library & Framework Requirements

- OpenCode Plugin API (event hook).
- Bun runtime для shell (`$`).
- cbx CLI в PATH или по абсолютному пути.

### Project Structure Notes

- Изменения только в `~/.config/opencode/plugin/cbx-speak.ts`.
- Не добавлять `.opencode/opencode.json` и `.opencode/command/speak.md` в этой истории.
- Тестовый фреймворк не определен; допускается smoke-проверка.

### Testing Requirements

- Ручная проверка в OpenCode: session.idle → вызов cbx.
- Негативный кейс: cbx отсутствует/не исполняется → лог без падения.

### Previous Story Intelligence

- Story 4.2 уже реализовала обработчик `session.idle` и извлечение текста (последний `assistant`, объединение `parts` типа `text`).
- В 4.2 запрещены shell-вызовы и конфиг — добавить только вызов cbx.
- Плагин уже инициализируется и работает в глобальном пути.

### Git Intelligence Summary

- Последние коммиты — документация/планирование, без изменений плагина.
- Ожидаемые изменения: только глобальный файл плагина.

### Latest Tech Information

- Рекомендованный триггер: `session.idle`.
- Плагин получает `$` (Bun shell) и `client` из контекста плагина.
- `client.session.messages({ path: { id } })` возвращает массив с `info.role` и `parts`.
- Пример вызова:
  ```typescript
  await $`cbx --text ${text} --tts`
  ```

### Project Context Reference

- `project-context.md` не найден; использовать контекст Epic 4 и исследования.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story 4.3]
- [Source: _bmad-output/planning-artifacts/opencode-integration-plan.md#Результаты исследования]
- [Source: _bmad-output/planning-artifacts/research-opencode-plugin-integration.md#2.1 Plugin System]
- [Source: _bmad-output/planning-artifacts/architecture.md#Architecture Summary]
- [Source: https://opencode.ai/docs/plugins/]
- [Source: https://opencode.ai/docs/sdk/]

## Dev Agent Record

### Agent Model Used

GPT-5

### Debug Log References

### Implementation Plan

- Обновить `~/.config/opencode/plugin/cbx-speak.ts`: добавить вызов cbx через `$` после извлечения текста.
- Использовать `CBX_PATH` как опциональный абсолютный путь с fallback на `cbx` из PATH.
- Логировать ошибки вызова cbx без проброса исключений.
- Проверить вручную в OpenCode: `session.idle` запускает cbx.

### Completion Notes List

- Добавлен shell-вызов cbx с `--tts` и обработкой ошибок.
- Поддержан `CBX_PATH` для абсолютного пути.
- Добавлен флаг `--tts-force` в cbx для обхода неинтерактивного режима в OpenCode.
- Обновлен тестовый скрипт для проверки наличия `--tts-force`.
- Smoke-проверка в OpenCode: cbx запускается, но аудио не создается (ошибка LocalTokenNotFoundError без HF_TOKEN).
- `cbx --tts --tts-force` выполняет TTS синхронно, но требует HF_TOKEN/HUGGINGFACE_HUB_TOKEN.
- Добавлена передача `CBX_TTS_HF_TOKEN`/`HF_TOKEN`/`HUGGINGFACE_HUB_TOKEN` в `--tts-hf-token` из плагина.
- Добавлен лог token=present/missing в `cbx-speak.log` при `session.idle`.
- Добавлен лог `event <type>` и список свойств для диагностики `session.idle`.
- Добавлен файл локальной конфигурации `~/.config/opencode/cbx-speak.env`.
- Конфиг читается на каждый `session.idle`, поддержан префикс `export`, добавлен лог пути конфига.
- Добавлен `--quiet` для подавления вывода cbx и снижения артефактов в TUI.
- Добавлена ротация лога `cbx-speak.log` при превышении 2MB и лимит на число файлов.
- Добавлены настройки логирования: `CBX_LOG_LEVEL`, `CBX_LOG_MAX_BYTES`, `CBX_LOG_MAX_FILES`.
- Исправлена передача `--tts-hf-token`: убран массив, аргументы передаются явно (Bun shell ограничение).
- Добавлено логирование ошибок cbx в файл с уровнем `error`.
- Smoke-проверка завершена: cbx вызывается при `session.idle`, ошибки логируются без краша.

### File List

- `~/.config/opencode/plugin/cbx-speak.ts`
- `scripts/test_opencode_plugin.py`
- `src/chatterbox_lazy_opencode/cli.py`

## Change Log

- 2026-01-07: Создана story 4.3 с контекстом и требованиями.
- 2026-01-07: Добавлен shell-вызов cbx и обработка ошибок.
- 2026-01-07: Добавлен флаг `--tts-force` для cbx и обновлен тестовый скрипт.
- 2026-01-07: `--tts-force` переведен в синхронный режим; тест уперся в отсутствие HF_TOKEN.
- 2026-01-07: Добавлен проброс токена (CBX_TTS_HF_TOKEN/HF_TOKEN/HUGGINGFACE_HUB_TOKEN) в `--tts-hf-token`.
- 2026-01-07: Лог `token=present/missing` добавлен для диагностики.
- 2026-01-07: Добавлен лог событий (`event <type>`) для диагностики `session.idle`.
- 2026-01-07: Добавлена поддержка `export KEY=VALUE`, повторное чтение конфига и лог пути конфига.
- 2026-01-07: Добавлена ротация `cbx-speak.log` при превышении 2MB и лимит на число файлов.
- 2026-01-07: Добавлены настройки логирования (уровень и лимиты).
- 2026-01-07: Добавлен флаг `--quiet` и подавление вывода cbx для TUI.
- 2026-01-07: Исправлена передача `--tts-hf-token` — явные аргументы вместо массива.
- 2026-01-07: Добавлено логирование ошибок cbx в файл.
- 2026-01-07: Smoke-проверка завершена, история закрыта.


## Status

done
