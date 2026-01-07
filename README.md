# Chatterbox Lazy OpenCode

CLI-инструмент для синтеза ответов AI-агентов с опциональной TTS-озвучкой.

## Возможности

- **Синтез ответов** — объединение ответов нескольких агентов в структурированный итог
- **Выявление расхождений** — автоматическое определение различий между ответами агентов
- **TTS-озвучка** — преобразование текста в речь через [Chatterbox TTS](https://github.com/resemble-ai/chatterbox)
- **Гибкий экспорт** — сохранение результатов в txt/md с фильтрацией секций
- **Конфигурация** — настройка через TOML/JSON файлы и CLI-флаги

## Установка

**Требования:** Python 3.11+

```bash
# Клонирование репозитория
git clone https://github.com/Nombah501/Chatterbox-lazy-opencode.git
cd Chatterbox-lazy-opencode

# Создание виртуального окружения
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Установка пакета
pip install -e .
```

## Быстрый старт

```bash
# Синтез простого текста
cbx --text "Искусственный интеллект помогает автоматизировать задачи"

# Синтез из JSON с ответами агентов
cbx --input responses.json

# С озвучкой (требуется GPU для оптимальной производительности)
cbx --text "Привет, мир!" --tts --tts-output output.wav
```

## Использование

### Базовые команды

```bash
# Синтез текста
cbx --text "ваш текст"

# Синтез из файла с ответами агентов
cbx --input responses.json

# Экспорт результата
cbx --text "текст" --output result.md
```

### Управление выводом

```bash
# Показать все секции (verbose)
cbx --input responses.json --verbose

# Скрыть расхождения
cbx --input responses.json --no-divergences

# Показать только итог
cbx --input responses.json --no-divergences --no-citations

# Показать цитаты
cbx --input responses.json --show-citations
```

### TTS-озвучка

```bash
# Включить озвучку
cbx --text "текст" --tts

# Выбор модели (turbo или multilingual)
cbx --text "текст" --tts --tts-model multilingual

# Указать устройство
cbx --text "текст" --tts --tts-device cuda

# Клонирование голоса
cbx --text "текст" --tts --tts-voice-prompt voice_sample.wav
```

## Формат входных данных

Файл `responses.json` для `--input`:

```json
[
  {
    "agent_id": "gpt-4",
    "content": "Python — лучший выбор для ML.",
    "citations": [
      {"source": "docs.python.org", "quote": "Python is versatile"}
    ]
  },
  {
    "agent_id": "claude",
    "content": "Рекомендую Python для машинного обучения."
  }
]
```

## Конфигурация

Создайте файл `config.toml`:

```toml
[tts]
enabled = true
engine = "chatterbox"
model = "turbo"           # turbo | multilingual
device = "auto"           # auto | cuda | cpu
voice = "default"
speed = 1.0
```

Использование:

```bash
cbx --config config.toml --text "текст"
```

## Структура проекта

```
src/chatterbox_lazy_opencode/
├── __init__.py
├── cli.py          # CLI интерфейс
├── synthesis.py    # Логика синтеза ответов
├── config.py       # Конфигурация
└── tts/
    └── provider.py # TTS провайдер (Chatterbox)
```

## Разработка

Проект использует [BMAD Method](https://github.com/bmad-code-org/BMAD-METHOD) для управления разработкой.

```bash
# Установка в режиме разработки
pip install -e .

# Запуск CLI
.venv/bin/cbx --help
```

## Лицензия

MIT License. См. файл [LICENSE](LICENSE).

## Авторы

- [@Nombah501](https://github.com/Nombah501)
