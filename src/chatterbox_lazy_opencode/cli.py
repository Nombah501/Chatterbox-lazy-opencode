from __future__ import annotations

import argparse
import json
import os
import sys
import threading
from pathlib import Path

from chatterbox_lazy_opencode.config import AppConfig, apply_overrides, load_config
from chatterbox_lazy_opencode.synthesis import AgentResponse, synthesize
from chatterbox_lazy_opencode.tts.provider import ChatterboxProvider


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Синтез ответов агентов с опциональной озвучкой"
    )
    parser.add_argument("--config", help="Путь к конфигу (toml или json)")
    parser.add_argument("--text", help="Текст для озвучки и синтеза")
    parser.add_argument("--input", help="Путь к JSON с ответами агентов")
    parser.add_argument("--agent-id", default="agent-1")
    parser.add_argument("--include-citations", action="store_true")

    parser.add_argument("--show-summary", dest="show_summary", action="store_true")
    parser.add_argument("--no-summary", dest="show_summary", action="store_false")
    parser.set_defaults(show_summary=True)

    parser.add_argument(
        "--show-divergences", dest="show_divergences", action="store_true"
    )
    parser.add_argument(
        "--no-divergences", dest="show_divergences", action="store_false"
    )
    parser.set_defaults(show_divergences=True)

    parser.add_argument("--show-citations", dest="show_citations", action="store_true")
    parser.add_argument("--no-citations", dest="show_citations", action="store_false")
    parser.set_defaults(show_citations=False)

    parser.add_argument("--verbose", action="store_true")

    parser.add_argument("--output", help="Путь к файлу для экспорта результата")
    parser.add_argument(
        "--format",
        choices=["txt", "md"],
        default=None,
        help="Формат файла для экспорта",
    )

    parser.add_argument("--tts", dest="tts_enabled", action="store_true")
    parser.add_argument("--no-tts", dest="tts_enabled", action="store_false")
    parser.set_defaults(tts_enabled=None)

    parser.add_argument("--tts-engine", choices=["chatterbox"], default=None)
    parser.add_argument("--tts-model", choices=["turbo", "multilingual"], default=None)
    parser.add_argument("--tts-device", choices=["auto", "cuda", "cpu"], default=None)
    parser.add_argument("--tts-voice", default=None)
    parser.add_argument("--tts-speed", type=float, default=None)
    parser.add_argument("--tts-voice-prompt", default=None)
    parser.add_argument("--tts-tags", dest="tts_tags", action="store_true")
    parser.add_argument("--no-tts-tags", dest="tts_tags", action="store_false")
    parser.set_defaults(tts_tags=None)
    parser.add_argument("--tts-hf-token", default=None)
    parser.add_argument("--tts-output", default="output.wav")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    config = load_config(args.config)
    overrides = _build_overrides(args, config)
    config = apply_overrides(config, overrides)

    responses: list[AgentResponse] = []
    tts_text = ""
    if args.input:
        _log_status("Сбор", "Загрузка ответов из файла")
        responses = _load_responses(args.input)
        if not responses:
            _log_status("Сбор", "Ошибка: нет валидных ответов", error=True)
            print("Нет валидных ответов для синтеза.", file=sys.stderr)
            return 2
        _log_status("Сбор", "Загружено ответов: {count}".format(count=len(responses)))
    else:
        text = args.text or sys.stdin.read().strip()
        if not text:
            print("Нет текста для синтеза.", file=sys.stderr)
            return 2
        responses = [AgentResponse(agent_id=args.agent_id, content=text)]
        tts_text = text
        _log_status("Сбор", "Загружен текстовый ввод")

    _log_status("Синтез", "Формирование итога и расхождений")
    output = synthesize(
        responses,
        include_citations=args.show_citations or args.include_citations,
        show_summary=args.show_summary,
        show_divergences=args.show_divergences,
        show_citations=args.show_citations,
        verbose=args.verbose,
    )
    _log_status("Синтез", "Синтез завершен")
    print(output)

    if args.output:
        _export_to_file(
            output,
            args.output,
            args.format,
            show_summary=args.show_summary,
            show_divergences=args.show_divergences,
            show_citations=args.show_citations,
        )

    if not tts_text:
        tts_text = output
    _maybe_speak(tts_text, config, args.tts_output)
    return 0


def _load_responses(path: str) -> list[AgentResponse]:
    file_path = Path(path)
    if not file_path.exists():
        print(f"Файл не найден: {file_path}", file=sys.stderr)
        return []

    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"Некорректный JSON: {exc}", file=sys.stderr)
        return []

    if not isinstance(data, list):
        print("Ожидался список ответов в JSON.", file=sys.stderr)
        return []

    responses: list[AgentResponse] = []
    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            print(f"Пропуск элемента #{index}: ожидался объект.", file=sys.stderr)
            continue
        agent_id = str(item.get("agent_id", "")).strip()
        content = str(item.get("content", "")).strip()
        if not agent_id or not content:
            print(
                f"Пропуск элемента #{index}: нет agent_id или content.", file=sys.stderr
            )
            continue
        citations = item.get("citations")
        if citations is not None and not isinstance(citations, list):
            print(
                f"Пропуск цитат в элементе #{index}: ожидался список.", file=sys.stderr
            )
            citations = None
        responses.append(
            AgentResponse(agent_id=agent_id, content=content, citations=citations)
        )
    return responses


