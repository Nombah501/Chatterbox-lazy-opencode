from pathlib import Path
import re
import sys


def main() -> int:
    plugin_path = Path.home() / ".config" / "opencode" / "plugin" / "cbx-speak.ts"
    if not plugin_path.exists():
        print(f"plugin file not found: {plugin_path}", file=sys.stderr)
        return 1

    text = plugin_path.read_text(encoding="utf-8")

    required = {
        "session.idle handler": r"session\.idle",
        "sessionID": r"sessionID",
        "messages fetch": r"client\.session\.messages",
        "assistant role": r"\"assistant\"",
        "text parts": r"type\s*===\s*\"text\"",
        "join newline": r"join\(\"\\n\"",
        "force tts flag": r"--tts-force",
        "hf token flag": r"--tts-hf-token",
        "quiet flag": r"--quiet",
        "local config": r"cbx-speak\.env",
    }

    missing = [
        label for label, pattern in required.items() if not re.search(pattern, text)
    ]
    if missing:
        print("missing required patterns:", file=sys.stderr)
        for label in missing:
            print(f"- {label}", file=sys.stderr)
        return 1

    print("ok: plugin scaffold matches required patterns")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
