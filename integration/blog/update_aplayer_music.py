import json
import os
import urllib.request

TARGET_FILE = os.getenv("TARGET_FILE", "layouts/partials/music.html")
MUSIC_URL = os.getenv(
    "MUSIC_URL",
    "https://raw.githubusercontent.com/lihan3238/music/main/musicList.json",
)

START_MARKER = "// MUSIC_LIST_START"
END_MARKER = "// MUSIC_LIST_END"


def read_remote_music_list(url: str):
    with urllib.request.urlopen(url, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def build_replacement_block(music_list):
    payload = json.dumps(music_list, ensure_ascii=False, indent=16)
    return (
        f"{START_MARKER}\n"
        f"                music: {payload}\n"
        f"                {END_MARKER}"
    )


def replace_between_markers(content: str, replacement: str):
    start = content.find(START_MARKER)
    end = content.find(END_MARKER)
    if start == -1 or end == -1 or end <= start:
        raise RuntimeError(
            "Markers not found or invalid. Please add '// MUSIC_LIST_START' and "
            "'// MUSIC_LIST_END' around the music array block."
        )

    end += len(END_MARKER)
    return content[:start] + replacement + content[end:]


def main():
    music_list = read_remote_music_list(MUSIC_URL)

    with open(TARGET_FILE, "r", encoding="utf-8") as f:
        original = f.read()

    updated = replace_between_markers(original, build_replacement_block(music_list))

    if updated == original:
        print("No changes detected in target file.")
        return

    with open(TARGET_FILE, "w", encoding="utf-8") as f:
        f.write(updated)

    print(f"Updated {TARGET_FILE} from {MUSIC_URL}")


if __name__ == "__main__":
    main()
