# Sprint 4 Backlog: Интеграция с OpenCode

**Дата:** 2026-01-07
**Sprint Goal:** Создать работающий OpenCode плагин для автоматической озвучки ответов агентов через cbx CLI.

## Sprint Scope

| Story | Название | SP | Приоритет | Status |
|-------|----------|-----|-----------|--------|
| 4.1 | Scaffold плагина cbx-speak.ts | 2 | High | backlog |
| 4.2 | Event handler session.idle | 3 | High | backlog |
| 4.3 | Shell integration с cbx | 3 | High | backlog |
| 4.4 | Конфигурация в opencode.json | 2 | High | backlog |

**Итого: 4 stories, 10 SP**

## Sprint Goal

> Пользователь OpenCode получает автоматическую озвучку ответов агентов после их завершения, плагин работает глобально в любом проекте.

## Definition of Done

- [ ] Плагин `~/.config/opencode/plugin/cbx-speak.ts` создан
- [ ] Плагин загружается OpenCode без ошибок
- [ ] В логах видно "cbx-speak initialized"
- [ ] Событие session.idle запускает обработчик
- [ ] Последний assistant message извлекается из сессии
- [ ] cbx вызывается через shell с флагом --tts
- [ ] Ошибки cbx логируются, но не ломают OpenCode
- [ ] Конфигурация enabled/disabled работает
- [ ] Параметры cbxPath и minWords читаются из конфига

## Технические решения

### Архитектура
```
OpenCode → Plugin (TypeScript) → Bun.$ → cbx (Python) → TTS
```

### Ключевые файлы
- `~/.config/opencode/plugin/cbx-speak.ts` — основной плагин
- `~/.config/opencode/opencode.json` — конфигурация
- `.opencode/package.json` — зависимость @opencode-ai/plugin

### Зависимости
- cbx должен быть в PATH или указан абсолютный путь
- @opencode-ai/plugin уже в .opencode/package.json

## Stories

### Story 4.1: Scaffold плагина cbx-speak.ts (2 SP)

**Цель:** Создать базовую структуру плагина для OpenCode

**Acceptance Criteria:**
- Given глобальная директория `~/.config/opencode/plugin/`
- When я создаю файл `cbx-speak.ts`
- Then плагин экспортирует Plugin функцию с правильной сигнатурой
- And плагин загружается OpenCode без ошибок
- And в логах видно "cbx-speak initialized"

**Технические задачи:**
1. Создать директорию ~/.config/opencode/plugin/ если не существует
2. Создать cbx-speak.ts с экспортом Plugin
3. Добавить инициализационное логирование
4. Проверить загрузку плагина

---

### Story 4.2: Event handler session.idle (3 SP)

**Цель:** Обработка события завершения ответа агента

**Acceptance Criteria:**
- Given плагин установлен и OpenCode запущен
- When агент завершает ответ (session.idle)
- Then плагин получает событие с sessionId
- And плагин извлекает последний assistant message из сессии
- And текстовые части сообщения объединяются для озвучки

**Технические задачи:**
1. Подписаться на событие session.idle
2. Получить sessionId из события
3. Вызвать client.session.messages() для получения истории
4. Найти последний message с role: "assistant"
5. Извлечь текстовые части (content.type === "text")

---

### Story 4.3: Shell integration с cbx (3 SP)

**Цель:** Вызов cbx для озвучки текста

**Acceptance Criteria:**
- Given текст ответа извлечён
- When плагин вызывает `cbx --text "..." --tts`
- Then cbx озвучивает текст
- And ошибки cbx логируются, но не ломают OpenCode
- And поддерживается абсолютный путь к cbx

**Технические задачи:**
1. Использовать Bun.$ для вызова cbx
2. Передать текст через --text параметр
3. Добавить --tts флаг
4. Обернуть в try/catch для graceful degradation
5. Логировать ошибки через console.error

---

### Story 4.4: Конфигурация в opencode.json (2 SP)

**Цель:** Управление плагином через конфигурацию

**Acceptance Criteria:**
- Given opencode.json с секцией cbx-speak
- When enabled: false
- Then плагин не запускает озвучку
- And поддерживаются параметры: enabled, cbxPath, minWords

**Технические задачи:**
1. Определить интерфейс конфигурации CbxSpeakConfig
2. Читать конфигурацию при инициализации
3. Проверять enabled перед озвучкой
4. Использовать cbxPath для пути к исполняемому файлу
5. Использовать minWords для минимальной длины текста

---

## Риски и митигации

| Риск | Вероятность | Митигация |
|------|-------------|-----------|
| Plugin API может измениться | Средняя | Следить за документацией OpenCode |
| Латентность IPC 100-200ms | Низкая | Приемлемо для MVP |
| cbx не в PATH | Средняя | Поддержка абсолютного пути через cbxPath |

## Порядок реализации

1. **Story 4.1** — базовая структура (блокирует остальные)
2. **Story 4.2** — event handler (зависит от 4.1)
3. **Story 4.3** — shell integration (зависит от 4.2)
4. **Story 4.4** — конфигурация (может быть параллельно с 4.3)

## Следующие шаги

1. Запустить `/bmad-bmm-dev-story` для Story 4.1
2. Создать файл истории 4-1-scaffold-plagina-cbx-speak-ts.md
3. Реализовать базовую структуру плагина
4. Тестировать загрузку в OpenCode

---

*Сгенерировано Sprint Planning 2026-01-07*
