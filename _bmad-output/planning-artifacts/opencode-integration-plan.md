# План интеграции cbx с OpenCode

Дата: 2026-01-07
Статус: Stories созданы, готов к Sprint Planning

## Контекст

MVP cbx (standalone CLI) завершён. Следующий этап — интеграция с OpenCode для автоматической озвучки ответов агентов.

## Результаты исследования

### Рекомендуемый подход: OpenCode Plugin

```
OpenCode → Plugin (TypeScript) → Bun.$ → cbx (Python) → TTS
```

### Почему Plugin?

| Вариант | Вердикт |
|---------|---------|
| **Plugin (session.idle)** | Рекомендуется — нативная интеграция, автоматический запуск |
| Command (/speak) | Запасной — только ручной вызов |
| MCP Server | Не подходит — LLM должен явно вызвать tool |
| SSE Daemon | Сложно — требует отдельный процесс |

### Ключевые решения (Party Mode консенсус)

| Тема | Решение |
|------|---------|
| Подход | OpenCode Plugin + session.idle |
| IPC | Shell (MVP) → Daemon (post-MVP) |
| Фильтрация | Smart filtering (>50 слов, без кода) |
| UX | Hotkey skip, визуальный индикатор, quiet mode |
| Тесты | Integration tests с mock TTS |
| Скорость | MVP за 1 день, затем итерации |

## Epic 4: Интеграция с OpenCode

### Stories

| ID | Описание | SP | Приоритет |
|----|----------|-----|-----------|
| OC-1 | Scaffold плагина cbx-speak.ts | 2 | High |
| OC-2 | Event handler session.idle | 3 | High |
| OC-3 | Shell integration с cbx | 3 | High |
| OC-4 | Конфигурация в opencode.json | 2 | High |
| OC-5 | Fallback /speak command | 2 | Medium |
| OC-6 | Документация | 1 | Medium |
| OC-7 | Smart TTS filtering | 3 | Medium |
| OC-8 | Test coverage for plugin | 2 | Medium |

**Итого: 18 SP (~1.5 спринта)**

## Структура файлов (план)

```
.opencode/
├── plugin/
│   └── cbx-speak.ts      # OpenCode plugin
├── command/
│   └── speak.md          # Fallback /speak command
└── opencode.json         # Plugin configuration
```

## Пример кода плагина (MVP)

```typescript
// .opencode/plugin/cbx-speak.ts
export default {
  name: "cbx-speak",
  events: {
    "session.idle": async (ctx) => {
      const lastMessage = ctx.session.messages.at(-1);
      if (lastMessage?.role === "assistant") {
        await Bun.$`cbx --text ${lastMessage.content} --tts`;
      }
    }
  }
}
```

## Следующие шаги

### После очистки контекста:

1. **Sprint Planning** — `/bmad-bmm-sprint-planning`
   - Выбрать stories для Sprint 4
   - Рекомендуемый scope: Stories 4.1-4.4 (High priority, 10 SP)

2. **Dev Story** — `/bmad-bmm-dev-story`
   - Начать с Story 4.1: Scaffold плагина
   - Создать `~/.config/opencode/plugin/cbx-speak.ts`

3. **Реализация MVP плагина** (Stories 4.1-4.3)
   - 4.1: Базовая структура плагина
   - 4.2: Event handler session.idle
   - 4.3: Shell integration с cbx

4. **Тестирование интеграции**
   - Запустить OpenCode
   - Проверить автоматическую озвучку

5. **Post-MVP** (Stories 4.4-4.8)
   - Конфигурация, /speak command, filtering, docs, tests

### Важные детали для разработки:

- Плагин устанавливается **глобально**: `~/.config/opencode/plugin/cbx-speak.ts`
- Зависимость `@opencode-ai/plugin` уже в `.opencode/package.json`
- cbx должен быть в PATH или указан абсолютный путь
- Stories описаны в `_bmad-output/planning-artifacts/epics.md` (Epic 4)

## Риски

- Plugin API в active development (может измениться)
- TypeScript → Python IPC через shell (латентность 100-200ms)
- Не каждый ответ нужно озвучивать (требуется фильтрация)

## Источники

- OpenCode Plugins: https://opencode.ai/docs/plugins/
- OpenCode CLI: https://opencode.ai/docs/cli/
- Party Mode discussion: 2026-01-07