def _build_overrides(args: argparse.Namespace, config: AppConfig) -> dict:
    tts_overrides = {}
    if args.tts_enabled is not None:
        tts_overrides["enabled"] = args.tts_enabled
    if args.tts_engine is not None:
        tts_overrides["engine"] = args.tts_engine
    if args.tts_model is not None:
        tts_overrides["model"] = args.tts_model
    if args.tts_device is not None:
        tts_overrides["device"] = args.tts_device
    if args.tts_voice_prompt is not None:
        tts_overrides["voice_prompt_path"] = args.tts_voice_prompt
    if args.tts_voice is not None:
        tts_overrides["voice"] = args.tts_voice
    if args.tts_speed is not None:
        tts_overrides["speed"] = args.tts_speed
    if args.tts_tags is not None:
        tts_overrides["tags_enabled"] = args.tts_tags
    if args.tts_hf_token is not None:
        tts_overrides["hf_token"] = args.tts_hf_token

    return {"tts": tts_overrides}


def _log_status(stage: str, message: str, error: bool = False) -> None:
    prefix = "!" if error else ">"
    print(f"[status] {stage}: {message} [{prefix}]", file=sys.stderr)


def _is_ci_or_noninteractive() -> bool:
    ci_vars = {"CI", "GITHUB_ACTIONS", "GITLAB_CI", "JENKINS_URL"}
    for var in ci_vars:
        if os.environ.get(var):
            return True
    return not (sys.stdin.isatty() and sys.stdout.isatty())


def _maybe_speak(text: str, config: AppConfig, output_path: str) -> None:
    if not config.tts.enabled:
        return

    _log_status("Озвучка", "Запуск TTS")

    if _is_ci_or_noninteractive():
        _log_status("Озвучка", "CI/неинтерактивный режим, озвучка отключена")
        print("[tts] CI/неинтерактивный режим, озвучка отключена", file=sys.stderr)
        return

    provider = ChatterboxProvider()
    if not provider.is_available():
        _log_status("Озвучка", "Ошибка: chatterbox недоступен", error=True)
        print("[tts] chatterbox недоступен", file=sys.stderr)
        return

    output_file = Path(output_path)

    def _run_tts() -> None:
        try:
            result = provider.synthesize(text, config.tts, str(output_file))
        except Exception as exc:
            _log_status("Озвучка", f"Ошибка: {type(exc).__name__}", error=True)
            print(
                f"[tts] ошибка: {type(exc).__name__}",
                file=sys.stderr,
            )
            return
        for warning in result.warnings:
            print(f"[tts] {warning}", file=sys.stderr)
        if result.success:
            _log_status("Озвучка", f"Аудио сохранено: {result.audio_path}")
            print(f"[tts] audio сохранено: {result.audio_path}", file=sys.stderr)

    thread = threading.Thread(target=_run_tts, name="tts-worker", daemon=True)
    thread.start()


def _export_to_file(
    content: str,
    output_path: str,
    format: str | None,
    show_summary: bool = True,
    show_divergences: bool = True,
    show_citations: bool = False,
) -> None:
    output_file = Path(output_path)
    try:
        output_file.parent.mkdir(parents=True, exist_ok=True)
    except Exception as exc:
        print(
            f"[export] ошибка создания директории {output_file.parent}: {type(exc).__name__}",
            file=sys.stderr,
        )
        return

    if output_file.exists():
        print(f"[export] файл будет перезаписан: {output_file}", file=sys.stderr)

    file_format = format
    if file_format is None:
        file_format = "md" if output_file.suffix.lower() == ".md" else "txt"

    filtered_content = content

    sections = {
        "Итог": show_summary,
        "Расхождения": show_divergences,
        "Цитаты": show_citations,
    }

    lines = content.split("\n")
    filtered_lines: list[str] = []
    current_section: str | None = None
    keep_current = False

    for line in lines:
        if line in sections:
            current_section = line
            keep_current = sections[line]
            if keep_current:
                filtered_lines.append(line)
            continue
        if current_section and keep_current:
            filtered_lines.append(line)

    filtered_content = "\n".join(filtered_lines)

    try:
        output_file.write_text(filtered_content, encoding="utf-8")
        print(
            f"[export] результат сохранен: {output_file} ({file_format})",
            file=sys.stderr,
        )
    except Exception as exc:
        print(
            f"[export] ошибка сохранения файла: {type(exc).__name__}",
            file=sys.stderr,
        )


if __name__ == "__main__":
    raise SystemExit(main())
