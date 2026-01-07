---
stepsCompleted: [1, 2, 3]
inputDocuments:
  - /home/nombah501/VibeCode/Chatterbox lazy opencode/_bmad-output/planning-artifacts/prd-Chatterbox lazy opencode-2026-01-07.md
  - /home/nombah501/VibeCode/Chatterbox lazy opencode/_bmad-output/planning-artifacts/product-brief-Chatterbox lazy opencode-2026-01-07.md
  - /home/nombah501/VibeCode/Chatterbox lazy opencode/_bmad-output/planning-artifacts/ux-design-specification.md
  - /home/nombah501/VibeCode/Chatterbox lazy opencode/_bmad-output/analysis/research-2026-01-07.md
  - /home/nombah501/VibeCode/Chatterbox lazy opencode/_bmad-output/analysis/brainstorming-session-2026-01-07.md
workflowType: 'architecture'
project_name: 'Chatterbox lazy opencode'
user_name: 'Nombah501'
date: '2026-01-07'
---

# Architecture Decision Document

_This document builds collaboratively through step-by-step discovery. Sections are appended as we work through each architectural decision together._

## Project Context Analysis

### Requirements Overview

**Functional Requirements:**
- Синтез нескольких ответов ИИ-агентов в структуру «итог + расхождения + цитаты».
- Опциональная озвучка итога через TTS, без влияния на текстовый поток.
- Настройки: голос/скорость, уровень детализации, режимы вывода.
- Экспорт результата в файл (txt/md).
- Автоматическое отключение TTS в CI/неинтерактивных окружениях.
- Показ статусов обработки (сбор, синтез, цитаты, озвучка).

**Non-Functional Requirements:**
- Латентность озвучки - секунды, не минуты.
- Надежность: сбой TTS не ломает текстовый вывод.
- CPU-first, GPU опционально.
- Приватность: локальная обработка по умолчанию.
- UX-стабильность: не мешать основному потоку OpenCode.

**Scale & Complexity:**
- Primary domain: CLI/плагин + локальный TTS-слой
- Complexity level: medium
- Estimated architectural components: 6-8

### Technical Constraints & Dependencies

- Платформа: Linux (Manjaro KDE) - приоритет.
- Лицензии: избегать GPL/AGPL; предпочитать MIT/Apache/BSD.
- Интеграция: OpenCode plugin API.
- Зависимости: OpenCode CLI, локальный TTS-движок, системные аудио-плееры.

### Cross-Cutting Concerns Identified

- Конфигурируемость и режимы вывода (кратко/подробно).
- Fallback-поведение при сбоях TTS.
- Прозрачность синтеза через цитаты/источники.
- Детект окружения (CI/неинтерактив/SSH).
- Производительность и ресурсные ограничения CPU.

## Architecture Summary

Целевая архитектура разделяет пользовательский CLI/плагин (Node.js/TypeScript) и TTS‑воркер (Python + Chatterbox) для устойчивости, изоляции зависимостей и минимального влияния на UX OpenCode. CLI отвечает за синтез и форматирование вывода, TTS‑воркер — за генерацию аудио по запросу.

## High-Level Components

1) **OpenCode Plugin Adapter**
- Подключение к OpenCode plugin API
- Перехват событий/сообщений для сборки ответов

2) **CLI Core (Node.js/TypeScript)**
- Команды: synthesize, speak, export, config
- Управление режимами вывода и флагами

3) **Synthesis Engine**
- Сбор ответов агентов
- Формирование «итог + расхождения + цитаты»

4) **Output Renderer**
- Структурированный вывод секций
- Режимы: кратко/подробно

5) **TTS Controller**
- Решение когда и что озвучивать
- Fallback при ошибках TTS

6) **TTS Worker (Python + Chatterbox)**
- Локальный сервис генерации аудио
- Интерфейс: HTTP или Unix socket

7) **Config Store**
- Локальный конфиг (yaml/json)
- Значения по умолчанию

8) **Exporter**
- Выгрузка результата в txt/md

## Data Flow

1) OpenCode Plugin Adapter принимает ответы агентов.
2) Synthesis Engine формирует итог, расхождения и цитаты.
3) Output Renderer печатает структурированный вывод.
4) TTS Controller инициирует озвучку итога (если включено).
5) TTS Worker возвращает аудио, CLI запускает воспроизведение.
6) Exporter сохраняет результат при наличии флага.

## Integration Points

- OpenCode plugin API: onPostMessage / onPostToolCall (или эквиваленты для получения финальных ответов).
- Локальный TTS‑воркер: HTTP/Unix socket (stdout‑fallback для простоты в MVP).
- Системные аудио‑плееры Linux: paplay/aplay/mpv (детект доступных).

## Configuration

- Файл конфигурации: локальный (например, `.opencode/chatterbox.json`).
- Дефолты: TTS выключен, краткий вывод, экспорт markdown.
- Параметры: голос, скорость, режимы вывода, авто‑отключение в CI/неинтерактиве.

## Error Handling & Fallbacks

- Ошибка TTS не влияет на текстовый вывод.
- Недоступный воркер: отключить TTS и вывести предупреждение.
- Таймауты синтеза: показать краткий итог или сырой текст.

## Deployment & Packaging

- CLI/плагин: npm‑пакет (Node.js/TypeScript).
- Установщик TTS: скрипт, настраивающий Python окружение и модели Chatterbox.
- Обновления: через npm.

## Security & Privacy

- Локальная обработка TTS по умолчанию.
- Отсутствие внешних сервисов в MVP.

## Observability

- Минимальные логи в CLI с флагом `--verbose`.
- Явные статусы этапов (синтез/озвучка/экспорт).

## Architecture Decisions (Summary)

- **CLI/плагин**: Node.js + TypeScript.
- **CLI framework**: commander.
- **TTS**: отдельный Python‑воркер (Chatterbox) через HTTP/Unix socket.
- **Packaging**: npm‑пакет + installer‑script для Python‑зависимостей.
- **External services**: отсутствуют в MVP.
