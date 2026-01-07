# Техническое исследование: Интеграция cbx с OpenCode Plugin API

**Дата**: 2026-01-07  
**Статус**: Завершено  
**Автор**: Analyst Agent  

---

## Резюме

Исследованы возможности интеграции CLI-инструмента `cbx` (синтез ответов агентов + TTS) с OpenCode для автоматической озвучки ответов. Рекомендуется использовать **OpenCode Plugin API** с событием `session.idle` для запуска озвучки после завершения ответа агента.

---

## 1. Изученные источники

| Источник | URL | Дата |
|----------|-----|------|
| OpenCode Plugins | https://opencode.ai/docs/plugins/ | 2026-01-06 |
| OpenCode CLI | https://opencode.ai/docs/cli/ | 2026-01-06 |
| OpenCode Commands | https://opencode.ai/docs/commands/ | 2026-01-06 |
| OpenCode MCP Servers | https://opencode.ai/docs/mcp-servers/ | 2026-01-06 |
| OpenCode SDK | https://opencode.ai/docs/sdk/ | 2026-01-06 |
| OpenCode Server API | https://opencode.ai/docs/server/ | 2026-01-06 |
| OpenCode Custom Tools | https://opencode.ai/docs/custom-tools/ | 2026-01-06 |

---

## 2. Точки интеграции OpenCode

### 2.1 Plugin System (Рекомендуется)

**Расположение файлов**:
- Проектные плагины: `.opencode/plugin/`
- Глобальные плагины: `~/.config/opencode/plugin/`

**Поддерживаемые события для озвучки**:

| Событие | Описание | Применимость |
|---------|----------|--------------|
| `session.idle` | Сессия завершила работу | Основной триггер |
| `message.updated` | Обновление сообщения | Для streaming озвучки |
| `message.part.updated` | Обновление части сообщения | Не рекомендуется (частые вызовы) |
| `tool.execute.after` | После выполнения tool | Для специфичных случаев |

**Контекст плагина**:
```typescript
export const Plugin = async ({ project, client, $, directory, worktree }) => {
  return {
    event: async ({ event }) => {
      if (event.type === "session.idle") {
        // Озвучка здесь
      }
    }
  }
}
```

### 2.2 Commands (Slash Commands)

**Расположение**: `.opencode/command/`  
**Формат**: Markdown с frontmatter

**Пример**: `/speak` для ручной озвучки
```markdown
---
description: Озвучить последний ответ
---
!`cbx --text "$ARGUMENTS" --tts`
```

**Ограничение**: Не автоматически, требует явный вызов пользователем.

### 2.3 MCP Server

**Описание**: cbx как внешний tool для LLM.  
**Конфигурация**:
```json
{
  "mcp": {
    "cbx": {
      "type": "local",
      "command": ["cbx", "--text", "...", "--tts"]
    }
  }
}
```

**Ограничение**: LLM должен явно вызвать tool; добавляет tokens в context.

### 2.4 SDK + SSE Events (Внешний демон)

**Описание**: Python-демон слушает SSE события OpenCode Server.
```python
# Концептуально
async for event in sse_client.subscribe():
    if event.type == "session.idle":
        await speak(event.data.last_message)
```

**Ограничение**: Требует отдельного процесса (daemon).

---

## 3. Сравнение вариантов

| Критерий | Plugin (A) | Command (B) | MCP (C) | SSE Daemon (D) |
|----------|------------|-------------|---------|----------------|
| Автоматическая озвучка | Да | Нет | Нет | Да |
| Простота установки | Высокая | Высокая | Средняя | Низкая |
| Нативная интеграция | Да | Да | Да | Нет |
| Требует daemon | Нет | Нет | Нет | Да |
| Python-only | Нет (TS+Python) | Да | Да | Да |
| Context pollution | Нет | Нет | Да | Нет |
| Контроль пользователя | Низкий | Высокий | Средний | Низкий |

---

## 4. Риски и ограничения

### 4.1 Технические риски

