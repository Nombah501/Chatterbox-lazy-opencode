---
stepsCompleted: [1]
inputDocuments:
  - /home/nombah501/VibeCode/Chatterbox lazy opencode/_bmad-output/planning-artifacts/architecture.md
  - /home/nombah501/VibeCode/Chatterbox lazy opencode/_bmad-output/planning-artifacts/ux-design-specification.md
  - /home/nombah501/VibeCode/Chatterbox lazy opencode/_bmad-output/planning-artifacts/prd-Chatterbox lazy opencode-2026-01-07.md
  - /home/nombah501/VibeCode/Chatterbox lazy opencode/_bmad-output/planning-artifacts/product-brief-Chatterbox lazy opencode-2026-01-07.md
  - /home/nombah501/VibeCode/Chatterbox lazy opencode/_bmad-output/analysis/research-2026-01-07.md
  - /home/nombah501/VibeCode/Chatterbox lazy opencode/_bmad-output/analysis/brainstorming-session-2026-01-07.md
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

### NonFunctional Requirements

NFR1: Латентность озвучки: секунды, не минуты.
NFR2: Надежность: при сбое TTS текстовый вывод не ломается.
NFR3: Ресурсы: работа на CPU обязательна, GPU опционально.
NFR4: Приватность: локальная обработка TTS по умолчанию.
NFR5: UX-стабильность: не мешать основному потоку OpenCode.

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

### FR Coverage Map

FR1: Epic 2 — управление TTS
FR2: Epic 1 — синтез итог/расхождения/цитаты
FR3: Epic 2 — настройка голоса/скорости
FR4: Epic 2 — озвучка итогов/завершений
FR5: Epic 3 — экспорт результатов
FR6: Epic 2 — авто-отключение TTS в CI/неинтерактиве

## Epic List

1) Прозрачный синтез результатов
2) Озвучка и управление TTS
3) Сохранение и обмен результатами

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
