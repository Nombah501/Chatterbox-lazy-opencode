```
   ________          __  __            __              
  / ____/ /_  ____ _/ /_/ /____  _____/ /_  ____  _  __
 / /   / __ \/ __ `/ __/ __/ _ \/ ___/ __ \/ __ \| |/_/
/ /___/ / / / /_/ / /_/ /_/  __/ /  / /_/ / /_/ />  <  
\____/_/ /_/\__,_/\__/\__/\___/_/  /_.___/\____/_/|_|  
                                                       
         Lazy OpenCode CLI
```

<p align="center">
  <strong>CLI-инструмент для синтеза ответов AI-агентов с TTS-озвучкой</strong>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
  <img src="https://img.shields.io/badge/python-3.11+-green.svg" alt="Python">
  <img src="https://img.shields.io/badge/version-0.1.0-orange.svg" alt="Version">
  <a href="https://github.com/resemble-ai/chatterbox"><img src="https://img.shields.io/badge/TTS-Chatterbox-purple.svg" alt="Chatterbox"></a>
</p>

---

## Возможности

| Функция | Описание |
|---------|----------|
| **Синтез ответов** | Объединение ответов нескольких агентов в структурированный итог |
| **Выявление расхождений** | Автоматическое определение различий между ответами агентов |
| **TTS-озвучка** | Преобразование текста в речь через Chatterbox (Turbo/Multilingual) |
| **Гибкий экспорт** | Сохранение результатов в txt/md с фильтрацией секций |
| **Конфигурация** | Настройка через TOML/JSON файлы и CLI-флаги |

---

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

---

## Быстрый старт

```bash
# Синтез простого текста
cbx --text "Искусственный интеллект помогает автоматизировать задачи"

# Синтез из JSON с ответами агентов
cbx --input responses.json

# С озвучкой
cbx --text "Привет, мир!" --tts --tts-output output.wav
```

### Пример вывода

```
$ cbx --input responses.json

[status] Сбор: Загружено ответов: 3 [>]
[status] Синтез: Синтез завершен [>]

Итог
Выделяются 3 направления: gpt-4: Python — лучший выбор для ML;
claude: Рекомендую Python для машинного обучения.
При стандартных условиях рекомендуется вариант gpt-4.

Расхождения
gpt-4: Python — лучший выбор для машинного обучения.
claude: Рекомендую Python для машинного обучения.
gemini: Julia быстрее, но Python популярнее.
```

---

## CLI-флаги

### Основные

| Флаг | Описание |
|------|----------|
| `--text TEXT` | Текст для синтеза |
| `--input FILE` | JSON-файл с ответами агентов |
| `--output FILE` | Путь для экспорта результата |
| `--config FILE` | Путь к конфигурации (TOML/JSON) |
| `--verbose` | Показать все секции |

### Управление выводом

| Флаг | Описание |
|------|----------|
| `--show-summary` / `--no-summary` | Показать/скрыть итог |
| `--show-divergences` / `--no-divergences` | Показать/скрыть расхождения |
| `--show-citations` / `--no-citations` | Показать/скрыть цитаты |

### TTS-озвучка

| Флаг | Описание |
|------|----------|
| `--tts` / `--no-tts` | Включить/выключить озвучку |
| `--tts-model MODEL` | Модель: `turbo` (быстрая) или `multilingual` |
| `--tts-device DEVICE` | Устройство: `auto`, `cuda`, `cpu` |
| `--tts-voice-prompt FILE` | WAV-файл для клонирования голоса |
| `--tts-output FILE` | Путь для сохранения аудио |

---

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

---

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

---

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

---

## Разработка

Проект использует [BMAD Method](https://github.com/bmad-code-org/BMAD-METHOD) для управления разработкой.

```bash
# Установка в режиме разработки
pip install -e .

# Запуск CLI
.venv/bin/cbx --help
```

---

## Лицензия

MIT License. См. файл [LICENSE](LICENSE).

---

<p align="center">
  <sub>Made with Python by <a href="https://github.com/Nombah501">@Nombah501</a></sub>
</p>
