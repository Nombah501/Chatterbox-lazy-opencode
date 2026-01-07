---
stepsCompleted: [1, 2, 3, 4]
inputDocuments:
  - /home/nombah501/VibeCode/Chatterbox lazy opencode/_bmad-output/planning-artifacts/architecture.md
  - /home/nombah501/VibeCode/Chatterbox lazy opencode/_bmad-output/planning-artifacts/ux-design-specification.md
  - /home/nombah501/VibeCode/Chatterbox lazy opencode/_bmad-output/planning-artifacts/prd-Chatterbox lazy opencode-2026-01-07.md
  - /home/nombah501/VibeCode/Chatterbox lazy opencode/_bmad-output/planning-artifacts/product-brief-Chatterbox lazy opencode-2026-01-07.md
  - /home/nombah501/VibeCode/Chatterbox lazy opencode/_bmad-output/analysis/research-2026-01-07.md
  - /home/nombah501/VibeCode/Chatterbox lazy opencode/_bmad-output/analysis/brainstorming-session-2026-01-07.md
  - /home/nombah501/VibeCode/Chatterbox lazy opencode/_bmad-output/planning-artifacts/opencode-integration-plan.md
  - /home/nombah501/VibeCode/Chatterbox lazy opencode/_bmad-output/planning-artifacts/research-opencode-plugin-integration.md
---

# Chatterbox lazy opencode - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for Chatterbox lazy opencode, decomposing the requirements from the PRD, UX Design if it exists, and Architecture requirements into implementable stories.

## Requirements Inventory

### Functional Requirements

FR1: Включение/выключение TTS в CLI.
FR2: Синтез «итог + расхождения» с цитатами.
FR3: Выбор голоса и скорости.
FR4: Озвучка итогов/завершений задач.
FR5: Экспорт результатов в файл.
FR6: Авто-отключение TTS в CI/неинтерактивных режимах.
FR7: Автоматическая озвучка ответов OpenCode при событии session.idle.
FR8: Извлечение текста последнего assistant message из сессии.
FR9: Вызов cbx CLI из TypeScript плагина через shell.
FR10: Конфигурация плагина в opencode.json (включение/выключение).
FR11: Fallback /speak команда для ручной озвучки.
FR12: Фильтрация коротких или технических ответов (smart filtering).

### NonFunctional Requirements

NFR1: Латентность озвучки: секунды, не минуты.
NFR2: Надежность: при сбое TTS текстовый вывод не ломается.
NFR3: Ресурсы: работа на CPU обязательна, GPU опционально.
NFR4: Приватность: локальная обработка TTS по умолчанию.
NFR5: UX-стабильность: не мешать основному потоку OpenCode.
NFR6: Латентность IPC (TypeScript→Python): <200ms overhead.
NFR7: Плагин не должен блокировать UX OpenCode.
NFR8: Совместимость с глобальной установкой (~/.config/opencode/plugin/).

### Additional Requirements

- Платформа приоритетно Linux (Manjaro KDE).
- Лицензии зависимостей: избегать GPL/AGPL, предпочитать MIT/Apache/BSD.
- Интеграция через OpenCode plugin API.
- CLI/плагин на Node.js/TypeScript; CLI framework: commander.
- TTS-воркер на Python + Chatterbox, связь через HTTP/Unix socket или stdout fallback.
- Формат вывода по умолчанию: Итог → Расхождения → Цитаты/источники.
- Режимы вывода: кратко/подробно; флаги для секций или интерактивный выбор.
- Статусы обработки: сбор, синтез, формирование цитат, озвучка.
- UX ошибок: при недоступном TTS продолжать без озвучки и показывать предупреждение.
- Таймаут синтеза: частичный результат и предложение повторить.
- Хранение/показ цитат-источников для прозрачности синтеза.
- Экспорт в файл (txt/md) с сообщением пути.
- Авто-детект CI/неинтерактив/SSH для отключения TTS.
- Конфиг локально (например, `.opencode/chatterbox.json`), дефолты: TTS off, кратко, экспорт markdown.
- Плееры Linux: детект доступных (paplay/aplay/mpv).
- Пакетирование: npm-пакет + installer-скрипт для Python-зависимостей.
- В MVP нет внешних сервисов.
- Минимальный core, функционально близкий к AgentVibes, но для OpenCode.
- Плагин на TypeScript с @opencode-ai/plugin.
- Использовать событие session.idle как основной триггер.
- Доступ к сообщениям через client.session.messages().
- Shell integration через Bun.$ для вызова cbx.
- Очередь или skip при активной озвучке (concurrent responses).
- Глобальная установка плагина для работы в любом проекте.
- cbx должен быть доступен в PATH или через абсолютный путь.
- Документация по установке и конфигурации.

