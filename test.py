import os
import json
import datetime
import shutil
import subprocess


def env_true(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}

# 指定目录路径
directory_path = "./musics/"  # 请将路径替换为实际的目录路径
lrc_txt_path = "./lrc/"      # 歌词文本文件目录
bak_path = "./Baks/"         # 备份目录
json_filename = "musicList.json"

is_ci = env_true("CI")
skip_lrc_generation = env_true("SKIP_LRC_GENERATION", default=is_ci)
require_lrc = env_true("REQUIRE_LRC", default=is_ci)
disable_backup = env_true("DISABLE_BAK", default=is_ci)

audio_exts = {".mp3", ".m4a", ".flac", ".wav", ".ogg", ".aac"}

# 构建URL的基本部分
base_url = "https://github.com/lihan3238/music/raw/main/musics/"
base_lrc_url = "https://raw.githubusercontent.com/lihan3238/music/main/musics/"

# 确保lrc目录存在
if not os.path.exists(lrc_txt_path):
    os.makedirs(lrc_txt_path)

# 确保音乐目录存在
if not os.path.exists(directory_path):
    raise FileNotFoundError(f"Music directory not found: {directory_path}")

# 确保备份目录存在（仅在启用备份时）
if not disable_backup and not os.path.exists(bak_path):
    os.makedirs(bak_path)

# 获取目录中的所有文件名
file_names = [
    file
    for file in os.listdir(directory_path)
    if os.path.isfile(os.path.join(directory_path, file))
]
file_names.sort(key=lambda name: name.lower())

music_list = []
missing_lrc_files = []

# 遍历文件名
for file_name in file_names:
    ext = os.path.splitext(file_name)[1].lower()
    if ext not in audio_exts:
        continue

    file_path = os.path.join(directory_path, file_name)
    file_base_name = os.path.splitext(file_name)[0]
    lrc_file_name = file_base_name + ".lrc"
    lrc_file_path = os.path.join(directory_path, lrc_file_name)

    # 检查是否需要生成LRC（CI默认跳过）
    if not os.path.exists(lrc_file_path) and not skip_lrc_generation:
        txt_file_path = os.path.join(lrc_txt_path, file_base_name + ".txt")
        print(f"Generating LRC for {file_name}...")
        try:
            # 调用 lrcgen
            # 有歌词文本则使用 --lyrics-file，否则直接生成
            # 使用绝对路径以防万一
            abs_audio = os.path.abspath(file_path)
            abs_lrc = os.path.abspath(lrc_file_path)
            
            if os.path.exists(txt_file_path):
                abs_txt = os.path.abspath(txt_file_path)
                cmd = ["lrcgen", abs_audio, abs_lrc, "--lyrics-file", abs_txt, "--model", "large-v3"]
            else:
                cmd = ["lrcgen", abs_audio, abs_lrc, "--model", "large-v3"]

            subprocess.run(cmd, check=True)
            print(f"Successfully generated {lrc_file_name}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to generate LRC for {file_name}: {e}")
        except FileNotFoundError:
            print("Error: lrcgen command not found. Please ensure lrcgen is installed and in PATH.")

    # 重新检查lrc是否存在（可能刚生成）
    has_lrc = os.path.exists(lrc_file_path)
    
    if not has_lrc:
        print(f"Warning: missing matching LRC for {file_name} -> expected {lrc_file_name}")
        missing_lrc_files.append(file_name)

    # 构建信息
    lrc_url = base_lrc_url + lrc_file_name if has_lrc else ""
    
    name_part = file_base_name
    if "-" in name_part:
        parts = name_part.split("-")
        name = parts[0].strip()
        artists = "-".join(parts[1:]).strip()
    else:
        name = name_part
        artists = ""

    url = f"{base_url}{file_name}"

    music_obj = {
        "name": name,
        "url": url,
        "artist": artists,
        "cover": "https://user-images.githubusercontent.com/140466644/266218167-0a08d24b-2f75-4a6b-9253-227612dffa98.png"
    }
    if lrc_url:
        music_obj["lrc"] = lrc_url

    music_list.append(music_obj)


if require_lrc and missing_lrc_files:
    print("\nMissing matching .lrc files for these tracks:")
    for file_name in missing_lrc_files:
        print(f"- {file_name}")
    raise SystemExit(1)


# 写入 JSON 文件
print(f"Updating {json_filename}...")
with open(json_filename, "w", encoding="utf-8") as f:
    json.dump(music_list, f, ensure_ascii=False, indent=4)


# 备份逻辑
if not disable_backup:
    bak_files = [f for f in os.listdir(bak_path) if f.startswith("musicList_") and f.endswith(".json")]
    if len(bak_files) > 5:
        print("备份文件超过6个，正在删除最旧的备份文件...")
        oldest_file = min(
            bak_files, key=lambda x: os.path.getctime(os.path.join(bak_path, x))
        )
        os.remove(os.path.join(bak_path, oldest_file))

    current_date_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    backup_file = f"musicList_{current_date_time}.json"
    if os.path.exists(json_filename):
        shutil.copy(json_filename, os.path.join(bak_path, backup_file))
        print(f"已备份为 {backup_file}")
else:
    print("Backup is disabled by DISABLE_BAK.")

print(f"数据已写入到 {json_filename} 文件中。")
