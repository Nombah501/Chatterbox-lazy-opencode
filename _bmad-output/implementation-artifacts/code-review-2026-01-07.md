# Code Review (BMAD)

Дата: 2026-01-07
Область: CLI, TTS-адаптер, синтез

## Критические
- `src/chatterbox_lazy_opencode/cli.py`: ошибки TTS не перехватываются, CLI падает.
- `src/chatterbox_lazy_opencode/tts/provider.py`: исключения при загрузке/скачивании/записи не обработаны, нет fallback.

## Высокие
- `src/chatterbox_lazy_opencode/tts/provider.py`: `HF_TOKEN` через `setdefault` может игнорировать токен из CLI.
- `src/chatterbox_lazy_opencode/cli.py`: синхронный TTS блокирует завершение команды.

## Средние
- `src/chatterbox_lazy_opencode/tts/provider.py`: `voice`, `speed`, `tags_enabled` не используются.
- `src/chatterbox_lazy_opencode/synthesis.py`: итог = первый ответ без реального синтеза.

## Низкие
- `src/chatterbox_lazy_opencode/cli.py`: озвучивается весь итоговый вывод, что может быть не тем, что ожидается.

## Рекомендации (в рамках следующих историй)
- Добавить try/except вокруг TTS и не блокировать CLI.
- Уточнить правила синтеза и расхождений.
- Поддержать параметры `voice/speed/tags` в адаптере.