### FR Coverage Map

FR1: Epic 2 — управление TTS
FR2: Epic 1 — синтез итог/расхождения/цитаты
FR3: Epic 2 — настройка голоса/скорости
FR4: Epic 2 — озвучка итогов/завершений
FR5: Epic 3 — экспорт результатов
FR6: Epic 2 — авто-отключение TTS в CI/неинтерактиве
FR7: Epic 4 — автоматическая озвучка через session.idle
FR8: Epic 4 — извлечение assistant message
FR9: Epic 4 — shell integration cbx
FR10: Epic 4 — конфигурация плагина
FR11: Epic 4 — fallback /speak команда
FR12: Epic 4 — smart filtering

## Epic List

1) Прозрачный синтез результатов
2) Озвучка и управление TTS
3) Сохранение и обмен результатами
4) Интеграция с OpenCode

## Epic 1: Прозрачный синтез результатов

Пользователь получает структурированный вывод «Итог → Расхождения → Цитаты» и понимает, откуда взялся синтез.

### Story 1.1: Синтез итогов и расхождений

As a соло-разработчик,
I want получать итог и расхождения по ответам агентов,
So that я быстро понимаю лучший путь без чтения всего текста.

**Acceptance Criteria:**

**Given** есть несколько ответов агентов
**When** я запускаю команду синтеза
**Then** вывод содержит секции Итог и Расхождения
**And** итог краткий по умолчанию

### Story 1.2: Прозрачные цитаты-источники

As a power user,
I want видеть цитаты-источники под секцией расхождений,
So that я могу проверить корректность синтеза.

**Acceptance Criteria:**

**Given** синтез выполнен
**When** я запрашиваю вывод с цитатами
**Then** отображаются цитаты с указанием источника
**And** если цитат нет, показывается пустая секция

### Story 1.3: Управление уровнем детализации вывода

As a соло-разработчик,
I want управлять кратким/подробным режимом вывода,
So that я вижу только нужный объем информации.

**Acceptance Criteria:**

**Given** команда синтеза
**When** я использую флаги отображения секций
**Then** вывод содержит только выбранные секции
**And** по умолчанию включен краткий режим

### Story 1.4: Статусы обработки

As a пользователь CLI,
I want видеть статусы обработки (сбор, синтез, цитаты),
So that я понимаю текущий этап работы.

**Acceptance Criteria:**

**Given** синтез запущен
**When** выполняется обработка
**Then** выводит краткие статусы этапов
**And** статусы не блокируют основной вывод

## Epic 2: Озвучка и управление TTS

Пользователь включает/выключает озвучку, настраивает голос и получает аудио‑итог без риска сломать текстовый поток.

### Story 2.1: Включение и выключение TTS

As a соло-разработчик,
I want включать и выключать TTS,
So that я сам решаю, когда мне нужен аудио-слой.

**Acceptance Criteria:**

**Given** установлен CLI
**When** я включаю TTS в конфиге или командой
**Then** итоговые ответы озвучиваются
**And** при отключении озвучка не запускается

### Story 2.2: Выбор голоса и скорости

As a пользователь,
I want выбрать голос и скорость речи,
So that озвучка звучит комфортно.

**Acceptance Criteria:**

**Given** TTS включен
**When** я задаю голос и скорость
**Then** озвучка использует выбранные параметры
**And** значения сохраняются в конфиге

### Story 2.3: Озвучка итогов с fallback

As a пользователь CLI,
I want чтобы озвучка итогов не ломала текстовый вывод,
So that я всегда вижу результат даже при ошибке TTS.

**Acceptance Criteria:**

**Given** итог сформирован
**When** TTS воркер недоступен или упал
**Then** текстовый вывод остаётся полным
**And** показывается предупреждение о сбое TTS

### Story 2.4: Авто-отключение в CI/неинтерактиве

As a пользователь,
I want чтобы TTS автоматически отключался в CI/неинтерактиве,
So that озвучка не мешает автоматизированным сценариям.

**Acceptance Criteria:**

**Given** запуск в CI или неинтерактивной среде
**When** выполняется синтез
**Then** озвучка не запускается
**And** сохраняется текстовый вывод