| Риск | Вероятность | Митигация |
|------|-------------|-----------|
| Plugin API изменится | Средняя | Fallback на /speak command |
| Bun runtime отсутствует | Низкая | OpenCode устанавливает Bun |
| TTS latency блокирует UX | Низкая | Async execution через daemon thread |
| Python не найден в PATH | Низкая | Использовать venv activation |

### 4.2 Архитектурные ограничения

1. **Язык плагина**: OpenCode плагины — TypeScript/JavaScript, cbx — Python.  
   **Решение**: Plugin вызывает cbx через `Bun.$` shell.

2. **Streaming vs Complete**: Озвучка по частям сложна и нестабильна.  
   **Решение**: Озвучивать только на `session.idle` (полный ответ).

3. **Concurrent responses**: Несколько ответов подряд могут перекрываться.  
   **Решение**: Очередь или skip при активной озвучке.

---

## 5. Рекомендуемая архитектура

```
┌─────────────────────────────────────────────────────────┐
│ OpenCode TUI                                            │
├─────────────────────────────────────────────────────────┤
│ .opencode/plugin/cbx-speak.ts                           │
│                                                         │
│   session.idle event:                                   │
│     1. client.session.messages(sessionID)              │
│     2. Извлечь последний assistant message              │
│     3. Bun.$ `cbx --text "..." --tts`                  │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ cbx CLI (Python)                                        │
│   → synthesis → chatterbox TTS → audio.wav             │
└─────────────────────────────────────────────────────────┘
```

---

## 6. Следующие шаги

### Epic: OpenCode Plugin Integration

| Story | Описание | Story Points |
|-------|----------|--------------|
| OC-1 | Scaffold: создать `.opencode/plugin/cbx-speak.ts` skeleton | 2 |
| OC-2 | Event Handler: реализовать `session.idle` → extract message | 3 |
| OC-3 | Shell Integration: вызов cbx через Bun.$ с обработкой ошибок | 3 |
| OC-4 | Configuration: добавить включение/выключение через opencode.json | 2 |
| OC-5 | Fallback Command: создать `/speak` для ручной озвучки | 2 |
| OC-6 | Documentation: README и инструкция по установке | 1 |

**Итого**: 13 SP (1 спринт)

### Зависимости

- OpenCode >= 1.0
- Bun runtime (устанавливается с OpenCode)
- Python >= 3.11
- cbx установлен в PATH или через `.venv/bin/cbx`

---

## 7. Прототип плагина

```typescript
// .opencode/plugin/cbx-speak.ts
import type { Plugin } from "@opencode-ai/plugin"

export const CbxSpeakPlugin: Plugin = async ({ client, $ }) => {
  return {
    event: async ({ event }) => {
      if (event.type === "session.idle" && event.properties?.sessionID) {
        const sessionID = event.properties.sessionID as string
        
        // Получить сообщения сессии
        const messages = await client.session.messages({ 
          path: { id: sessionID } 
        })
        
        // Найти последний ответ ассистента
        const lastAssistant = messages.data
          ?.filter(m => m.info.role === "assistant")
          .pop()
        
        if (!lastAssistant) return
        
        // Извлечь текст
        const textParts = lastAssistant.parts
          ?.filter(p => p.type === "text")
          .map(p => p.text)
          .join("\n")
        
        if (!textParts) return
        
        // Вызвать cbx
        try {
          await $`cbx --text ${textParts} --tts`
        } catch (error) {
          console.error("[cbx-speak] TTS failed:", error)
        }
      }
    }
  }
}
```

---

## 8. Альтернативная стратегия

Если Plugin API изменится или окажется нестабильным:

1. **Command-only**: `/speak` для ручной озвучки (Вариант B)
2. **Post-hook script**: Внешний watcher на файл `~/.local/share/opencode/sessions/`
3. **Desktop integration**: Отдельное приложение с SSE listener

---

## Заключение

**Рекомендация**: Реализовать интеграцию через OpenCode Plugin API с событием `session.idle`. Это обеспечивает нативную интеграцию, автоматическую озвучку и простоту установки для пользователя.

**Следующий шаг**: Создать Epic "OpenCode Plugin Integration" в backlog и запланировать первый спринт.
