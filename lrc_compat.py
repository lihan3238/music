import re
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path


APLAYER_TIMESTAMP_PATTERN = re.compile(r"^\[\d{2}:\d{2}(?:\.\d{2,3})?\]$")
LRC_TIMESTAMP_PATTERN = re.compile(r"\[(\d{1,2}):(\d{1,2})(?:\.(\d+))?\]")


def _normalize_timestamp(match: re.Match) -> str:
    minutes, seconds, fraction = match.group(1), match.group(2), match.group(3)
    if len(minutes) == 2 and len(seconds) == 2 and (
        fraction is None or len(fraction) in {2, 3}
    ):
        return match.group(0)

    total_seconds = int(minutes) * 60 + int(seconds)
    if fraction is None:
        return f"[{total_seconds // 60:02d}:{total_seconds % 60:02d}]"

    if len(fraction) in {2, 3}:
        return f"[{total_seconds // 60:02d}:{total_seconds % 60:02d}.{fraction}]"

    if len(fraction) == 1:
        milliseconds = int(fraction) * 100
    else:
        milliseconds = int(
            (Decimal(f"0.{fraction}") * Decimal(1000)).quantize(
                Decimal("1"),
                rounding=ROUND_HALF_UP,
            )
        )

    if milliseconds >= 1000:
        total_seconds += 1
        milliseconds = 0

    return f"[{total_seconds // 60:02d}:{total_seconds % 60:02d}.{milliseconds:03d}]"


def normalize_lrc_timestamps(text: str) -> str:
    normalized_lines = []
    for line in text.splitlines(keepends=True):
        if line.endswith("\r\n"):
            body, newline = line[:-2], "\r\n"
        elif line.endswith("\n"):
            body, newline = line[:-1], "\n"
        else:
            body, newline = line, ""

        normalized_body = LRC_TIMESTAMP_PATTERN.sub(_normalize_timestamp, body)
        if normalized_body != body:
            normalized_body = normalized_body.rstrip(" \t")

        normalized_lines.append(normalized_body + newline)

    return "".join(normalized_lines)


def find_incompatible_lrc_timestamps(text: str) -> list[tuple[int, str]]:
    issues = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        for timestamp in LRC_TIMESTAMP_PATTERN.finditer(line):
            value = timestamp.group(0)
            if not APLAYER_TIMESTAMP_PATTERN.fullmatch(value):
                issues.append((line_number, value))
    return issues


def normalize_lrc_file(path: str | Path) -> bool:
    lrc_path = Path(path)
    with lrc_path.open("r", encoding="utf-8", newline="") as handle:
        original = handle.read()

    normalized = normalize_lrc_timestamps(original)
    if normalized == original:
        return False

    with lrc_path.open("w", encoding="utf-8", newline="") as handle:
        handle.write(normalized)

    return True