## Epic 3: Сохранение и обмен результатами

Пользователь сохраняет итог в файл, чтобы возвращаться к нему или делиться с другими.

### Story 3.1: Экспорт результата в файл

As a мейнтейнер,
I want экспортировать результат в файл,
So that я могу поделиться итогом с командой.

**Acceptance Criteria:**

**Given** синтез выполнен
**When** я запускаю экспорт
**Then** создается файл в формате txt или md
**And** CLI выводит путь к файлу

### Story 3.2: Экспорт с выбранными секциями

As a пользователь,
I want экспортировать только нужные секции,
So that файл содержит ровно то, что мне нужно.

**Acceptance Criteria:**

**Given** синтез выполнен
**When** я указываю флаги секций при экспорте
**Then** файл содержит только выбранные секции
**And** форматирование сохраняет порядок Итог → Расхождения → Цитаты

## Epic 4: Интеграция с OpenCode

Пользователь получает автоматическую озвучку ответов OpenCode без ручных действий, плагин работает глобально в любом проекте.

**FRs covered:** FR7, FR8, FR9, FR10, FR11, FR12

### Story 4.1: Scaffold плагина cbx-speak.ts

As a разработчик,
I want иметь базовую структуру плагина для OpenCode,
So that я могу расширять его функциональность.

**Acceptance Criteria:**

**Given** глобальная директория `~/.config/opencode/plugin/`
**When** я создаю файл `cbx-speak.ts`
**Then** плагин экспортирует Plugin функцию с правильной сигнатурой
**And** плагин загружается OpenCode без ошибок
**And** в логах видно "cbx-speak initialized"

### Story 4.2: Event handler session.idle

As a пользователь OpenCode,
I want чтобы плагин реагировал на завершение ответа агента,
So that озвучка запускалась автоматически.

**Acceptance Criteria:**

**Given** плагин установлен и OpenCode запущен
**When** агент завершает ответ (session.idle)
**Then** плагин получает событие с sessionId
**And** плагин извлекает последний assistant message из сессии
**And** текстовые части сообщения объединяются для озвучки

### Story 4.3: Shell integration с cbx

As a пользователь OpenCode,
I want чтобы плагин вызывал cbx для озвучки,
So that я слышал ответы агентов.

**Acceptance Criteria:**

**Given** текст ответа извлечён
**When** плагин вызывает `cbx --text "..." --tts`
**Then** cbx озвучивает текст
**And** ошибки cbx логируются, но не ломают OpenCode
**And** поддерживается абсолютный путь к cbx

### Story 4.4: Конфигурация в opencode.json

As a пользователь,
I want управлять плагином через конфигурацию,
So that я могу включать/выключать озвучку.

**Acceptance Criteria:**

**Given** opencode.json с секцией cbx-speak
**When** enabled: false
**Then** плагин не запускает озвучку
**And** поддерживаются параметры: enabled, cbxPath, minWords

### Story 4.5: Fallback /speak command

As a пользователь OpenCode,
I want ручную команду для озвучки,
So that я могу озвучить текст когда автоматика отключена.

**Acceptance Criteria:**

**Given** файл `.opencode/command/speak.md`
**When** я вызываю `/speak текст`
**Then** cbx озвучивает указанный текст
**And** команда работает независимо от настройки enabled

### Story 4.6: Smart TTS filtering

As a пользователь OpenCode,
I want чтобы короткие и технические ответы не озвучивались,
So that озвучка не мешала работе.

**Acceptance Criteria:**

**Given** ответ агента получен
**When** текст короче minWords (default: 50)
**Then** озвучка не запускается
**And** ответы с большим количеством кода (>50%) не озвучиваются
**And** tool calls не озвучиваются

### Story 4.7: Документация и установка

As a пользователь,
I want понятную инструкцию по установке плагина,
So that я могу настроить озвучку за 5 минут.

**Acceptance Criteria:**

**Given** README в репозитории
**When** пользователь следует инструкции
**Then** плагин устанавливается глобально
**And** документация включает: требования, установку, конфигурацию, troubleshooting

### Story 4.8: Test coverage for plugin

As a разработчик,
I want тесты для плагина,
So that изменения не ломают функциональность.

**Acceptance Criteria:**

**Given** тестовый фреймворк настроен
**When** запускаются тесты
**Then** покрыты: event handler, text extraction, filtering, shell call
**And** используется mock для cbx
