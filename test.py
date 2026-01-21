import os
import json
import datetime
import shutil
import subprocess

# 指定目录路径
directory_path = "./musics/"  # 请将路径替换为实际的目录路径
lrc_txt_path = "./lrc/"      # 歌词文本文件目录
bak_path = "./Baks/"         # 备份目录
json_filename = "musicList.json"

# 构建URL的基本部分
base_url = "https://github.com/lihan3238/music/raw/main/musics/"
base_lrc_url = "https://raw.githubusercontent.com/lihan3238/music/main/musics/"

# 确保lrc目录存在
if not os.path.exists(lrc_txt_path):
    os.makedirs(lrc_txt_path)

# 获取目录中的所有文件名
file_names = [
    file
    for file in os.listdir(directory_path)
    if os.path.isfile(os.path.join(directory_path, file))
]

music_list = []

# 遍历文件名
for file_name in file_names:
    # 忽略非音乐文件（这里简单的通过排除.lrc来判断，或者检查常见音频格式，
    # 原逻辑是排除.lrc，我们保留原逻辑，但通常应该检查后缀）
    if file_name.endswith(".lrc"):
        continue

    file_path = os.path.join(directory_path, file_name)
    file_base_name = os.path.splitext(file_name)[0]
    lrc_file_name = file_base_name + ".lrc"
    lrc_file_path = os.path.join(directory_path, lrc_file_name)

    # 检查是否需要生成LRC
    if not os.path.exists(lrc_file_path):
        txt_file_path = os.path.join(lrc_txt_path, file_base_name + ".txt")
        if os.path.exists(txt_file_path):
            print(f"Generating LRC for {file_name}...")
            try:
                # 调用 lrcgen
                # 假设 lrcgen 命令格式: lrcgen <audio_file> <output_lrc> --lyrics-file <text_file>
                # 使用绝对路径以防万一
                abs_audio = os.path.abspath(file_path)
                abs_lrc = os.path.abspath(lrc_file_path)
                abs_txt = os.path.abspath(txt_file_path)
                
                cmd = ["lrcgen", abs_audio, abs_lrc, "--lyrics-file", abs_txt, "--model", "large-v3"]
                subprocess.run(cmd, check=True)
                print(f"Successfully generated {lrc_file_name}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to generate LRC for {file_name}: {e}")
            except FileNotFoundError:
                print("Error: lrcgen command not found. Please ensure lrcgen is installed and in PATH.")
        else:
            # print(f"Skipping generation for {file_name}: No corresponding txt file found in {lrc_txt_path}")
            pass

    # 重新检查lrc是否存在（可能刚生成）
    has_lrc = os.path.exists(lrc_file_path)
    
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


# 写入 JSON 文件
print(f"Updating {json_filename}...")
with open(json_filename, "w", encoding="utf-8") as f:
    json.dump(music_list, f, ensure_ascii=False, indent=4)


# 备份逻辑
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

print(f"数据已写入到 {json_filename} 文件中。")
